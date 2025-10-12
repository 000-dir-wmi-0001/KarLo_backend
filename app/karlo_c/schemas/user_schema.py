from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Base Schema ----------
class UserBase(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None
    role: Optional[str] = "user"
    geo_location: Optional[str] = None


# ---------- Create ----------
class UserCreate(UserBase):
    full_name: str
    email: EmailStr
    password: str   # plain password for request


# ---------- Update ----------
class UserUpdate(UserBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # allow updating password


# ---------- Response ----------
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool
    is_deleted: bool
    last_login: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- List Response ----------
class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Delete Response ----------
class UserDeleteResponse(BaseModel):
    success: bool
    message: str
    


# ---------- Create Response ----------
class CreateUserResponse(BaseModel):
    data: UserResponse
    message: str


# ---------- Login Response ----------
class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None  # include if you issue refresh tokens
    token_type: str = "bearer"
    expires_in: int                      # seconds until access token expires
    user: UserResponse


# ---------- Login Request ----------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------- Password Update Request ----------
class PasswordUpdate(BaseModel):
    new_password: str
