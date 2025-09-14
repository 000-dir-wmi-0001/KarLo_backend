from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.repositories.crud import CRUDBase
from app.utils.security import hash_password

curd_user = CRUDBase(User)

def create_user(db: Session, data: UserCreate):
  # Convert Pydantic model to dict and map password -> hashed_password
  payload = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
  raw_password = payload.pop('password', None)
  if raw_password:
    payload['hashed_password'] = hash_password(raw_password)
  return curd_user.create(db, payload)

def update_user(db:Session, id:int, data:UserUpdate):
  db_obj = curd_user.get_by_id(db, id)
  if not db_obj:
    return None
  return curd_user.update(db, db_obj, data)

def get_user_by_id(db:Session, id:int):
  return curd_user.get_by_id(db, id)

def get_user_by_email(db:Session, email:str):
  return db.query(User).filter(User.email == email).first()

def get_all_users(db:Session, skip:int=0, limit:int=100):
  return curd_user.get_all(db, skip, limit)


def delete_user(db:Session, id:int):
  db_obj = curd_user.get_by_id(db, id)
  if not db_obj:
    return None
  return curd_user.delete(db, db_obj)