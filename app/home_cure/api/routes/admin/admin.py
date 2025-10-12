from fastapi import APIRouter
from .user_route import user_router
from .service_route import service_router
from .contact_route import contact_router
from .dashboard_route import dashboard_router



api_admin_router = APIRouter(prefix="/admin", tags=["Admin"])
api_admin_router.include_router(user_router)
api_admin_router.include_router(service_router)
api_admin_router.include_router(contact_router)
api_admin_router.include_router(dashboard_router)
