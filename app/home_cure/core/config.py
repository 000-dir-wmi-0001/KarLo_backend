"""
Home Cure Configuration
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
