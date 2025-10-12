# Home Cure Quick Reference

## 🚀 Quick Start

### Start the Server
```bash
# Activate virtual environment (if not active)
d:\Al-Ansar\KarLo_backend\env\Scripts\activate

# Start server
uvicorn app.main:app --reload --port 8000
```

### Access Documentation
- **Main API Docs**: http://localhost:8000/docs
- **Home Cure Docs**: http://localhost:8000/home_cure/docs
- **ReDoc**: http://localhost:8000/home_cure/redoc

## 📁 File Locations

### Need to add a new route?
→ `app/home_cure/api/routes/{admin|user}/`

### Need to add business logic?
→ `app/home_cure/services/`

### Need to add a database model?
→ `app/home_cure/models/`

### Need to add validation schema?
→ `app/home_cure/schemas/`

### Need to add database queries?
→ `app/home_cure/repositories/`

### Need to change configuration?
→ `app/home_cure/core/config.py`

## 🔐 Authentication

### Public Endpoints (No token needed)
```
POST /home_cure/auth/register
POST /home_cure/auth/login
POST /home_cure/auth/refresh-token
GET  /home_cure/auth/test
```

### Protected Endpoints (Token required)
```
PATCH /home_cure/user/{user_id}/update
GET   /home_cure/admin/users
GET   /home_cure/admin/services
... (all other endpoints)
```

### How to make a request with authentication
```bash
# 1. Login first
curl -X POST http://localhost:8000/home_cure/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Response: {"access_token": "eyJ...", "refresh_token": "eyJ..."}

# 2. Use the access_token in subsequent requests
curl -X PATCH http://localhost:8000/home_cure/user/1/update \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name"}'
```

## 🗄️ Database

### Run migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Check migration status
alembic current

# Rollback migration
alembic downgrade -1
```

### Access database
- **Type**: PostgreSQL (Neon)
- **Connection**: Configured in `.env` or `app/core/config.py`

## 📝 Common Tasks

### Add a new endpoint

1. **Create route file** (if needed)
   ```python
   # app/home_cure/api/routes/user/new_route.py
   from fastapi import APIRouter
   
   router = APIRouter(prefix="/feature", tags=["Feature"])
   
   @router.get("/")
   def get_features():
       return {"message": "Features"}
   ```

2. **Add to router**
   ```python
   # app/home_cure/api/routes/user/user.py
   from .new_route import router as new_router
   
   api_user_router.include_router(new_router)
   ```

### Add a new model

1. **Create model file**
   ```python
   # app/home_cure/models/new_model.py
   from sqlalchemy import Column, Integer, String
   from app.db.base import Base
   
   class NewModel(Base):
       __tablename__ = "home_cure_new_model"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, nullable=False)
   ```

2. **Import in base.py** (if needed)
   ```python
   # app/db/base.py
   from app.home_cure.models.new_model import NewModel
   ```

3. **Create migration**
   ```bash
   alembic revision --autogenerate -m "add new_model"
   alembic upgrade head
   ```

### Add a new service

1. **Create service file**
   ```python
   # app/home_cure/services/new_service.py
   from sqlalchemy.orm import Session
   
   def do_something(data, db: Session):
       # Business logic here
       return result
   ```

2. **Use in route**
   ```python
   from app.home_cure.services import new_service
   
   @router.post("/action")
   def perform_action(data: Schema, db: Session = Depends(get_db)):
       return new_service.do_something(data, db)
   ```

## 🐛 Debugging

### Check logs
Server logs will show in the terminal where you ran `uvicorn`

### Test imports
```bash
python -c "from app.home_cure import home_cure_app; print('OK')"
```

### Check route registration
```bash
# Server startup logs show all registered routes
# Look for [ROUTE] lines
```

### Verify database connection
```bash
python -c "from app.db.session import engine; print(engine.url)"
```

## 🧪 Testing

### Test authentication
```python
# Test login
response = client.post("/home_cure/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
assert response.status_code == 200
token = response.json()["access_token"]

# Test protected endpoint
response = client.get(
    "/home_cure/user/1/update",
    headers={"Authorization": f"Bearer {token}"}
)
```

## 🔧 Configuration

### Add a public path
```python
# app/home_cure/core/config.py
HOME_CURE_PUBLIC_PATHS: List[str] = [
    "/home_cure/auth/login",
    "/home_cure/auth/register",
    "/home_cure/new-public-endpoint",  # Add here
]
```

### Change CORS settings
```python
# app/home_cure/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.com",  # Add here
    ],
    ...
)
```

## 📊 Current Structure

```
Main App (/api/v1/*)
├── KarLo API (original)
└── Home Cure (/home_cure/*)
    ├── Auth routes (/auth/*)
    ├── User routes (/user/*)
    └── Admin routes (/admin/*)
```

## ✅ Status

- [x] Module reorganization complete
- [x] JWT authentication working
- [x] All routes accessible
- [x] Database migrations working
- [ ] Healthcare models (next)
- [ ] QR code system (next)
- [ ] Booking management (next)

## 📚 Documentation

- **Module README**: `app/home_cure/README.md`
- **Architecture**: `HOME_CURE_ARCHITECTURE.md`
- **Reorganization**: `HOME_CURE_REORGANIZATION.md`
- **Implementation Status**: `IMPLEMENTATION_STATUS.md`

## 🆘 Common Issues

### Import Error
- Check `__init__.py` files exist
- Verify imports use absolute paths: `from app.home_cure...`

### Authentication Error
- Check token is valid (not expired)
- Verify endpoint is in protected_prefixes
- Check if path should be in public_paths

### Migration Error
- Verify database connection
- Check alembic.ini configuration
- Review migration file for syntax

### Route Not Found
- Check prefix in router definition
- Verify router is included in main router
- Check server logs for registered routes

---

**Last Updated**: October 12, 2025
**Status**: ✅ Ready for development
