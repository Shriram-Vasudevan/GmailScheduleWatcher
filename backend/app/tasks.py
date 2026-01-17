from app.celery_app import celery_app
from app.db.session import get_sync_db
from app.db.base import Email, EmailStatus
from app.services.gmail import send_email, check_thread_has_new_messages


@celery_app.task(bind=True, max_retries=3)
def send_scheduled_email(self, thread_id: str, to: str, subject: str, body: str, message_count_at_schedule: int = 0):
    # Send a scheduled email via Gmail API
    
    db = next(get_sync_db())

    if db is None:
        raise Exception("Database connection not found")

    email = db.query(Email).filter(Email.thread_id == thread_id).first()

    if email is None:
        raise Exception("Email record not found")

    if email.cancelled:
        return {"status": "cancelled", "reason": email.cancelled_reason}

    # Check if thread has new messages (auto-cancel feature)
    if message_count_at_schedule > 0:
        if check_thread_has_new_messages(thread_id, message_count_at_schedule):
            email.status = EmailStatus.CANCELLED
            email.cancelled = True
            email.cancelled_reason = "Thread received new messages before scheduled send time"
            db.commit()
            return {"status": "cancelled", "reason": email.cancelled_reason}

    try:
        result = send_email(
            to=to,
            subject=subject,
            body=body,
            thread_id=thread_id if message_count_at_schedule > 0 else None
        )

        email.status = EmailStatus.SENT
        email.sent = True
        db.commit()

        return {"status": "sent", "message_id": result.get("id")}

    except Exception as e:
        email.status = EmailStatus.FAILED
        email.cancelled_reason = str(e)
        db.commit()

        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
