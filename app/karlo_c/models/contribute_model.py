from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Contribute(Base):
  __tablename__ = 'contribute'

  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String, index=True)
  last_name = Column(String, index=True)
  email= Column(String, index=True)
  gitHub_link = Column(String, index=True)
  linkedIn_link = Column(String, index=True)
  country = Column(String, index=True)
  state = Column(String, index=True)
  city = Column(String, index=True)
  zip_code = Column(String, index=True)
