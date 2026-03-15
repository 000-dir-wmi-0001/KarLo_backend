from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.karlo_c.api.v1.authz import get_current_user
from app.karlo_c.schemas.profile_schema import ProfileUpdate
from app.karlo_c.schemas.user_schema import UserResponse


profile_router = APIRouter(prefix="/profile", tags=["Profile"])


@profile_router.get("/me", response_model=UserResponse)
def get_my_profile(request: Request, db: Session = Depends(get_db)):
    return get_current_user(request, db)


@profile_router.put("/me", response_model=UserResponse)
def update_my_profile(payload: ProfileUpdate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
