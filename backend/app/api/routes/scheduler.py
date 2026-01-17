from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schedule import ScheduleEmailRequest, GetEmailStatusRequest, EmailStatusResponse
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Email, EmailStatus
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.tasks import send_scheduled_email

router = APIRouter()

@router.post("/schedule-email")
async def schedule_email(schedule_email_request: ScheduleEmailRequest, db: AsyncSession = Depends(get_db)):
    new_email = Email(
        thread_id=schedule_email_request.thread_id,
        status=EmailStatus.SCHEDULED,
        scheduled_time=schedule_email_request.scheduled_time,
        sent=False,
        cancelled=False,
        cancelled_reason=""
    )

    db.add(new_email)
    await db.commit()
    await db.refresh(new_email)

    # Schedule the Celery task to run at the specified time
    send_scheduled_email.apply_async(
        args=[
            schedule_email_request.thread_id,
            schedule_email_request.to,
            schedule_email_request.subject,
            schedule_email_request.message_content,
            schedule_email_request.message_count_at_schedule
        ],
        eta=schedule_email_request.scheduled_time
    )

    return JSONResponse(status_code=201, content={"message": "Email scheduled successfully", "id": new_email.id})

@router.get("/get-email-status")
async def schedule_email_status(get_email_status_request: GetEmailStatusRequest, db: AsyncSession = Depends(get_db)) -> EmailStatusResponse:
    email_status = await db.execute(select(Email).where(Email.id == get_email_status_request.email_id))
    email = email_status.scalar_one_or_none()
    if email:
        return EmailStatusResponse(
            email_id=email.email_id,
            status=email.status,
            scheduled_time=email.scheduled_time,
            sent=email.sent,
            cancelled=email.cancelled,
            cancelled_reason=email.cancelled_reason
        )
    else:
        raise HTTPException(status_code=404, detail="Email not found")