from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


def _now_utc():
    return datetime.now(timezone.utc)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True, index=True)
    default_radius_meters = Column(Integer, nullable=False, default=150)
    default_reminder_schedule = Column(String(20), nullable=False, default="daily")
    notifications_enabled = Column(Boolean, nullable=False, default=True)
    live_tracking_enabled = Column(Boolean, nullable=False, default=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_now_utc, onupdate=_now_utc)
