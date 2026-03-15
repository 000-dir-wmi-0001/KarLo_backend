from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.karlo_c.schemas import task_schema
from app.karlo_c.services.task import task_service


task_router = APIRouter(prefix="/task", tags=["Task"])


def _get_auth_user_id(request: Request) -> int:
    token_payload = getattr(request.state, "user", None)
    token_sub = token_payload.get("sub") if isinstance(token_payload, dict) else None
    if token_sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return int(token_sub)


@task_router.post("/create", response_model=task_schema.CreateTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: task_schema.TaskCreate, request: Request, db: Session = Depends(get_db)):
    user_id = _get_auth_user_id(request)
    created = task_service.create_task(task, user_id, db)
    return {
        "data": created,
        "message": "Task created successfully",
    }


@task_router.get("/", response_model=task_schema.TaskListResponse)
def list_my_tasks(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_id = _get_auth_user_id(request)
    tasks = task_service.get_tasks_for_user(user_id, db, skip, limit)
    return {
        "tasks": tasks,
        "total": len(tasks),
    }


@task_router.get("/{task_id}", response_model=task_schema.TaskResponse)
def get_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = _get_auth_user_id(request)
    task = task_service.get_task_by_id(task_id, db)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@task_router.put("/update/{task_id}", response_model=task_schema.TaskResponse)
def update_task(task_id: int, task: task_schema.TaskUpdate, request: Request, db: Session = Depends(get_db)):
    user_id = _get_auth_user_id(request)
    existing = task_service.get_task_by_id(task_id, db)
    if not existing or existing.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated = task_service.update_task(task_id, task, db)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated


@task_router.delete("/delete/{task_id}", response_model=task_schema.TaskDeleteResponse)
def delete_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = _get_auth_user_id(request)
    existing = task_service.get_task_by_id(task_id, db)
    if not existing or existing.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    deleted = task_service.delete_task(task_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return {
        "success": True,
        "message": f"Task with ID {task_id} deleted successfully",
    }


@task_router.post("/check-geofence", response_model=task_schema.GeofenceCheckResponse)
def check_geofence(payload: task_schema.GeofenceCheckRequest, request: Request, db: Session = Depends(get_db)):
    user_id = _get_auth_user_id(request)
    triggered = task_service.check_geofence_for_user(user_id, payload.latitude, payload.longitude, db)
    return {
        "triggered_tasks": triggered,
        "total_triggered": len(triggered),
    }
