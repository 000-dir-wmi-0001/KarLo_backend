from sqlalchemy.orm import Session
from app.karlo_c.repositories.user import user_repository
from app.utils.security import hash_password, verify_password


def authenticate_user(email: str, password: str, db: Session):
    user = user_repository.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_password(user_id: int, new_password: str, db: Session):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        return None
    hashed_password = hash_password(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
