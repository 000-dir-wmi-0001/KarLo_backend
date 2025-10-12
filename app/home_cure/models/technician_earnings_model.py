"""
Technician Earnings Model
Tracks earnings and payments for technicians
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class TechnicianEarnings(Base):
    __tablename__ = "home_cure_technician_earnings"

    id = Column(Integer, primary_key=True, index=True)
    technician_id = Column(Integer, ForeignKey("home_cure_technician.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("home_cure_booking.id"), nullable=False)
    
    # Earnings Details
    amount = Column(Float, nullable=False)
    commission_rate = Column(Float, default=0.15)  # 15% commission to platform
    net_earnings = Column(Float, nullable=False)  # Amount after commission
    
    # Payment Status
    payment_status = Column(String(50), default="pending")  # pending, paid, on_hold
    payment_date = Column(String(100), nullable=True)  # ISO format date
    payment_method = Column(String(100), nullable=True)  # bank_transfer, wallet, etc.
    
    # Transaction Details
    transaction_id = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    technician = relationship("Technician", back_populates="earnings", foreign_keys=[technician_id])
    booking = relationship("Booking", foreign_keys=[booking_id])

    def __repr__(self):
        return f"<TechnicianEarnings(id={self.id}, technician_id={self.technician_id}, amount={self.amount}, status={self.payment_status})>"
