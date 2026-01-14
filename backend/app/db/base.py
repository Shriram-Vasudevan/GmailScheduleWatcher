from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, MappedColumn, Integer, String, DateTime, Boolean
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Email(Base):
    __tablename__ = "emails"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True)
    email_id: Mapped[str] = MappedColumn(String, unique=True)
    status: Mapped[str] = MappedColumn(String)
    scheduled_time: Mapped[datetime] = MappedColumn(DateTime)
    sent: Mapped[bool] = MappedColumn(Boolean)
    cancelled: Mapped[bool] = MappedColumn(Boolean)
    cancelled_reason: Mapped[str] = MappedColumn(String)