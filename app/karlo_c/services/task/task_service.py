from sqlalchemy.orm import Session
from app.karlo_c.schemas import task_schema
from app.karlo_c.repositories.task import task_repository
from datetime import datetime, timedelta, timezone
import math


def _haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius_m = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius_m * c


def create_task(data: task_schema.TaskCreate, user_id: int, db: Session):
    payload = data.model_dump()
    payload["user_id"] = user_id
    return task_repository.create_task(db, payload)


def get_task_by_id(task_id: int, db: Session):
    return task_repository.get_task_by_id(db, task_id)


def get_tasks_for_user(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    return task_repository.get_tasks_by_user_id(db, user_id, skip, limit)


def update_task(task_id: int, data: task_schema.TaskUpdate, db: Session):
    return task_repository.update_task(db, task_id, data)


def delete_task(task_id: int, db: Session):
    return task_repository.delete_task(db, task_id)


def check_geofence_for_user(user_id: int, latitude: float, longitude: float, db: Session):
    cooldown = timedelta(minutes=30)
    now = datetime.now(timezone.utc)
    candidates = task_repository.get_active_location_tasks_by_user_id(db, user_id)

    triggered = []
    for task in candidates:
        distance = _haversine_meters(latitude, longitude, task.latitude, task.longitude)
        if distance > task.radius_meters:
            continue

        if task.last_triggered_at and now - task.last_triggered_at < cooldown:
            continue

        task.last_triggered_at = now
        triggered.append(task)

    if triggered:
        db.commit()
        for task in triggered:
            db.refresh(task)

    return triggered
