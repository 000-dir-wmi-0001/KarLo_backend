from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from app.utils.token.jwt import verify_token, create_access_token, create_refresh_token
from app.core.config import settings



class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_prefix: str = "/v1", public_paths: list = None, protected_prefixes: list = None):
        super().__init__(app)
        self.protected_prefix = protected_prefix
        self.protected_prefixes = protected_prefixes or [protected_prefix]
        self.public_paths = public_paths or []

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        rotate_tokens: tuple[str, str] | None = None

        # Skip public paths (strip trailing slash for comparison so both /path and /path/ match)
        if path.rstrip("/") in [p.rstrip("/") for p in self.public_paths]:
            return await call_next(request)

        # Allow CORS preflight requests to pass through without auth checks
        if request.method == "OPTIONS":
            return await call_next(request)

        # Check if path matches any protected prefix
        is_protected = any(path.startswith(prefix) for prefix in self.protected_prefixes)
        
        # Only protect routes under the protected prefixes
        if is_protected:
            token = request.cookies.get("access_token")
            if not token:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

            payload = verify_token(token) if token else None

            if not payload:
                refresh_token = request.cookies.get("refresh_token")
                refresh_payload = verify_token(refresh_token, expected_type="refresh") if refresh_token else None

                if not refresh_payload:
                    detail = "Missing token" if not token and not refresh_token else "Invalid or expired token"
                    return JSONResponse(
                        status_code=HTTP_401_UNAUTHORIZED,
                        content={"detail": detail},
                    )

                sub = refresh_payload.get("sub")
                if not sub:
                    return JSONResponse(
                        status_code=HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid token payload"},
                    )

                # Backend-managed rotation using refresh cookie only.
                payload = {"sub": str(sub), "type": "access"}
                rotate_tokens = (
                    create_access_token({"sub": str(sub)}),
                    create_refresh_token({"sub": str(sub)}),
                )

            request.state.user = payload

        response = await call_next(request)

        if is_protected:
            if rotate_tokens:
                access_token, refresh_token = rotate_tokens
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

        return response
