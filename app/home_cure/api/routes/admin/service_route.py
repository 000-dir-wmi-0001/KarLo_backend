from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.home_cure.schemas.service_schema import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
    ServiceListResponse,
    ServiceDeleteResponse,
)
from app.home_cure.services import service_service
from app.db.session import get_db

service_router = APIRouter(prefix="/service", tags=["Services"])


@service_router.post("/create", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new = service_service.create_service(service, db)
    return new


@service_router.put("/update/{id}", response_model=ServiceResponse)
def update_service(id: int, service: ServiceUpdate, db: Session = Depends(get_db)):
    result = service_service.update_service(id, service, db)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result


@service_router.get("/{id}", response_model=ServiceResponse)
def get_service(id: int, db: Session = Depends(get_db)):
    result = service_service.get_service_by_id(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result


@service_router.get("/", response_model=ServiceListResponse)
def get_all_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = service_service.get_all_services(db, skip, limit)
    return {"services": services, "total": len(services)}


@service_router.delete("/delete/{id}", response_model=ServiceDeleteResponse)
def delete_service(id: int, db: Session = Depends(get_db)):
    result = service_service.delete_service(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"success": True, "message": f"Service with ID {id} deleted successfully"}