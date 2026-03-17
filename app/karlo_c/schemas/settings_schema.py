from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class UserSettingsBase(BaseModel):
    default_radius_meters: int = Field(default=150, ge=25, le=5000)
    default_reminder_schedule: Literal["daily", "weekdays", "tomorrow"] = "daily"
    notifications_enabled: bool = True
    live_tracking_enabled: bool = False


class UserSettingsUpdate(BaseModel):
    default_radius_meters: int | None = Field(default=None, ge=25, le=5000)
    default_reminder_schedule: Literal["daily", "weekdays", "tomorrow"] | None = None
    notifications_enabled: bool | None = None
    live_tracking_enabled: bool | None = None


class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
