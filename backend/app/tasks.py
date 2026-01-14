from app.celery_app import celery_app
from app.db.session import get_db
from app.db.base import Email, EmailStatus

@celery_app.task
def send_scheduled_email(thread_id: str):
    db = next(get_db())

    if db is None:
        raise Exception("Database connection not found")
    
    email = db.query(Email).filter(Email.thread_id == thread_id).first()

    if email is None or email.cancelled:
        raise Exception("Email not found")
    
    if email.cancelled:
        raise Exception("Email has been cancelled")

    try:
        # TODO: Implement Gmail sending logic
        pass
    except Exception as e:
        email.status = EmailStatus.FAILED
        email.cancelled_reason = str(e)
        db.commit()
        db.refresh(email)
        raise e

    email.status = EmailStatus.SENT
    email.sent = True
    db.commit()
    db.refresh(email)
