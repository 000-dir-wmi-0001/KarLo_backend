"""
Pydantic schemas for all admin dashboard endpoints.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ──────────────────────────────────────────
# Overview
# ──────────────────────────────────────────

class AdminOverviewStats(BaseModel):
    total_users: int
    active_users_30d: int
    new_signups_7d: int
    newsletter_subscribers: int
    total_tasks: int
    total_reminders_triggered: int


# ──────────────────────────────────────────
# User management
# ──────────────────────────────────────────

class AdminUserResponse(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_superuser: bool
    is_deleted: bool
    agreed_to_terms: bool
    newsletter_opt_in: bool
    country: Optional[str] = None
    city: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AdminUserListResponse(BaseModel):
    users: List[AdminUserResponse]
    total: int


class AdminUserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None


class AdminHardDeleteRequest(BaseModel):
    confirm: bool = False


# ──────────────────────────────────────────
# Task analytics
# ──────────────────────────────────────────

class DailyCount(BaseModel):
    date: str          # ISO date string  e.g. "2026-03-16"
    count: int


class AdminTaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    avg_per_user: float
    daily_counts: List[DailyCount]


# ──────────────────────────────────────────
# Reminder analytics
# ──────────────────────────────────────────

class AdminReminderStats(BaseModel):
    total_triggered: int
    enter_count: int
    exit_count: int
    avg_per_user: float
    daily_counts: List[DailyCount]


# ──────────────────────────────────────────
# Contact & Contribution inbox
# ──────────────────────────────────────────

class AdminContactResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    website: Optional[str] = None
    is_read: bool = False
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AdminContactListResponse(BaseModel):
    contacts: List[AdminContactResponse]
    total: int


class AdminContributeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    gitHub_link: Optional[str] = None
    linkedIn_link: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AdminContributeListResponse(BaseModel):
    contributions: List[AdminContributeResponse]
    total: int


class AdminActionResponse(BaseModel):
    success: bool
    message: str


# ──────────────────────────────────────────
# Newsletter  (Phase 3)
# ──────────────────────────────────────────

class AdminNewsletterSubscriber(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AdminNewsletterListResponse(BaseModel):
    subscribers: List[AdminNewsletterSubscriber]
    total: int


# ──────────────────────────────────────────
# Security Audit Log  (Phase 3)
# ──────────────────────────────────────────

class AdminSecurityLogEntry(BaseModel):
    id: int
    admin_user_id: int
    admin_email: Optional[str] = None
    action: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    detail: Optional[str] = None
    performed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AdminSecurityLogListResponse(BaseModel):
    logs: List[AdminSecurityLogEntry]
    total: int


# ──────────────────────────────────────────
# Geofence Density Heatmap  (Phase 3)
# ──────────────────────────────────────────

class HeatmapCell(BaseModel):
    lat_bucket: float
    lng_bucket: float
    count: int


class AdminHeatmapResponse(BaseModel):
    cells: List[HeatmapCell]
    total_cells: int
    suppressed_cells: int   # cells below k-anonymity threshold, not returned
    days: int


# ──────────────────────────────────────────
# Platform Settings  (Phase 4)
# ──────────────────────────────────────────

class AdminPlatformSettings(BaseModel):
    maintenance_mode: bool
    environment: str
    app_version: str
    total_users: int
    total_tasks: int


class AdminPlatformSettingsUpdate(BaseModel):
    maintenance_mode: Optional[bool] = None

