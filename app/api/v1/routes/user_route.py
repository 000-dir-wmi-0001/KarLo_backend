from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.services.user import user_service
from app.db.session import get_db

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/create", response_model=user_schema.CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)
  
@user_router.get("/{id}", response_model=user_schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    result = user_service.get_user_by_id(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
@user_router.get("/", response_model=user_schema.UserListResponse)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_all_users(db, skip, limit)
    return {
        "users": users,
        "total": len(users)
    }
@user_router.put("/update/{id}", response_model=user_schema.UserResponse)
def update_user(
    id: int,
    user: user_schema.UserUpdate,
    db: Session = Depends(get_db)
):
    result = user_service.update_user(id, user, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result 
@user_router.delete("/delete/{id}", response_model=user_schema.UserDeleteResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    result = user_service.delete_user(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "success": True,
        "message": f"User with ID {id} deleted successfully"
    } 
