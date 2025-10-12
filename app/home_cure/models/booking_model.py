"""
Booking Model
Handles service bookings with QR codes, status tracking, and technician assignments
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import enum


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Booking(Base):
    __tablename__ = "home_cure_booking"

    id = Column(Integer, primary_key=True, index=True)
    
    # References
    user_id = Column(Integer, ForeignKey("home_cure_user.id"), nullable=False)
    technician_id = Column(Integer, ForeignKey("home_cure_technician.id"), nullable=True)
    service_id = Column(Integer, ForeignKey("home_cure_service.id"), nullable=False)
    
    # Booking Details
    status = Column(String(50), default=BookingStatus.PENDING.value, nullable=False)
    scheduled_date = Column(String(100), nullable=False)  # ISO format datetime
    scheduled_time = Column(String(50), nullable=False)  # e.g., "14:00"
    duration_minutes = Column(Integer, default=60)
    
    # Location
    service_address = Column(Text, nullable=False)
    service_location = Column(String(255), nullable=True)  # Geo coordinates
    
    # QR Code
    qr_code = Column(Text, nullable=True)  # Base64 encoded QR code image
    qr_code_data = Column(String(500), nullable=True)  # Data encoded in QR
    
    # Payment
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String(50), default="pending")  # pending, paid, refunded
    payment_method = Column(String(50), nullable=True)
    
    # Notes
    user_notes = Column(Text, nullable=True)
    technician_notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    
    # Ratings and Feedback
    user_rating = Column(Float, nullable=True)  # User rates the service (0-5)
    user_review = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    completed_at = Column(String, nullable=True)
    cancelled_at = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bookings", foreign_keys=[user_id])
    technician = relationship("Technician", back_populates="bookings", foreign_keys=[technician_id])
    service = relationship("Service", back_populates="bookings", foreign_keys=[service_id])

    def __repr__(self):
        return f"<Booking(id={self.id}, user_id={self.user_id}, status={self.status}, scheduled_date={self.scheduled_date})>"
