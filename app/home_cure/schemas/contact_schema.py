from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    message: str
    model_config = ConfigDict(from_attributes=True)

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ContactListResponse(BaseModel):
    contacts: list[ContactResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)

class ContactDeleteResponse(BaseModel):
    success: bool
    message: str

class CreateContactResponse(BaseModel):
    data: ContactResponse
    message: str
