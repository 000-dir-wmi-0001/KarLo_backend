from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.db.base import Base
from app.db.session import engine
from app.karlo_c.api.api import api_router
from app.core.config import settings
from app.middleware.jwt_middleware import JWTMiddleware
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
from app.home_cure import home_cure_app
from app.home_cure.core.config import HOME_CURE_PUBLIC_PATHS

public_paths = [
    # Public API endpoints (include full routed path with /api prefix)
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/api/v1/auth/refresh-token",
    "/api/v1/contact/create",
    "/api/v1/contribute/create",
    "/api/v1/user/create",
    # Docs (keep public)
    "/docs",
    "/redoc",
    "/openapi.json",
] + HOME_CURE_PUBLIC_PATHS  # Add home_cure public paths


# Create tables only in dev or when using SQLite (avoid on remote DBs)
# Disabled: Using Alembic for database migrations instead
# from urllib.parse import urlparse
# is_sqlite = urlparse(settings.DATABASE_URL or "sqlite:///./karlo.db").scheme.startswith("sqlite")
# if settings.DEBUG or is_sqlite:
#     Base.metadata.create_all(bind=engine)


# Lifespan handler replaces deprecated on_event hooks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: log route response_class to catch misconfigurations breaking OpenAPI
    try:
        for route in app.routes:
            if isinstance(route, APIRoute):
                rc = route.response_class
                rc_name = getattr(rc, "__name__", str(rc))
                print(f"[ROUTE] {route.path} -> response_class={rc_name}")
    except Exception as e:
        print("[ROUTE-LOG] error:", e)
    yield
    # Shutdown: place any cleanup here if needed

app = FastAPI(
    title="KarLo API",
    description="FastAPI backend for KarLo data.",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://momin-mohasin.vercel.app",
        "https://kar-lo.vercel.app",
        "http://localhost:3001",
        "https://home-cure-frontend.vercel.app",
    ],
    # allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    JWTMiddleware,
    # Protect all versioned API routes (v1, v2, ...) under the /api prefix and /home_cure
    protected_prefix="/api/v",
    protected_prefixes=["/api/v", "/home_cure"],
    public_paths=public_paths
)


# Register API routes
app.include_router(api_router)

# Mount the Home Cure app as a sub-application
app.mount("/home_cure", home_cure_app)

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

# (Lifespan used instead of deprecated on_event hooks)

# Customize OpenAPI to include Bearer auth and mark protected routes
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Define Bearer security scheme
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    # Apply security to protected API routes (/api/v...) except the explicit public ones
    paths = openapi_schema.get("paths", {})
    for path, methods in paths.items():
        is_api_versioned = path.startswith("/api/v")
        is_public = path in public_paths
        if not is_api_versioned or is_public:
            continue
        for method, op in methods.items():
            if not isinstance(op, dict):
                continue
            # Attach Bearer requirement
            op["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
