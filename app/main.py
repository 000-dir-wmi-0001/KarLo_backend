from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.api.api import api_router
from app.core.config import settings


# Create tables only in dev or when using SQLite (avoid on remote DBs)
from urllib.parse import urlparse
is_sqlite = urlparse(settings.DATABASE_URL or "sqlite:///./karlo.db").scheme.startswith("sqlite")
if settings.DEBUG or is_sqlite:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KarLo API",
    description="FastAPI backend for KarLo data.",
    version="1.0.0"
)

# Register API routes
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://momin-mohasin.vercel.app",
        "https://kar-lo.vercel.app",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
