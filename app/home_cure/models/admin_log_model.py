"""
Admin Log Model
Tracks all admin activities for audit trail
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class AdminLog(Base):
    __tablename__ = "home_cure_admin_log"

    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, ForeignKey("home_cure_user.id"), nullable=False)
    
    # Action Details
    action = Column(String(255), nullable=False)  # e.g., "user_updated", "booking_assigned"
    entity_type = Column(String(100), nullable=False)  # user, booking, technician, etc.
    entity_id = Column(Integer, nullable=True)  # ID of the affected entity
    
    # Change Details
    description = Column(Text, nullable=False)
    previous_values = Column(JSON, nullable=True)  # Before changes
    new_values = Column(JSON, nullable=True)  # After changes
    
    # Context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Timestamp
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    admin_user = relationship("User", foreign_keys=[admin_user_id])

    def __repr__(self):
        return f"<AdminLog(id={self.id}, action={self.action}, entity_type={self.entity_type}, admin_user_id={self.admin_user_id})>"
