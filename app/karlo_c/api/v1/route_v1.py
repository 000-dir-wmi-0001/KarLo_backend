from fastapi import APIRouter
from .routes.contribute_route import contribute_router
from .routes.contact_route import contact_router
from .routes.user_route import user_router
from .routes.auth_route import auth_router
from .routes.task_route import task_router
from .routes.geocode_route import geocode_router
from .routes.profile_route import profile_router
from .routes.settings_route import settings_router
from .routes.reminders_route import reminders_router
from .routes.activity_route import activity_router


api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(contribute_router)
api_v1_router.include_router(contact_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(task_router)
api_v1_router.include_router(geocode_router)
api_v1_router.include_router(profile_router)
api_v1_router.include_router(settings_router)
api_v1_router.include_router(reminders_router)
api_v1_router.include_router(activity_router)
