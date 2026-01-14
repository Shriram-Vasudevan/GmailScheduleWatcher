from pydantic import BaseModel
from datetime import datetime

class ScheduleEmailRequest(BaseModel):
    thread_id: str
    subject: str
    message_content: str
    scheduled_time: datetime


class GetEmailStatusRequest(BaseModel):
    email_id: str

class EmailStatusResponse(BaseModel):
    email_id: str
    status: str
    scheduled_time: datetime
    sent: bool
    cancelled: bool
    cancelled_reason: str
    