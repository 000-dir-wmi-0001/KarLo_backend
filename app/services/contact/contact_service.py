from sqlalchemy.orm import Session
from app.schemas import contact_schema
from app.repositories.contact import contact_repository


def create_contact(data: contact_schema.ContactCreate, db: Session):
    return contact_repository.create_contact(db, data)


def update_contact(id: int, data: contact_schema.ContactUpdate, db: Session):
    return contact_repository.update_contact(db, id, data)


def get_contact_by_id(id: int, db: Session):
    return contact_repository.get_contact_by_id(db, id)


def get_all_contacts(db: Session, skip: int = 0, limit: int = 100):
    return contact_repository.get_all_contacts(db, skip, limit)


def delete_contact(id: int, db: Session):
    return contact_repository.delete_contact(db, id)


def get_contact_by_email(email: str, db: Session):
    return contact_repository.get_by_email(db, email)
