"""
Notification Model
Stores user notifications for bookings, updates, and system messages
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Notification(Base):
    __tablename__ = "home_cure_notification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("home_cure_user.id"), nullable=False)
    
    # Notification Details
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(100), nullable=False)  # booking, payment, system, etc.
    
    # Related Entity
    related_entity_type = Column(String(100), nullable=True)  # booking, payment, etc.
    related_entity_id = Column(Integer, nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(String, nullable=True)
    
    # Priority
    priority = Column(String(50), default="normal")  # low, normal, high
    
    # Action URL
    action_url = Column(String(500), nullable=True)  # Link to relevant page
    
    # Timestamps
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    user = relationship("User", back_populates="notifications", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, title={self.title}, is_read={self.is_read})>"
