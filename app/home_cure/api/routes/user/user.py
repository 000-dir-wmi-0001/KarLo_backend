from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .services_route import services_router
from .contact_route import contact_router
from app.home_cure.services import user_service
from app.home_cure.schemas import user_schema
from app.db.session import get_db


api_user_router = APIRouter(prefix="/user", tags=["User"])

api_user_router.include_router(services_router)
api_user_router.include_router(contact_router)


# Patch alias: support client requests that PATCH /home_cure/user/{id}/update
@api_user_router.patch("/{user_id}/update", response_model=user_schema.UserResponse)
def patch_update_user(user_id: int, user_data: user_schema.UserUpdate, db: Session = Depends(get_db)):
	updated_user = user_service.update_user(user_id, user_data, db)
	if not updated_user:
		raise HTTPException(status_code=404, detail="User not found")
	return updated_user