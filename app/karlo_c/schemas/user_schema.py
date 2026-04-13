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
    agreed_to_terms: Optional[bool] = False
    newsletter_opt_in: Optional[bool] = False


# ---------- Create ----------
class UserCreate(UserBase):
    full_name: str
    email: EmailStr
    password: str   # plain password for request
    agreed_to_terms: bool
    newsletter_opt_in: bool


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
    message: str = "Login successful"
    user: UserResponse


# ---------- Login Request ----------
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


# ---------- Password Update Request ----------
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


# ---------- MFA Schemas ----------
class MFASetupResponse(BaseModel):
    secret: str
    uri: str
    qr_svg: str

class MFAEnableRequest(BaseModel):
    secret: str
    code: str

class MFAEnableResponse(BaseModel):
    backup_codes: list[str]

class MFAVerifyRequest(BaseModel):
    code: str

class MFAStatusResponse(BaseModel):
    mfa_enabled: bool
    mfa_enabled_at: Optional[datetime] = None
