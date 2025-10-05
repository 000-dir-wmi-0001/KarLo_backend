from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SAEnum
from app.db.base import Base
import enum


def _now_utc():
    """Return a timezone-aware UTC datetime for SQLAlchemy defaults."""
    return datetime.now(timezone.utc)


# --- Enum for user roles (string-backed) ---
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"
    USER = "user"


# --- User Model ---
class User(Base):
    __tablename__ = "home_cure_user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String, index=True, nullable=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(String, index=True, nullable=True)
    date_of_birth = Column(DateTime, index=True, nullable=True)

    # Account status flags
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    # Profile info
    profile_picture = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    country = Column(String, index=True, nullable=True)
    state = Column(String, index=True, nullable=True)
    city = Column(String, index=True, nullable=True)
    zip_code = Column(String, index=True, nullable=True)
    address = Column(String, index=True, nullable=True)

    # Role system: store as plain string to avoid DB Enum processing issues.
    # Some rows may contain extra quotes (e.g. '"user"') from earlier inserts;
    # the `role_enum` property below will normalize values into the UserRole enum.
    role = Column(String, nullable=False, default=UserRole.USER.value)

    # Location and metadata
    geo_location = Column(String, nullable=True)  # e.g., "37.7749,-122.4194"
    last_login = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now_utc)
    updated_at = Column(DateTime(timezone=True), default=_now_utc, onupdate=_now_utc)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

    @property
    def role_enum(self):
        """Return the role as a UserRole enum, normalizing stored strings.

        Handles values stored with surrounding quotes or differing case.
        Returns None if the stored value can't be mapped.
        """
        raw = self.role
        if raw is None:
            return None
        # strip surrounding quotes if present
        if isinstance(raw, str):
            cleaned = raw.strip().strip('"').strip("'").lower()
            for member in UserRole:
                if member.value == cleaned:
                    return member
        return None
