from sqlalchemy import create_engine, text
from app.core.config import settings

print("[DB] URL:", settings.DATABASE_URL.split('@')[-1])
engine = create_engine(settings.DATABASE_URL)

try:
    with engine.connect() as conn:
        # Alembic version table check
        try:
            ver = conn.execute(text("SELECT version_num FROM alembic_version")).fetchall()
            print("[Alembic] version:", ver)
        except Exception as e:
            print("[Alembic] version table missing or unreadable:", e)

        # Contact table columns
        cols = conn.execute(text(
            """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='contact' 
            ORDER BY ordinal_position
            """
        )).fetchall()
        print("[Schema] contact columns:", [c[0] for c in cols])
except Exception as e:
    print("[DB] Connection error:", e)
