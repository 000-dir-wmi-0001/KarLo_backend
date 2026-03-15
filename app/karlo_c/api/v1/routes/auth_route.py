from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.karlo_c.schemas import user_schema
from app.karlo_c.services.auth import auth_service
from app.karlo_c.services.user import user_service
from app.db.session import get_db
from app.utils.token.jwt import create_token, verify_token, create_refresh_token
from app.core.config import settings
from datetime import timedelta

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )


@auth_router.post("/register", response_model=user_schema.CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)


@auth_router.post("/login", response_model=user_schema.UserLoginResponse)
def login(user: user_schema.UserLogin, response: Response, db: Session = Depends(get_db)):
    user_obj = auth_service.authenticate_user(user.email, user.password, db)
    if not user_obj:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # generate tokens directly
    access_token = create_token(
        data={"sub": str(user_obj.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )
    refresh_token = create_token(
        data={"sub": str(user_obj.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )

    _set_auth_cookies(response, access_token, refresh_token)

    return user_schema.UserLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
        user=user_obj
    )


  
@auth_router.put("/update-password/{user_id}", response_model=user_schema.UserResponse)
def update_password(
    user_id: int,
    password_update: user_schema.PasswordUpdate,
    db: Session = Depends(get_db),
    request: Request = None,
):
    # Require that the token subject matches the user_id
    token_payload = getattr(request.state, "user", None) if request else None
    token_sub = token_payload.get("sub") if isinstance(token_payload, dict) else None
    if token_sub is None or str(user_id) != str(token_sub):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    result = auth_service.update_password(user_id, password_update.new_password, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
  
@auth_router.post("/refresh-token", response_model=user_schema.UserLoginResponse)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    # Validate as a refresh token
    payload = verify_token(token, expected_type="refresh")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")

    user_obj = user_service.get_user_by_id(int(sub), db)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    # Issue new access token (and rotate refresh token)
    access_token = create_token(
        data={"sub": str(user_obj.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )
    new_refresh_token = create_refresh_token({"sub": str(user_obj.id)})

    _set_auth_cookies(response, access_token, new_refresh_token)

    return user_schema.UserLoginResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_obj,
    )


@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        domain=settings.COOKIE_DOMAIN,
        path="/",
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
    response.delete_cookie(
        key="refresh_token",
        domain=settings.COOKIE_DOMAIN,
        path="/",
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
    return {"message": "Logged out successfully"}


@auth_router.get("/me", response_model=user_schema.UserResponse)
def me(request: Request, db: Session = Depends(get_db)):
    token_payload = getattr(request.state, "user", None)
    token_sub = token_payload.get("sub") if isinstance(token_payload, dict) else None
    if token_sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user_obj = user_service.get_user_by_id(int(token_sub), db)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user_obj