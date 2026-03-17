from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.karlo_c.api.v1.authz import get_current_user
from app.karlo_c.models.user_settings_model import UserSettings
from app.karlo_c.schemas.settings_schema import UserSettingsResponse, UserSettingsUpdate


settings_router = APIRouter(prefix="/settings", tags=["Settings"])


def _get_or_create_settings(user_id: int, db: Session) -> UserSettings:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if settings:
        return settings

    settings = UserSettings(user_id=user_id)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@settings_router.get("/me", response_model=UserSettingsResponse)
def get_my_settings(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return _get_or_create_settings(user.id, db)


@settings_router.put("/me", response_model=UserSettingsResponse)
def update_my_settings(payload: UserSettingsUpdate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    settings = _get_or_create_settings(user.id, db)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(settings, field):
            setattr(settings, field, value)

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings
