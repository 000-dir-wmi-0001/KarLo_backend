from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.db.base import Base


def _now_utc():
    return datetime.now(timezone.utc)

class Contact(Base):
  __tablename__ = 'contact'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  email = Column(String, index=True)
  subject = Column(String, index=True)
  message = Column(String, index=True)
  website = Column(String, index=True, nullable=True)
  is_read = Column(Boolean, default=False)
  created_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc)
