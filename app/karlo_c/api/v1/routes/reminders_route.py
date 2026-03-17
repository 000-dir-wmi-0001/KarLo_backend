from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.karlo_c.api.v1.authz import get_current_user_id
from app.karlo_c.schemas.task_schema import TaskListResponse, TaskResponse, TaskUpdate
from app.karlo_c.services.task import task_service


reminders_router = APIRouter(prefix="/reminders", tags=["Reminders"])


@reminders_router.get("/", response_model=TaskListResponse)
@reminders_router.get("", response_model=TaskListResponse, include_in_schema=False)
def list_my_reminders(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    tasks = task_service.get_tasks_for_user(user_id, db, skip, limit)
    reminders = [task for task in tasks if task.latitude is not None and task.longitude is not None]
    return {"tasks": reminders, "total": len(reminders)}


@reminders_router.put("/{task_id}", response_model=TaskResponse)
def update_reminder(task_id: int, payload: TaskUpdate, request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    task = task_service.get_task_by_id(task_id, db)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")

    updated = task_service.update_task(task_id, payload, db)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")

    return updated
