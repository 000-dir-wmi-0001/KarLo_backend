# KarLo Backend (FastAPI)

Core backend for KarLo with cookie-based auth and modular APIs.

## Tech Stack
- FastAPI + Starlette
- SQLAlchemy + Alembic
- Pydantic v2
- JWT auth via HttpOnly cookies

## Python Version Strategy
- Recommended: Python 3.11 or 3.14
- Supported: Python 3.11, 3.12, 3.13, 3.14

Use this on Windows:
```cmd
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Environment
Create `.env` from `.env.example`.

Important values:
- `DATABASE_URL` (defaults to SQLite fallback if omitted)
- `SECRET_KEY`
- `ORIGIN_URL`
- `COOKIE_SECURE`, `COOKIE_SAMESITE`, `COOKIE_DOMAIN`

Email delivery is not used in the current backend runtime.

## Run
```cmd
uvicorn app.main:app --reload
```

- API root: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Modules (v1)
Base prefix: `/api/v1`

- Auth: `/auth/*`
- User: `/user/*`
- Contact: `/contact/*`
- Contribute: `/contribute/*`
- Task (location reminder MVP): `/task/*`

Task endpoints:
- `POST /task/create`
- `GET /task/`
- `GET /task/{task_id}`
- `PUT /task/update/{task_id}`
- `DELETE /task/delete/{task_id}`

## Auth Model
- Login sets `access_token` and `refresh_token` cookies
- Middleware validates access token for private routes
- Backend rotates tokens using refresh cookie when needed
- Frontend calls backend through same-origin Next rewrite (`/api/*`)

## Migrations
```cmd
alembic upgrade head
```

## Tests
```cmd
.venv\Scripts\python.exe -m pytest
```

Backend API tests cover authentication, task geofence checks, authorization boundaries, and Home Cure admin protection.

## Docker
```cmd
docker build -t karlo-backend .
docker run --rm -p 8000:8000 --env-file .env karlo-backend
```

## Notes
- Home Cure module is mounted at `/home_cure` and has separate routes.
- For local development, SQLite fallback works when `DATABASE_URL` is missing.
