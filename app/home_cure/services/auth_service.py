from sqlalchemy.orm import Session
from app.home_cure.repositories.user import user_repository
from app.utils.security import hash_password, verify_password


def authenticate_user(email: str, password: str, db: Session):
    user = user_repository.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    # Normalize role value to a plain string that matches UserRole values.
    try:
        raw = getattr(user, 'role', None)
        if isinstance(raw, str):
            cleaned = raw.strip().strip('"').strip("'").lower()
            # if model defines UserRole, ensure it's valid; otherwise just set cleaned
            from app.home_cure.models.user_model import UserRole as ModelUserRole
            if any(m.value == cleaned for m in ModelUserRole):
                user.role = cleaned
            else:
                # fallback: leave as-is
                user.role = cleaned
    except Exception:
        # be permissive; do not block authentication on normalization errors
        pass
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
