"""
Home Cure Module - Healthcare Platform API
Handles user bookings, technician management, and health services
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api.home_cure_route import api_home_cure_router


# Public paths that don't require authentication
public_paths = [
    "/home_cure/auth/login",
    "/home_cure/auth/register",
    "/home_cure/auth/refresh-token",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup and shutdown events"""
    print("[HOME_CURE] Starting up...")
    yield
    print("[HOME_CURE] Shutting down...")


def create_home_cure_app() -> FastAPI:
    """Factory function to create the Home Cure FastAPI application"""
    app = FastAPI(
        title="Home Cure API",
        description="Healthcare platform for booking technicians and managing health services",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
            "https://momin-mohasin.vercel.app",
            "https://kar-lo.vercel.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Home Cure routes
    app.include_router(api_home_cure_router)

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Home Cure API",
            "version": "1.0.0",
            "endpoints": "/docs"
        }

    return app


# Create the app instance
home_cure_app = create_home_cure_app()
