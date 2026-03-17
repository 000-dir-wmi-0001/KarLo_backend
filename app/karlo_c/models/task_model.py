from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from app.db.base import Base


def _now_utc():
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)

    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    radius_meters = Column(Integer, nullable=False, default=150)
    reminder_schedule = Column(String(20), nullable=False, default="daily")

    remind_on_arrival = Column(Boolean, nullable=False, default=True)
    is_completed = Column(Boolean, nullable=False, default=False)

    due_at = Column(DateTime(timezone=True), nullable=True)
    last_triggered_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=_now_utc)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_now_utc, onupdate=_now_utc)
