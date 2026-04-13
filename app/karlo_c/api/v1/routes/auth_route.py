from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.karlo_c.schemas import user_schema
from app.karlo_c.schemas.user_schema import MFASetupResponse, MFAEnableRequest, MFAEnableResponse, MFAVerifyRequest, MFAStatusResponse
from app.karlo_c.services.auth import auth_service
from app.karlo_c.services.user import user_service
from app.karlo_c.services.mfa import mfa_service
from app.db.session import get_db
from app.utils.token.jwt import create_token, verify_token, create_refresh_token
from app.core.config import settings
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str, remember_me: bool = False):
    access_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    refresh_max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60 if remember_me else None
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        max_age=access_max_age,
        path="/",
    )
    if refresh_max_age is not None:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            max_age=refresh_max_age,
            path="/",
        )
    else:
        # Session cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            path="/",
        )


@auth_router.post("/register", response_model=user_schema.CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(user, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")


@auth_router.post("/login", response_model=user_schema.UserLoginResponse)
def login(user: user_schema.UserLogin, response: Response, db: Session = Depends(get_db)):
    user_obj = auth_service.authenticate_user(user.email, user.password, db)
    if not user_obj:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # generate tokens directly
    token_data = {"sub": str(user_obj.id), "is_superuser": user_obj.is_superuser}

    access_token = create_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )
    refresh_token = create_token(
        data=token_data,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )

    _set_auth_cookies(response, access_token, refresh_token, remember_me=user.remember_me)

    if user_obj.mfa_enabled:
        # Don't issue real auth cookies yet — set a short-lived pending cookie
        response.delete_cookie(key="access_token", path="/")
        response.delete_cookie(key="refresh_token", path="/")
        response.set_cookie(
            key="mfa_pending",
            value=str(user_obj.id),
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            max_age=300,
            path="/",
        )
        return user_schema.UserLoginResponse(user=user_obj, message="mfa_required")

    return user_schema.UserLoginResponse(
        user=user_obj,
        message="Login successful"
    )


  
@auth_router.put("/update-password/{user_id}", response_model=user_schema.UserResponse)
def update_password(
    user_id: int,
    password_update: user_schema.PasswordUpdate,
    db: Session = Depends(get_db),
    request: Request = None,
):
    token_payload = getattr(request.state, "user", None) if request else None
    token_sub = token_payload.get("sub") if isinstance(token_payload, dict) else None
    if token_sub is None or str(user_id) != str(token_sub):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Verify current password
    user_obj = auth_service.authenticate_user_by_id(user_id, password_update.current_password, db)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

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
        data={"sub": str(user_obj.id), "is_superuser": user_obj.is_superuser},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )
    new_refresh_token = create_refresh_token({"sub": str(user_obj.id), "is_superuser": user_obj.is_superuser})

    _set_auth_cookies(response, access_token, new_refresh_token)

    return user_schema.UserLoginResponse(
        user=user_obj,
        message="Token refreshed successfully"
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


# ── MFA ──────────────────────────────────────────────────────────────────────

def _get_authed_user(request: Request, user_id: int, db: Session):
    token_payload = getattr(request.state, "user", None)
    token_sub = token_payload.get("sub") if isinstance(token_payload, dict) else None
    if token_sub is None or str(user_id) != str(token_sub):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    user_obj = user_service.get_user_by_id(user_id, db)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_obj


@auth_router.get("/mfa/{user_id}/status", response_model=MFAStatusResponse)
def mfa_status(user_id: int, request: Request, db: Session = Depends(get_db)):
    user_obj = _get_authed_user(request, user_id, db)
    return MFAStatusResponse(mfa_enabled=user_obj.mfa_enabled, mfa_enabled_at=user_obj.mfa_enabled_at)


@auth_router.post("/mfa/{user_id}/setup", response_model=MFASetupResponse)
def mfa_setup(user_id: int, request: Request, db: Session = Depends(get_db)):
    user_obj = _get_authed_user(request, user_id, db)
    if user_obj.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA already enabled")
    return mfa_service.generate_setup(user_obj)


@auth_router.post("/mfa/{user_id}/enable", response_model=MFAEnableResponse)
def mfa_enable(user_id: int, body: MFAEnableRequest, request: Request, db: Session = Depends(get_db)):
    user_obj = _get_authed_user(request, user_id, db)
    try:
        backup_codes = mfa_service.enable_mfa(user_obj, body.secret, body.code, db)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return MFAEnableResponse(backup_codes=backup_codes)


@auth_router.post("/mfa/{user_id}/disable")
def mfa_disable(user_id: int, body: MFAVerifyRequest, request: Request, db: Session = Depends(get_db)):
    user_obj = _get_authed_user(request, user_id, db)
    if not user_obj.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA not enabled")
    if not mfa_service.verify_login(user_obj, body.code):
        raise HTTPException(status_code=400, detail="Invalid code")
    mfa_service.disable_mfa(user_obj, db)
    return {"message": "MFA disabled"}


@auth_router.post("/mfa/verify", response_model=user_schema.UserLoginResponse)
def mfa_verify(body: MFAVerifyRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """Second step of login when MFA is enabled. Expects mfa_pending cookie."""
    pending_sub = request.cookies.get("mfa_pending")
    if not pending_sub:
        raise HTTPException(status_code=401, detail="No pending MFA session")
    user_obj = user_service.get_user_by_id(int(pending_sub), db)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not mfa_service.verify_login(user_obj, body.code):
        raise HTTPException(status_code=400, detail="Invalid code")
    # Clear pending cookie, issue real auth cookies
    response.delete_cookie(key="mfa_pending", path="/")
    token_data = {"sub": str(user_obj.id), "is_superuser": user_obj.is_superuser}
    access_token = create_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), token_type="access")
    refresh_token = create_token(data=token_data, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), token_type="refresh")
    _set_auth_cookies(response, access_token, refresh_token)
    return user_schema.UserLoginResponse(user=user_obj, message="Login successful")