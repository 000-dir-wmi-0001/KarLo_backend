from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.core.config import settings
from urllib.parse import urlparse

db_url = settings.DATABASE_URL or "sqlite:///./karlo.db"

parsed = urlparse(db_url)
is_sqlite = parsed.scheme.startswith("sqlite")

# Mask sensitive parts for logging
def _mask_url(u: str) -> str:
    try:
        p = urlparse(u)
        netloc = p.netloc
        if "@" in netloc:
            creds, host = netloc.split("@", 1)
            if ":" in creds:
                user, _ = creds.split(":", 1)
                netloc = f"{user}:***@{host}"
            else:
                netloc = f"***@{host}"
        masked = p._replace(netloc=netloc).geturl()
        return masked
    except Exception:
        return "<unavailable>"

masked = _mask_url(db_url)
if is_sqlite:
    print(f"[DB] Using SQLite fallback at {masked}. Set DATABASE_URL to use your remote DB.")
else:
    print(f"[DB] Using configured database: {masked}")

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
