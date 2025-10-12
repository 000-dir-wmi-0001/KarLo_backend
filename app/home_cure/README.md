# Home Cure Module

Healthcare platform for booking technicians and managing health services.

## Overview

The Home Cure module is a standalone FastAPI application that provides:
- User authentication and authorization
- Healthcare service management
- Booking system for technicians
- Admin dashboard for management
- User health records

## Structure

```
home_cure/
├── __init__.py                 # Module initialization
├── main.py                     # FastAPI app factory
├── api/                        # API routes
│   ├── __init__.py
│   ├── home_cure_route.py     # Main router
│   └── routes/
│       ├── auth_route.py      # Authentication endpoints
│       ├── admin/             # Admin routes
│       │   ├── admin.py
│       │   ├── user_route.py
│       │   ├── service_route.py
│       │   └── contact_route.py
│       └── user/              # User routes
│           ├── user.py
│           ├── services_route.py
│           └── contact_route.py
├── core/                       # Configuration
│   ├── __init__.py
│   └── config.py              # Home Cure specific settings
├── models/                     # Database models
│   ├── user_model.py
│   ├── service_model.py
│   └── contact_model.py
├── schemas/                    # Pydantic schemas
│   ├── user_schema.py
│   ├── service_schema.py
│   └── contact_schema.py
├── repositories/               # Data access layer
│   ├── crud.py                # Base CRUD operations
│   ├── user/
│   │   └── user_repository.py
│   └── service/
│       └── service_repository.py
└── services/                   # Business logic
    ├── auth_service.py
    ├── user_service.py
    ├── service_service.py
    └── contact_service.py
```

## API Endpoints

### Base URL
All Home Cure endpoints are prefixed with `/home_cure`

### Authentication
- `POST /home_cure/auth/register` - Register new user
- `POST /home_cure/auth/login` - Login user
- `POST /home_cure/auth/refresh-token` - Refresh access token
- `GET /home_cure/auth/test` - Test endpoint (public)

### User Routes
- `GET /home_cure/user/services` - Get available services
- `POST /home_cure/user/contact` - Submit contact form
- `PATCH /home_cure/user/{user_id}/update` - Update user profile

### Admin Routes
- `GET /home_cure/admin/users` - List all users
- `GET /home_cure/admin/services` - List all services
- `GET /home_cure/admin/contacts` - List contact submissions

## Authentication

The module uses JWT-based authentication. Protected routes require a Bearer token in the Authorization header:

```
Authorization: Bearer <token>
```

### Public Paths (No authentication required)
- `/home_cure/auth/login`
- `/home_cure/auth/register`
- `/home_cure/auth/refresh-token`
- `/home_cure/auth/test`
- `/home_cure/` (root)
- `/home_cure/docs` (API documentation)

## Running the Module

The Home Cure module is automatically mounted on the main FastAPI app at `/home_cure`.

Start the server:
```bash
uvicorn app.main:app --reload
```

Access the API documentation:
- Swagger UI: http://localhost:8000/home_cure/docs
- ReDoc: http://localhost:8000/home_cure/redoc

## Database

The module uses SQLAlchemy models and shares the database session with the main application.

Models are located in `app/home_cure/models/` and migrations are managed through Alembic.

## Development

### Adding New Routes

1. Create route file in `app/home_cure/api/routes/`
2. Create corresponding service in `app/home_cure/services/`
3. Create schema in `app/home_cure/schemas/`
4. Add route to appropriate router in `home_cure_route.py`

### Creating New Models

1. Add model in `app/home_cure/models/`
2. Create Alembic migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

## Future Enhancements

- [ ] Booking system with QR codes
- [ ] Technician management
- [ ] Health records
- [ ] Payment integration
- [ ] Notification system
- [ ] Real-time updates
