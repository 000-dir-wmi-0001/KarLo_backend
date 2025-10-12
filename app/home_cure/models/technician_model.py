"""
Technician Model
Stores technician profile information, specialization, and ratings
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Technician(Base):
    __tablename__ = "home_cure_technician"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("home_cure_user.id"), unique=True, nullable=False)
    
    # Professional Information
    specialization = Column(String(255), nullable=False)  # e.g., "Nurse", "Physical Therapist"
    certifications = Column(JSON, nullable=True)  # List of certifications
    experience_years = Column(Integer, default=0)
    license_number = Column(String(100), unique=True, nullable=True)
    
    # Ratings and Performance
    rating = Column(Float, default=0.0)  # Average rating (0-5)
    total_reviews = Column(Integer, default=0)
    completed_bookings = Column(Integer, default=0)
    
    # Availability
    is_available = Column(Boolean, default=True)
    availability_schedule = Column(JSON, nullable=True)  # e.g., {"monday": ["09:00-17:00"], ...}
    service_areas = Column(JSON, nullable=True)  # List of areas they service
    
    # Bio and Additional Info
    bio = Column(Text, nullable=True)
    profile_picture = Column(String(500), nullable=True)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    user = relationship("app.home_cure.models.user_model.User", back_populates="technician", foreign_keys=[user_id])
    bookings = relationship("Booking", back_populates="technician", foreign_keys="[Booking.technician_id]")
    earnings = relationship("TechnicianEarnings", back_populates="technician", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Technician(id={self.id}, user_id={self.user_id}, specialization={self.specialization}, rating={self.rating})>"
