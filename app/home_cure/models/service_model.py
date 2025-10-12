from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


def _now_utc():
    return datetime.now(timezone.utc)


class Service(Base):
    __tablename__ = "home_cure_service"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    duration_minutes = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc)
    updated_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc, onupdate=_now_utc)
    
    # Relationships
    bookings = relationship("Booking", back_populates="service", foreign_keys="[Booking.service_id]")
