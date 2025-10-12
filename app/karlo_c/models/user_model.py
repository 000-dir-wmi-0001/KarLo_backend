from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base


def _now_utc():
    """Return a timezone-aware UTC datetime for SQLAlchemy defaults."""
    return datetime.now(timezone.utc)


class KarloUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String, index=True, nullable=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)  # True for active
    is_superuser = Column(Boolean, default=False)  # True for superuser
    is_verified = Column(Boolean, default=True)  # True for verified (consider default=False depending on flow)
    profile_picture = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    country = Column(String, index=True, nullable=True)
    state = Column(String, index=True, nullable=True)
    city = Column(String, index=True, nullable=True)
    zip_code = Column(String, index=True, nullable=True)
    address = Column(String, index=True, nullable=True)
    # Use timezone-aware DateTime columns
    last_login = Column(DateTime(timezone=True), nullable=True)
    role = Column(String, index=True, nullable=True, default="user")  # e.g., admin, user, moderator
    geo_location = Column(String, nullable=True)  # e.g., "37.7749,-122.4194"
    is_deleted = Column(Boolean, default=False)  # True for deleted
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc)
    updated_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc, onupdate=_now_utc)
