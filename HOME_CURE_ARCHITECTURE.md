# Home Cure Architecture Diagram

## Application Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         Main FastAPI App                         │
│                         (app.main:app)                           │
│                                                                   │
│  ┌──────────────────┐      ┌──────────────────────────────┐    │
│  │  JWT Middleware   │      │     CORS Middleware          │    │
│  │                   │      │                              │    │
│  │  Protected:       │      │  Origins:                    │    │
│  │  - /api/v*        │      │  - localhost:3000/3001       │    │
│  │  - /home_cure/*   │      │  - vercel domains            │    │
│  └──────────────────┘      └──────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Route Mapping                            │ │
│  │                                                             │ │
│  │  /api/v1/*  →  KarLo API (api_router)                     │ │
│  │  /           →  Root endpoint                              │ │
│  │  /docs       →  Main Swagger UI                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │        Mounted Sub-Application: /home_cure                  │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │         Home Cure FastAPI App                         │ │ │
│  │  │      (app.home_cure.main:home_cure_app)              │ │ │
│  │  │                                                       │ │ │
│  │  │  Routes:                                             │ │ │
│  │  │  ├─ /auth/*      → Authentication                   │ │ │
│  │  │  ├─ /user/*      → User endpoints                   │ │ │
│  │  │  ├─ /admin/*     → Admin dashboard                  │ │ │
│  │  │  ├─ /            → Home Cure root                   │ │ │
│  │  │  └─ /docs        → Home Cure Swagger UI             │ │ │
│  │  │                                                       │ │ │
│  │  │  Public Paths (No Auth):                            │ │ │
│  │  │  ✓ /home_cure/auth/login                            │ │ │
│  │  │  ✓ /home_cure/auth/register                         │ │ │
│  │  │  ✓ /home_cure/auth/refresh-token                    │ │ │
│  │  │                                                       │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Home Cure Module Internal Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    app/home_cure/ Module                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  main.py                                                         │
│  ├─ create_home_cure_app() → Factory function                   │
│  └─ home_cure_app          → FastAPI instance                   │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   api/         │  │   models/      │  │   schemas/     │   │
│  │                │  │                │  │                │   │
│  │  Routes:       │  │  Database:     │  │  Validation:   │   │
│  │  • auth        │  │  • User        │  │  • UserCreate  │   │
│  │  • user        │  │  • Service     │  │  • UserUpdate  │   │
│  │  • admin       │  │  • Contact     │  │  • UserLogin   │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │ repositories/  │  │  services/     │  │   core/        │   │
│  │                │  │                │  │                │   │
│  │  Data Access:  │  │  Business:     │  │  Config:       │   │
│  │  • CRUDBase    │  │  • auth        │  │  • PUBLIC_PATHS│   │
│  │  • user repo   │  │  • user        │  │  • settings    │   │
│  │  • service repo│  │  • service     │  │                │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### Public Request (Login)
```
Client Request: POST /home_cure/auth/login
    ↓
Main App (JWT Middleware)
    ↓
Check: Is path in public_paths? → YES
    ↓
Skip authentication
    ↓
Route to mounted Home Cure app
    ↓
Home Cure auth_router
    ↓
auth_service.authenticate_user()
    ↓
user_repository (DB query)
    ↓
Return JWT tokens
```

### Protected Request (Update User)
```
Client Request: PATCH /home_cure/user/123/update
Header: Authorization: Bearer <token>
    ↓
Main App (JWT Middleware)
    ↓
Check: Is path in public_paths? → NO
Check: Path starts with /home_cure? → YES
    ↓
Verify JWT token
    ↓
Extract user from token → request.state.user
    ↓
Route to mounted Home Cure app
    ↓
Home Cure user_router
    ↓
user_service.update_user()
    ↓
user_repository (DB update)
    ↓
Return updated user
```

## Data Flow Layers

```
┌──────────────────────────────────────────────────┐
│  API Routes (FastAPI endpoints)                  │
│  - Handle HTTP requests                          │
│  - Validate input via Pydantic schemas           │
│  - Return HTTP responses                         │
└────────────────┬─────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────┐
│  Services (Business Logic)                       │
│  - Coordinate operations                         │
│  - Apply business rules                          │
│  - Call repositories                             │
└────────────────┬─────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────┐
│  Repositories (Data Access)                      │
│  - Database queries (CRUD)                       │
│  - Data transformation                           │
│  - Use SQLAlchemy ORM                            │
└────────────────┬─────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────┐
│  Models (SQLAlchemy ORM)                         │
│  - Define database schema                        │
│  - Relationships                                 │
│  - Constraints                                   │
└────────────────┬─────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────┐
│  Database (PostgreSQL/Neon)                      │
│  - Store data                                    │
│  - Execute queries                               │
│  - Maintain integrity                            │
└──────────────────────────────────────────────────┘
```

## Authentication Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ POST /home_cure/auth/register
       │ {email, password, name}
       ↓
┌─────────────────────────┐
│   auth_router.register  │
│   (Public - No Auth)    │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  user_service.create    │
│  - Hash password        │
│  - Validate data        │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  user_repository.create │
│  - Insert to DB         │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  Return User object     │
│  (without password)     │
└──────┬──────────────────┘
       │
       ↓
┌─────────────┐
│   Client    │
│ Receives:   │
│ {id, email, │
│  name, role}│
└─────────────┘

       │ POST /home_cure/auth/login
       │ {email, password}
       ↓
┌─────────────────────────┐
│   auth_router.login     │
│   (Public - No Auth)    │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────────┐
│  auth_service.authenticate  │
│  - Find user by email       │
│  - Verify password (bcrypt) │
└──────┬──────────────────────┘
       │
       ↓
┌─────────────────────────┐
│  Generate JWT tokens    │
│  - access_token         │
│  - refresh_token        │
└──────┬──────────────────┘
       │
       ↓
┌─────────────┐
│   Client    │
│ Receives:   │
│ {access_    │
│  token,     │
│  refresh_   │
│  token}     │
└─────────────┘

       │ PATCH /home_cure/user/123/update
       │ Header: Authorization: Bearer <access_token>
       ↓
┌──────────────────────┐
│  JWT Middleware      │
│  - Verify token      │
│  - Extract payload   │
│  - Set request.state │
└──────┬───────────────┘
       │ ✓ Authenticated
       ↓
┌─────────────────────────┐
│  user_router.update     │
│  (Protected - Has Auth) │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  user_service.update    │
│  - Validate changes     │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  user_repository.update │
│  - Update in DB         │
└──────┬──────────────────┘
       │
       ↓
┌─────────────┐
│   Client    │
│ Receives:   │
│ Updated user│
└─────────────┘
```

## Database Architecture

```
┌───────────────────────────────────────┐
│         PostgreSQL (Neon DB)          │
├───────────────────────────────────────┤
│                                       │
│  Tables (Alembic migrations):        │
│                                       │
│  ┌─────────────────┐                │
│  │ home_cure_user  │                │
│  ├─────────────────┤                │
│  │ • id (PK)       │                │
│  │ • email         │                │
│  │ • password_hash │                │
│  │ • name          │                │
│  │ • role          │                │
│  │ • phone         │                │
│  │ • address       │                │
│  │ • geo_location  │                │
│  │ • created_at    │                │
│  │ • updated_at    │                │
│  └─────────────────┘                │
│                                       │
│  ┌─────────────────┐                │
│  │ home_cure_service│               │
│  ├─────────────────┤                │
│  │ • id (PK)       │                │
│  │ • title         │                │
│  │ • description   │                │
│  │ • price         │                │
│  │ • duration      │                │
│  │ • created_at    │                │
│  └─────────────────┘                │
│                                       │
│  ┌─────────────────┐                │
│  │ home_cure_contact│               │
│  ├─────────────────┤                │
│  │ • id (PK)       │                │
│  │ • name          │                │
│  │ • email         │                │
│  │ • message       │                │
│  │ • created_at    │                │
│  └─────────────────┘                │
│                                       │
│  Future tables:                      │
│  • technician                        │
│  • booking (with QR code)            │
│  • health_record                     │
│  • technician_earnings               │
│  • admin_log                         │
│  • system_settings                   │
│                                       │
└───────────────────────────────────────┘
```

## Key Benefits of This Architecture

### 1. Separation of Concerns
- Main app handles routing and middleware
- Home Cure module is independent
- Clear boundaries between concerns

### 2. Scalability
- Easy to add more modules
- Can scale home_cure independently
- Module-specific configuration

### 3. Security
- Centralized JWT authentication
- Clear public/protected paths
- Request state management

### 4. Maintainability
- Each layer has single responsibility
- Easy to test individual components
- Clear data flow

### 5. Documentation
- Separate API docs per module
- Self-documenting structure
- Clear README files

---

**Architecture Status:** ✅ Implemented and Working
**Next Phase:** Healthcare Models Implementation
