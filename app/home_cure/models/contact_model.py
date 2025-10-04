from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Contact(Base):
    __tablename__ = 'home_cure_contact'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String(10), index=True, nullable=True)  # max length 10
    message = Column(String, nullable=True)  # no index for long text
