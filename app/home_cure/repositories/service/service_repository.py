from sqlalchemy.orm import Session
from app.home_cure.models.service_model import Service
from app.home_cure.schemas.service_schema import ServiceCreate, ServiceUpdate
from app.karlo_c.repositories.crud import CRUDBase


crud_service = CRUDBase(Service)


def create_service(db: Session, data: ServiceCreate):
    return crud_service.create(db, data)


def update_service(db: Session, id: int, data: ServiceUpdate):
    db_obj = crud_service.get_by_id(db, id)
    if not db_obj:
        return None
    return crud_service.update(db, db_obj, data)


def get_service_by_id(db: Session, id: int):
    return crud_service.get_by_id(db, id)


def get_all_services(db: Session, skip: int = 0, limit: int = 100):
    return crud_service.get_all(db, skip, limit)


def delete_service(db: Session, id: int):
    db_obj = crud_service.get_by_id(db, id)
    if not db_obj:
        return None
    return crud_service.delete(db, db_obj)
