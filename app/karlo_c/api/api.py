
from fastapi import APIRouter
from .v1.route_v1 import api_v1_router
# from app.api.v2 import v2_router

api_router = APIRouter(prefix="/api", tags=["API"])
api_router.include_router(api_v1_router)

# api_router.include_router(v2_router)
