from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.home_cure.schemas.service_schema import (
    ServiceCreate,
    ServiceResponse,
    ServiceListResponse,
)
from app.home_cure.services import service_service
from app.db.session import get_db

services_router = APIRouter(prefix="/services", tags=["Services"])


@services_router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new = service_service.create_service(service, db)
    return new


@services_router.get("/{id}", response_model=ServiceResponse)
def get_service(id: int, db: Session = Depends(get_db)):
    result = service_service.get_service_by_id(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result


@services_router.get("/", response_model=ServiceListResponse)
def get_all_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = service_service.get_all_services(db, skip, limit)
    return {"services": services, "total": len(services)}