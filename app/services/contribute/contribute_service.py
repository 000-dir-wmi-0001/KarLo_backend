from sqlalchemy.orm import Session
from app.schemas import contribute_schema
from app.repositories.contribute import contribute_repository


def create_contribution(data: contribute_schema.ContributeCreate, db: Session):
    return contribute_repository.create_contribute(db, data)


def update_contribution(id: int, data: contribute_schema.ContributeUpdate, db: Session):
    return contribute_repository.update_contribute(db, id, data)


def get_contribution_by_id(id: int, db: Session):
    return contribute_repository.get_contribute_by_id(db, id)


def get_all_contributions(db: Session, skip: int = 0, limit: int = 100):
    return contribute_repository.get_all_contributes(db, skip, limit)


def delete_contribution(id: int, db: Session):
    return contribute_repository.delete_contribute(db, id)


def get_contribution_by_email(email: str, db: Session):
    return contribute_repository.get_by_email(db, email)


def get_contributions_by_country(country: str, db: Session):
    return contribute_repository.get_by_country(db, country)
