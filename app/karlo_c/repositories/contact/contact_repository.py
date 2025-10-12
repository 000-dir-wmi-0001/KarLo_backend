from sqlalchemy.orm import Session
from app.karlo_c.models.contact_model import Contact
from app.karlo_c.schemas.contact_schema import ContactCreate, ContactUpdate
from app.karlo_c.repositories.crud import CRUDBase

crud_contact = CRUDBase(Contact)

def create_contact(db: Session, data: ContactCreate):
    return crud_contact.create(db, data)

def update_contact(db: Session, id: int, data: ContactUpdate):
    db_obj = crud_contact.get_by_id(db, id)
    if not db_obj:
        return None
    return crud_contact.update(db, db_obj, data)

def get_contact_by_id(db: Session, id: int):
    return crud_contact.get_by_id(db, id)

def get_all_contacts(db: Session, skip: int = 0, limit: int = 100):
    return crud_contact.get_all(db, skip, limit)

def delete_contact(db: Session, id: int):
    db_obj = crud_contact.get_by_id(db, id)
    if not db_obj:
        return None
    # CRUD delete now accepts either id or model instance
    return crud_contact.delete(db, db_obj)

def get_by_email(db: Session, email: str):
    return db.query(Contact).filter(Contact.email == email).first()