from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

class ScheduleEmailRequest(BaseModel):
    thread_id: str
    subject: str
    message_content: str
    scheduled_time: datetime
    
    @field_validator("scheduled_time")
    def validate_scheduled_time(cls, v):
        if v < datetime.now(timezone.utc):
            raise ValueError("Scheduled time must be in the future")
        return v


class GetEmailStatusRequest(BaseModel):
    email_id: str

class EmailStatusResponse(BaseModel):
    email_id: str
    status: str
    scheduled_time: datetime
    sent: bool
    cancelled: bool
    cancelled_reason: str
    