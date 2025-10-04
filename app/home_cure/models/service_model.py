from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float
from app.db.base import Base


def _now_utc():
    return datetime.now(timezone.utc)


class Service(Base):
    __tablename__ = "home_cure_service"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc)
    updated_at = Column(DateTime(timezone=True), nullable=True, default=_now_utc, onupdate=_now_utc)
