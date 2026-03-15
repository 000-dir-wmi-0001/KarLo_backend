from sqlalchemy.orm import Session
from app.karlo_c.models.task_model import Task
from app.karlo_c.schemas.task_schema import TaskCreate, TaskUpdate
from app.karlo_c.repositories.crud import CRUDBase

crud_task = CRUDBase(Task)


def create_task(db: Session, payload: dict):
    return crud_task.create(db, payload)


def get_task_by_id(db: Session, task_id: int):
    return crud_task.get_by_id(db, task_id)


def get_tasks_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_active_location_tasks_by_user_id(db: Session, user_id: int):
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .filter(Task.is_completed.is_(False))
        .filter(Task.remind_on_arrival.is_(True))
        .filter(Task.latitude.isnot(None))
        .filter(Task.longitude.isnot(None))
        .all()
    )


def update_task(db: Session, task_id: int, data: TaskUpdate):
    db_obj = crud_task.get_by_id(db, task_id)
    if not db_obj:
        return None
    return crud_task.update(db, db_obj, data)


def delete_task(db: Session, task_id: int):
    db_obj = crud_task.get_by_id(db, task_id)
    if not db_obj:
        return None
    return crud_task.delete(db, db_obj)
