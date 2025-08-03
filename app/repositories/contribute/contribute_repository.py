from sqlalchemy.orm import Session
from app.models.contribute_model import Contribute
from app.schemas.contribute_schema import ContributeCreate
from app.repositories.crud import CRUDBase

crud_contribute = CRUDBase(Contribute)

def create_contribute(db: Session, data: ContributeCreate):
    return crud_contribute.create(db, data)

def update_contribute(db: Session, id: int, data: ContributeCreate):
    db_obj = crud_contribute.get_by_id(db, id)
    if not db_obj:
        return None
    return crud_contribute.update(db, db_obj, data)

def get_contribute_by_id(db: Session, id: int):
    return crud_contribute.get_by_id(db, id)

def get_all_contributes(db: Session, skip: int = 0, limit: int = 100):
    return crud_contribute.get_all(db, skip, limit)

def delete_contribute(db: Session, id: int):
    db_obj = crud_contribute.get_by_id(db, id)
    if not db_obj:
        return None
    return crud_contribute.delete(db, db_obj)

def get_by_email(db: Session, email: str):
    return db.query(Contribute).filter(Contribute.email == email).first()

def get_by_country(db: Session, country: str):
    return db.query(Contribute).filter(Contribute.country == country).all() 