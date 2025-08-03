# app/db/init_db.py

from app.db.base import Base
from app.db.session import engine
from app.models import user  # Add other models here as needed

def init_db():
    Base.metadata.create_all(bind=engine)
