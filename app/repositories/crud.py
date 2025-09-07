# app/repositories/crud.py

from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, Any
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: SchemaType) -> ModelType:
        obj_data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in.dict()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, id: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: ModelType, obj_in: SchemaType | dict[str, Any]) -> ModelType:
        # Accept both Pydantic model and plain dict
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in.dict(exclude_unset=True)
        else:
            update_data = obj_in
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj_or_id) -> bool:
        # Accept either a model instance or an ID
        if isinstance(obj_or_id, self.model):
            obj = obj_or_id
        else:
            obj = self.get_by_id(db, obj_or_id)
            if not obj:
                return False
        db.delete(obj)
        db.commit()
        return True
    
    def get_by_email(self, db: Session, email: str) -> ModelType | None:
        try:
            return db.query(self.model).filter(self.model.email == email).one()
        except NoResultFound:
            return None
        
    def get_by_country(self, db: Session, country: str) -> list[ModelType]:
        return db.query(self.model).filter(self.model.country == country).all()
