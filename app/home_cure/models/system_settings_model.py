"""
System Settings Model
Stores configurable system-wide settings
"""
from sqlalchemy import Column, Integer, String, Text, Boolean
from app.db.base import Base
from datetime import datetime


class SystemSettings(Base):
    __tablename__ = "home_cure_system_settings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Setting Details
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    data_type = Column(String(50), default="string")  # string, number, boolean, json
    
    # Metadata
    category = Column(String(100), nullable=True)  # e.g., "payment", "notification", "general"
    description = Column(Text, nullable=True)
    is_editable = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())

    def __repr__(self):
        return f"<SystemSettings(id={self.id}, key={self.key}, value={self.value})>"
