from fastapi import APIRouter

from .routes.admin import admin
from .routes.user import user
from .routes.auth_route import auth_router

# No prefix here since the app will be mounted at /home_cure
api_home_cure_router = APIRouter(tags=["Home Cure"])
api_home_cure_router.include_router(admin.api_admin_router)
api_home_cure_router.include_router(user.api_user_router)
api_home_cure_router.include_router(auth_router)
