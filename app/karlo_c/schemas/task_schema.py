from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    radius_meters: int = Field(default=150, ge=25, le=5000)

    remind_on_arrival: bool = True
    due_at: Optional[datetime] = None


class TaskCreate(TaskBase):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    radius_meters: Optional[int] = Field(default=None, ge=25, le=5000)
    remind_on_arrival: Optional[bool] = None
    due_at: Optional[datetime] = None
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    is_completed: bool
    last_triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int


class TaskDeleteResponse(BaseModel):
    success: bool
    message: str


class CreateTaskResponse(BaseModel):
    data: TaskResponse
    message: str


class GeofenceCheckRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class GeofenceCheckResponse(BaseModel):
    triggered_tasks: list[TaskResponse]
    total_triggered: int
