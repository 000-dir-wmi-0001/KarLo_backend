from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.core.config import settings
from urllib.parse import urlparse

db_url = settings.DATABASE_URL or "sqlite:///./karlo.db"

parsed = urlparse(db_url)
is_sqlite = parsed.scheme.startswith("sqlite")

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if is_sqlite else {},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
