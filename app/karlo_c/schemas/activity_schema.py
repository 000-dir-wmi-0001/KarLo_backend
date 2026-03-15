from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class ActivityItem(BaseModel):
    type: Literal["task_created", "task_updated", "task_completed", "reminder_triggered"]
    title: str
    description: str
    task_id: int
    timestamp: datetime


class ActivityListResponse(BaseModel):
    items: list[ActivityItem]
    total: int
