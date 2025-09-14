from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.repositories.user import user_repository
from app.utils.security import hash_password


def create_user(data: user_schema.UserCreate, db: Session):
    # Do not pre-hash here; repository will map password -> hashed_password
    created = user_repository.create_user(db, data)
    return {"data": created, "message": "User created successfully"}
  
def update_user(id: int, data: user_schema.UserUpdate, db: Session):
    return user_repository.update_user(db, id, data)

def get_user_by_id(id: int, db: Session):
    return user_repository.get_user_by_id(db, id)

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return user_repository.get_all_users(db, skip, limit)

def delete_user(id: int, db: Session):
    return user_repository.delete_user(db, id)
