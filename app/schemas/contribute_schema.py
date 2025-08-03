from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class ContributeCreate(BaseModel):
    first_name: str
    last_name: str
    gitHub_link: str
    linkedIn_link: str
    country: str
    state: str
    city: str
    zip_code: str
    email: EmailStr

class ContributeResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class ContributeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gitHub_link: Optional[str] = None
    linkedIn_link: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)

class ContributeListResponse(BaseModel):
    contributions: list[ContributeResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)

class ContributeDeleteResponse(BaseModel):
    success: bool
    message: str

    model_config = ConfigDict(from_attributes=True)

class CreateContributeResponse(BaseModel):
    data: ContributeResponse
    message: str
