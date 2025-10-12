from sqlalchemy.orm import Session
from app.home_cure.models.user_model import User
from app.home_cure.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.home_cure.repositories.crud import CRUDBase
from app.utils.security import hash_password

curd_user = CRUDBase(User)

def create_user(db: Session, data: UserCreate):
  # Convert Pydantic model to dict and map password -> hashed_password
  payload = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
  raw_password = payload.pop('password', None)
  if raw_password:
    payload['hashed_password'] = hash_password(raw_password)
  # Ensure role is a plain string (enum members -> their value)
  role_val = payload.get('role')
  try:
    # If Pydantic left an Enum member, extract its value
    if hasattr(role_val, 'value'):
      payload['role'] = role_val.value
  except Exception:
    # be permissive; if anything goes wrong leave payload as-is
    pass
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