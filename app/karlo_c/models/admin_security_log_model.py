"""
Admin Action Security Log model.
Append-only audit table — records every sensitive admin action.
Never deleted or modified after creation.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from app.db.base import Base


def _now_utc():
    return datetime.now(timezone.utc)


class AdminSecurityLog(Base):
    """Immutable audit trail for all admin actions."""
    __tablename__ = "admin_security_log"

    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, nullable=False, index=True)       # who performed it
    admin_email = Column(String, nullable=True)                        # snapshot at time of action
    action = Column(String(100), nullable=False, index=True)           # e.g. "soft_delete_user"
    target_type = Column(String(50), nullable=True)                    # e.g. "user", "task", "contact"
    target_id = Column(Integer, nullable=True)                         # ID of affected resource
    detail = Column(String(500), nullable=True)                        # human-readable note
    performed_at = Column(DateTime(timezone=True), nullable=False, default=_now_utc)
