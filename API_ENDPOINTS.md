# KarLo API Endpoints

Base URL: <http://localhost:8000>

Base prefix: /api/v1

## Public Endpoints

### Auth

- POST /auth/register
- POST /auth/login
- POST /auth/refresh-token
- POST /auth/logout

### Contact

- POST /contact/create

### Contribute

- POST /contribute/create

### User Registration

- POST /user/create

## Protected Endpoints

### Auth Session

- GET /auth/me
- PUT /auth/update-password/{user_id}

### User Management

- GET /user/{id}
- GET /user/
- PUT /user/update/{id}
- DELETE /user/delete/{id}

### Contact (admin-only for non-create operations)

- GET /contact/{id}
- GET /contact/
- PUT /contact/update/{id}
- DELETE /contact/delete/{id}
- GET /contact/email/{email}

### Contribute (admin-only for non-create operations)

- GET /contribute/{id}
- GET /contribute/
- PUT /contribute/update/{id}
- DELETE /contribute/delete/{id}
- GET /contribute/email/{email}
- GET /contribute/country/{country}

### Task

- POST /task/create
- GET /task/
- GET /task/{task_id}
- PUT /task/update/{task_id}
- DELETE /task/delete/{task_id}
- POST /task/check-geofence

### Geocode

- GET /geocode/search?q={query}
- POST /geocode/reverse

## Health and Docs

- GET /
- GET /docs
- GET /redoc
- GET /openapi.json
