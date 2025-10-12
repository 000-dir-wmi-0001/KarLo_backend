"""
Health Record Model
Stores user's health history and service records
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class HealthRecord(Base):
    __tablename__ = "home_cure_health_record"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("home_cure_user.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("home_cure_booking.id"), nullable=True)
    
    # Record Details
    record_type = Column(String(100), nullable=False)  # e.g., "checkup", "therapy", "consultation"
    record_date = Column(String(100), nullable=False)  # ISO format date
    
    # Medical Information
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    medications = Column(JSON, nullable=True)  # List of medications
    vitals = Column(JSON, nullable=True)  # Blood pressure, temperature, etc.
    
    # Documents
    documents = Column(JSON, nullable=True)  # List of document URLs
    lab_results = Column(JSON, nullable=True)  # Lab test results
    
    # Provider Information
    provider_name = Column(String(255), nullable=True)
    provider_notes = Column(Text, nullable=True)
    
    # Follow-up
    follow_up_required = Column(String(10), default="no")  # yes/no
    follow_up_date = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    user = relationship("app.home_cure.models.user_model.User", back_populates="health_records", foreign_keys=[user_id])
    booking = relationship("Booking", foreign_keys=[booking_id])

    def __repr__(self):
        return f"<HealthRecord(id={self.id}, user_id={self.user_id}, record_type={self.record_type}, record_date={self.record_date})>"
