from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class ServiceBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ServiceCreate(ServiceBase):
    name: str


class ServiceUpdate(ServiceBase):
    name: Optional[str] = None


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceListResponse(BaseModel):
    services: List[ServiceResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)


class ServiceDeleteResponse(BaseModel):
    success: bool
    message: str


class CreateServiceResponse(BaseModel):
    data: ServiceResponse
    message: str
