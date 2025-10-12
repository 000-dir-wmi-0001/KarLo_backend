from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from app.utils.token.jwt import verify_token



class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_prefix: str = "/v1", public_paths: list = None, protected_prefixes: list = None):
        super().__init__(app)
        self.protected_prefix = protected_prefix
        self.protected_prefixes = protected_prefixes or [protected_prefix]
        self.public_paths = public_paths or []

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip public paths
        if path in self.public_paths:
            return await call_next(request)

        # Check if path matches any protected prefix
        is_protected = any(path.startswith(prefix) for prefix in self.protected_prefixes)
        
        # Only protect routes under the protected prefixes
        if is_protected:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "Missing token"},
                )

            token = auth_header.split(" ")[1]
            payload = verify_token(token)
            if not payload:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or expired token"},
                )

            # Optionally attach payload to request.state for routes to access
            request.state.user = payload

        response = await call_next(request)
        return response
