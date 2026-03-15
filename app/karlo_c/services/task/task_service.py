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


def _task_schedule(task) -> str:
    schedule = getattr(task, "reminder_schedule", None)
    return schedule or "daily"


def _is_task_active_for_now(task, now: datetime) -> bool:
    schedule = _task_schedule(task)

    if schedule == "daily":
        return True

    if schedule == "weekdays":
        return now.weekday() < 5

    if schedule == "tomorrow":
        due_at = getattr(task, "due_at", None)
        if due_at is None:
            created_at = getattr(task, "created_at", None)
            if created_at is None:
                return False
            due_at = created_at + timedelta(days=1)

        if due_at.tzinfo is None:
            due_at = due_at.replace(tzinfo=timezone.utc)

        return now.date() == due_at.astimezone(timezone.utc).date()

    return True


def create_task(data: task_schema.TaskCreate, user_id: int, db: Session):
    payload = data.model_dump()
    payload["user_id"] = user_id
    if payload.get("reminder_schedule") == "tomorrow" and payload.get("due_at") is None:
        payload["due_at"] = datetime.now(timezone.utc) + timedelta(days=1)
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
        if not _is_task_active_for_now(task, now):
            continue

        distance = _haversine_meters(latitude, longitude, task.latitude, task.longitude)
        if distance > task.radius_meters:
            continue

        if task.last_triggered_at and now - task.last_triggered_at < cooldown:
            continue

        task.last_triggered_at = now
        if _task_schedule(task) == "tomorrow":
            task.is_completed = True
        triggered.append(task)

    if triggered:
        db.commit()
        for task in triggered:
            db.refresh(task)

    return triggered
