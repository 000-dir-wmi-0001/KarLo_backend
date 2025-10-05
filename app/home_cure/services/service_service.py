from sqlalchemy.orm import Session
from app.home_cure.schemas.service_schema import ServiceCreate, ServiceUpdate
from app.home_cure.repositories.service import service_repository


def create_service(data: ServiceCreate, db: Session):
    return service_repository.create_service(db, data)


def update_service(id: int, data: ServiceUpdate, db: Session):
    return service_repository.update_service(db, id, data)


def get_service_by_id(id: int, db: Session):
    return service_repository.get_service_by_id(db, id)


def get_all_services(db: Session, skip: int = 0, limit: int = 100):
    return service_repository.get_all_services(db, skip, limit)


def delete_service(id: int, db: Session):
    return service_repository.delete_service(db, id)
