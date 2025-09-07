from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Contact(Base):
  __tablename__ = 'contact'

  id = Column(Integer, primary_key=True, index=True)
  email= Column(String, index=True)
  subject = Column(String, index=True)
  message = Column(String, index=True)
  website = Column(String, index=True,nullable=True)
