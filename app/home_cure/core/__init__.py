"""
Home Cure Core Configuration
"""
from typing import List

# Public paths that don't require authentication
HOME_CURE_PUBLIC_PATHS: List[str] = [
    "/home_cure/auth/login",
    "/home_cure/auth/register",
    "/home_cure/auth/refresh-token",
    "/home_cure/auth/test",
    "/home_cure/",
    "/home_cure/docs",
    "/home_cure/redoc",
    "/home_cure/openapi.json",
]

# Home Cure specific settings
HOME_CURE_SETTINGS = {
    "title": "Home Cure API",
    "description": "Healthcare platform for booking technicians and managing health services",
    "version": "1.0.0",
    "prefix": "/home_cure",
}
