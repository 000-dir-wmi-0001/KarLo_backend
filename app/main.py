from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.api.api import api_router
from app.core.config import settings


# Create tables if not using Alembic (dev only)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contribute API",
    description="FastAPI backend for contributor data.",
    version="1.0.0"
)

# Register API routes
app.include_router(api_router)

# Setup CORS
origins = settings.CORS_ORIGINS.split(",") if isinstance(settings.CORS_ORIGINS, str) else settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
