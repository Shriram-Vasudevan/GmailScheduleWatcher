from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, Enum as SQLAlchemyEnum
from datetime import datetime
from typing import Optional
import enum

class EmailStatus(enum.Enum):
    SCHEDULED = "scheduled"
    SENT = "sent"
    CANCELLED = "cancelled"
    FAILED = "failed"
class Base(DeclarativeBase):
    pass

class Email(Base):
    __tablename__ = "emails"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    status: Mapped[EmailStatus] = mapped_column(SQLAlchemyEnum(EmailStatus))
    scheduled_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    cancelled_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
