from fastapi import APIRouter
from .routes.contribute_route import contribute_router
from .routes.contact_route import contact_router
from .routes.user_route import user_router
from .routes.auth_route import auth_router


api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(contribute_router)
api_v1_router.include_router(contact_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(auth_router)
