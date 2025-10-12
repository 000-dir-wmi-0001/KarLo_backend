from sqlalchemy.orm import Session
from app.home_cure.schemas import user_schema
from app.home_cure.repositories.user import user_repository
from app.utils.security import hash_password
from app.home_cure.models.user_model import UserRole  
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

  
def create_user(data: user_schema.UserCreate, db: Session):
    # Ensure role is set to default 'USER'
    data.role = UserRole.USER  # or "USER" if your repository handles the enum mapping

    try:
        created = user_repository.create_user(db, data)
    except IntegrityError as e:
        # Duplicate email
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return {"data": created, "message": "User created successfully"} 
  
def update_user(id: int, data: user_schema.UserUpdate, db: Session):
    return user_repository.update_user(db, id, data)

def get_user_by_id(id: int, db: Session):
    return user_repository.get_user_by_id(db, id)

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return user_repository.get_all_users(db, skip, limit)

def delete_user(id: int, db: Session):
    return user_repository.delete_user(db, id)
