from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.karlo_c.services.user import user_service


def get_current_user_payload(request: Request) -> dict:
    token_payload = getattr(request.state, "user", None)
    if not isinstance(token_payload, dict):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return token_payload


def get_current_user_id(request: Request) -> int:
    token_payload = get_current_user_payload(request)
    token_sub = token_payload.get("sub")
    if token_sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return int(token_sub)


def get_current_user(request: Request, db: Session):
    user_id = get_current_user_id(request)
    current_user = user_service.get_user_by_id(user_id, db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return current_user


def require_superuser(request: Request, db: Session):
    current_user = get_current_user(request, db)
    if not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return current_user


def require_self_or_superuser(target_user_id: int, request: Request, db: Session):
    current_user = get_current_user(request, db)
    if getattr(current_user, "is_superuser", False):
        return current_user
    if int(current_user.id) != int(target_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return current_user