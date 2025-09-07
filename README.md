# KarLo_backend

FastAPI backend for KarLo. It provides REST APIs for contact and contribute modules, SQLAlchemy models with optional Alembic migrations, and SMTP email via fastapi-mail.

## Tech stack
- FastAPI, Starlette, Uvicorn
- SQLAlchemy, Alembic
- Pydantic v2
- Email: fastapi-mail (SMTP)

## Requirements
- Python 3.11+ (Windows)
- Optional: PostgreSQL (project also supports SQLite by default)

## Setup (Windows cmd)
If you see an existing `env` folder, activate it; otherwise create a new one.

Activate existing env (if present):
```cmd
env\Scripts\activate
```

Or create and activate a new venv:
```cmd
py -3 -m venv .venv
.venv\Scripts\activate
```

Install dependencies:
```cmd
pip install -r requirements.txt
```

Create a `.env` file in the project root (example):
```ini
# Security
SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database (choose one)
# DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/karlo
# or SQLite fallback (used automatically if DATABASE_URL is not set):
# DATABASE_URL=sqlite:///./karlo.db

# Email (Gmail STARTTLS recommended)
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your@gmail.com
MAIL_FROM_NAME=KarLo
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
MAIL_USE_CREDENTIALS=true
MAIL_VALIDATE_CERTS=true
MAIL_SUPPRESS_SEND=false
```

## Run
```cmd
uvicorn app.main:app --reload

## Deployment Run
```cmd
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

- App: http://127.0.0.1:8000/
- Docs (Swagger): http://127.0.0.1:8000/docs
- Docs (ReDoc): http://127.0.0.1:8000/redoc

## API overview
All routes are served under the prefix: `/api/v1`

Contact
- POST `/contact/create`
- GET `/contact/`
- GET `/contact/{id}`
- GET `/contact/email/{email}`
- PUT `/contact/update/{id}`
- DELETE `/contact/delete/{id}`

Contribute
- POST `/contribute/create`
- GET `/contribute/`
- GET `/contribute/{id}`
- GET `/contribute/email/{email}`
- GET `/contribute/country/{country}`
- PUT `/contribute/update/{id}`
- DELETE `/contribute/delete/{id}`

Use Swagger UI to try these endpoints easily.

## Database and migrations
- By default, if `DATABASE_URL` is not set, the app uses SQLite at `./karlo.db`.
- For production, prefer Postgres and manage schema changes with Alembic:
```cmd
alembic upgrade head
```

## Project structure (high level)
- `app/main.py` — FastAPI application entry
- `app/api/` — Routers (`/api/v1/contact`, `/api/v1/contribute`)
- `app/models/` — SQLAlchemy models
- `app/schemas/` — Pydantic models
- `app/repositories/` — CRUD layer
- `app/services/` — Business logic
- `app/db/` — DB base and session
- `app/utils/mail/` — Email utilities (config + sender + dispatcher)

## Troubleshooting
- SMTP (Gmail): use an App Password (requires 2FA). For SSL use port 465 with `MAIL_SSL_TLS=true` and `MAIL_STARTTLS=false`.
- CORS: add your frontend URL to `CORS_ORIGINS` (comma-separated).
- DB: verify `DATABASE_URL`; for SQLite ensure the folder is writable.
