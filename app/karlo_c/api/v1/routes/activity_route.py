from datetime import timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.karlo_c.api.v1.authz import get_current_user_id
from app.karlo_c.schemas.activity_schema import ActivityListResponse
from app.karlo_c.services.task import task_service


activity_router = APIRouter(prefix="/activity", tags=["Activity"])


def _to_utc(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@activity_router.get("/", response_model=ActivityListResponse)
@activity_router.get("", response_model=ActivityListResponse, include_in_schema=False)
def list_activity(request: Request, limit: int = 200, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    tasks = task_service.get_tasks_for_user(user_id, db, 0, limit)

    items = []
    for task in tasks:
        created_at = _to_utc(task.created_at)
        updated_at = _to_utc(task.updated_at)
        last_triggered = _to_utc(task.last_triggered_at)

        if created_at:
            items.append(
                {
                    "type": "task_created",
                    "title": task.title,
                    "description": "Task created",
                    "task_id": task.id,
                    "timestamp": created_at,
                }
            )

        if updated_at and created_at and updated_at > created_at and not task.is_completed:
            items.append(
                {
                    "type": "task_updated",
                    "title": task.title,
                    "description": "Task updated",
                    "task_id": task.id,
                    "timestamp": updated_at,
                }
            )

        if task.is_completed and updated_at:
            items.append(
                {
                    "type": "task_completed",
                    "title": task.title,
                    "description": "Task marked as completed",
                    "task_id": task.id,
                    "timestamp": updated_at,
                }
            )

        if last_triggered:
            items.append(
                {
                    "type": "reminder_triggered",
                    "title": task.title,
                    "description": "Reminder triggered by location",
                    "task_id": task.id,
                    "timestamp": last_triggered,
                }
            )

    items.sort(key=lambda item: item["timestamp"], reverse=True)
    return {"items": items[:limit], "total": len(items)}
