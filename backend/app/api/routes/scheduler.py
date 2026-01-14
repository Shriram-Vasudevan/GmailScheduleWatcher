from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schedule import ScheduleEmailRequest, GetEmailStatusRequest, EmailStatusResponse
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Email
from sqlalchemy import select

router = APIRouter()

@router.post("/schedule-email")
async def schedule_email(schedule_email_request: ScheduleEmailRequest):
    return {"message": "Email scheduled successfully"}

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