from fastapi import APIRouter
from .routes.contribute_route import contribute_router
from .routes.contact_route import contact_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(contribute_router)
api_v1_router.include_router(contact_router)
