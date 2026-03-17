"""
Admin repository — all aggregate DB queries used by the admin dashboard.

Privacy rules enforced here:
  - NEVER SELECT title, description, message, location_label or any content column.
  - Only COUNT(*), status flags, timestamps, and user_id are accessed.
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.karlo_c.models.user_model import KarloUser as User
from app.karlo_c.models.task_model import Task
from app.karlo_c.models.contact_model import Contact
from app.karlo_c.models.contribute_model import Contribute


def _now():
    return datetime.now(timezone.utc)


# ──────────────────────────────────────────
# Overview
# ──────────────────────────────────────────

def get_overview_stats(db: Session) -> dict:
    now = _now()
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago = now - timedelta(days=7)

    total_users = db.query(func.count(User.id)).filter(User.is_deleted == False).scalar() or 0

    active_users_30d = (
        db.query(func.count(User.id))
        .filter(User.is_deleted == False, User.last_login >= thirty_days_ago)
        .scalar() or 0
    )

    new_signups_7d = (
        db.query(func.count(User.id))
        .filter(User.is_deleted == False, User.created_at >= seven_days_ago)
        .scalar() or 0
    )

    newsletter_subscribers = (
        db.query(func.count(User.id))
        .filter(User.is_deleted == False, User.newsletter_opt_in == True)
        .scalar() or 0
    )

    # Privacy: count only — never select title / description
    total_tasks = db.query(func.count(Task.id)).scalar() or 0

    # Reminder triggers: count rows where type is reminder_triggered from activity
    # Activity is stored in JSON-backed records. We use a safe raw COUNT.
    try:
        total_reminders = db.execute(
            text("SELECT COUNT(*) FROM activity WHERE type = 'reminder_triggered'")
        ).scalar() or 0
    except Exception:
        total_reminders = 0

    return {
        "total_users": total_users,
        "active_users_30d": active_users_30d,
        "new_signups_7d": new_signups_7d,
        "newsletter_subscribers": newsletter_subscribers,
        "total_tasks": total_tasks,
        "total_reminders_triggered": total_reminders,
    }


# ──────────────────────────────────────────
# User management
# ──────────────────────────────────────────

def get_admin_users(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: str = "",
    role: str = "",
    is_active: bool | None = None,
    is_deleted: bool | None = None,
) -> tuple[list, int]:
    q = db.query(User)

    if search:
        like = f"%{search}%"
        q = q.filter((User.full_name.ilike(like)) | (User.email.ilike(like)))
    if role:
        q = q.filter(User.role == role)
    if is_active is not None:
        q = q.filter(User.is_active == is_active)
    if is_deleted is not None:
        q = q.filter(User.is_deleted == is_deleted)
    else:
        # default: show non-deleted users
        q = q.filter(User.is_deleted == False)

    total = q.count()
    users = q.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users, total


def get_admin_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def admin_update_user(db: Session, user_id: int, data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for field, value in data.items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    user.is_deleted = True
    user.deleted_at = _now()
    db.commit()
    return True


def hard_delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def restore_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.is_deleted = False
    user.deleted_at = None
    db.commit()
    db.refresh(user)
    return user


# ──────────────────────────────────────────
# Task analytics — Privacy: COUNT only, no content
# ──────────────────────────────────────────

def get_task_stats(db: Session) -> dict:
    total = db.query(func.count(Task.id)).scalar() or 0
    completed = db.query(func.count(Task.id)).filter(Task.is_completed == True).scalar() or 0
    pending = total - completed

    distinct_users = db.query(func.count(func.distinct(Task.user_id))).scalar() or 1
    avg_per_user = round(total / distinct_users, 2) if distinct_users else 0.0

    # Last 30 days — date bucket + count, NO content columns
    thirty_days_ago = _now() - timedelta(days=30)
    rows = (
        db.query(
            func.date(Task.created_at).label("date"),
            func.count(Task.id).label("count"),
        )
        .filter(Task.created_at >= thirty_days_ago)
        .group_by(func.date(Task.created_at))
        .order_by(func.date(Task.created_at))
        .all()
    )
    daily_counts = [{"date": str(r.date), "count": r.count} for r in rows]

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "avg_per_user": avg_per_user,
        "daily_counts": daily_counts,
    }


def admin_delete_task(db: Session, task_id: int) -> bool:
    """Admin force-delete — never reads or returns content."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


# ──────────────────────────────────────────
# Reminder analytics — Privacy: COUNT only, no content
# ──────────────────────────────────────────

def get_reminder_stats(db: Session) -> dict:
    thirty_days_ago = _now() - timedelta(days=30)

    try:
        total_triggered = db.execute(
            text("SELECT COUNT(*) FROM activity WHERE type = 'reminder_triggered'")
        ).scalar() or 0

        enter_count = db.execute(
            text("SELECT COUNT(*) FROM activity WHERE type = 'reminder_triggered' AND trigger_type = 'enter'")
        ).scalar() or 0

        exit_count = db.execute(
            text("SELECT COUNT(*) FROM activity WHERE type = 'reminder_triggered' AND trigger_type = 'exit'")
        ).scalar() or 0

        distinct_users = db.execute(
            text("SELECT COUNT(DISTINCT user_id) FROM activity WHERE type = 'reminder_triggered'")
        ).scalar() or 1

        avg_per_user = round(total_triggered / distinct_users, 2) if distinct_users else 0.0

        rows = db.execute(
            text("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM activity
                WHERE type = 'reminder_triggered'
                  AND created_at >= :cutoff
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at)
            """),
            {"cutoff": thirty_days_ago},
        ).fetchall()
        daily_counts = [{"date": str(r[0]), "count": r[1]} for r in rows]

    except Exception:
        total_triggered = enter_count = exit_count = 0
        avg_per_user = 0.0
        daily_counts = []

    return {
        "total_triggered": total_triggered,
        "enter_count": enter_count,
        "exit_count": exit_count,
        "avg_per_user": avg_per_user,
        "daily_counts": daily_counts,
    }


# ──────────────────────────────────────────
# Contact inbox
# ──────────────────────────────────────────

def get_all_contacts_admin(db: Session, skip: int = 0, limit: int = 100):
    q = db.query(Contact).order_by(Contact.created_at.desc())
    total = q.count()
    contacts = q.offset(skip).limit(limit).all()
    return contacts, total


def mark_contact_read(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return None
    contact.is_read = True
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact_admin(db: Session, contact_id: int) -> bool:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return False
    db.delete(contact)
    db.commit()
    return True


def get_all_contributions_admin(db: Session, skip: int = 0, limit: int = 100):
    q = db.query(Contribute)
    total = q.count()
    contributions = q.offset(skip).limit(limit).all()
    return contributions, total


# ──────────────────────────────────────────
# Newsletter  (Phase 3)
# ──────────────────────────────────────────

def get_newsletter_subscribers(db: Session, skip: int = 0, limit: int = 500):
    q = (
        db.query(User)
        .filter(User.newsletter_opt_in == True, User.is_deleted == False)
        .order_by(User.created_at.desc())
    )
    total = q.count()
    subscribers = q.offset(skip).limit(limit).all()
    return subscribers, total


# ──────────────────────────────────────────
# Security Audit Log  (Phase 3)
# ──────────────────────────────────────────

from app.karlo_c.models.admin_security_log_model import AdminSecurityLog


def write_security_log(
    db: Session,
    admin_user_id: int,
    admin_email: str,
    action: str,
    target_type: str | None = None,
    target_id: int | None = None,
    detail: str | None = None,
):
    """Append an audit record. Never update or delete existing rows."""
    entry = AdminSecurityLog(
        admin_user_id=admin_user_id,
        admin_email=admin_email,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_security_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    action_filter: str = "",
) -> tuple[list, int]:
    q = db.query(AdminSecurityLog).order_by(AdminSecurityLog.performed_at.desc())
    if action_filter:
        q = q.filter(AdminSecurityLog.action.ilike(f"%{action_filter}%"))
    total = q.count()
    logs = q.offset(skip).limit(limit).all()
    return logs, total


# ──────────────────────────────────────────
# Geofence Density Heatmap  (Phase 3)
# Privacy: ROUND(lat,2)/ROUND(lng,2) bucketing + k-anonymity ≥ 5
# ──────────────────────────────────────────

import os

K_ANONYMITY_THRESHOLD = int(os.getenv("HEATMAP_K_ANONYMITY", "2"))


def get_task_heatmap(db: Session, days: int = 30) -> dict:
    """
    Returns lat/lng grid cells with density counts for task geofences.
    Cells with fewer than K_ANONYMITY_THRESHOLD unique users are suppressed.
    Privacy: reads ONLY latitude/longitude/created_at/user_id — never title/description.
    """
    cutoff = _now() - timedelta(days=days)
    try:
        # Two-step: raw cells + k-anonymity filter
        rows = db.execute(
            text("""
                SELECT
                    ROUND(CAST(latitude AS NUMERIC), 2)  AS lat_bucket,
                    ROUND(CAST(longitude AS NUMERIC), 2) AS lng_bucket,
                    COUNT(*)                              AS total_count,
                    COUNT(DISTINCT user_id)               AS unique_users
                FROM task
                WHERE latitude IS NOT NULL
                  AND longitude IS NOT NULL
                  AND created_at >= :cutoff
                GROUP BY lat_bucket, lng_bucket
                ORDER BY total_count DESC
            """),
            {"cutoff": cutoff},
        ).fetchall()

        cells = []
        suppressed = 0
        for r in rows:
            if r[3] < K_ANONYMITY_THRESHOLD:
                suppressed += 1
            else:
                cells.append({
                    "lat_bucket": float(r[0]),
                    "lng_bucket": float(r[1]),
                    "count": int(r[2]),
                })

        return {
            "cells": cells,
            "total_cells": len(cells),
            "suppressed_cells": suppressed,
            "days": days,
        }
    except Exception:
        return {"cells": [], "total_cells": 0, "suppressed_cells": 0, "days": days}


def get_reminder_heatmap(db: Session, days: int = 30) -> dict:
    """
    Same structure but for the reminder (activity) table.
    Falls back gracefully if activity table has no lat/lng columns.
    """
    cutoff = _now() - timedelta(days=days)
    try:
        rows = db.execute(
            text("""
                SELECT
                    ROUND(CAST(task_latitude AS NUMERIC), 2)  AS lat_bucket,
                    ROUND(CAST(task_longitude AS NUMERIC), 2) AS lng_bucket,
                    COUNT(*)                                   AS total_count,
                    COUNT(DISTINCT user_id)                    AS unique_users
                FROM activity
                WHERE task_latitude IS NOT NULL
                  AND task_longitude IS NOT NULL
                  AND type = 'reminder_triggered'
                  AND created_at >= :cutoff
                GROUP BY lat_bucket, lng_bucket
                ORDER BY total_count DESC
            """),
            {"cutoff": cutoff},
        ).fetchall()

        cells = []
        suppressed = 0
        for r in rows:
            if r[3] < K_ANONYMITY_THRESHOLD:
                suppressed += 1
            else:
                cells.append({
                    "lat_bucket": float(r[0]),
                    "lng_bucket": float(r[1]),
                    "count": int(r[2]),
                })

        return {
            "cells": cells,
            "total_cells": len(cells),
            "suppressed_cells": suppressed,
            "days": days,
        }
    except Exception:
        return {"cells": [], "total_cells": 0, "suppressed_cells": 0, "days": days}


# ──────────────────────────────────────────
# Platform Settings  (Phase 4)
# ──────────────────────────────────────────

import os

_maintenance_mode: dict[str, bool] = {"enabled": False}


def get_platform_settings(db: Session) -> dict:
    total_users = db.query(func.count(User.id)).filter(User.is_deleted == False).scalar() or 0
    total_tasks = db.query(func.count(Task.id)).scalar() or 0
    return {
        "maintenance_mode": _maintenance_mode["enabled"],
        "environment": os.getenv("APP_ENV", "development"),
        "app_version": os.getenv("APP_VERSION", "1.0.0"),
        "total_users": total_users,
        "total_tasks": total_tasks,
    }


def update_maintenance_mode(enabled: bool) -> None:
    """In-memory toggle — replace with DB/Redis flag in production."""
    _maintenance_mode["enabled"] = enabled


# ──────────────────────────────────────────
# CSV Export helpers  (Phase 4)
# ──────────────────────────────────────────

def get_users_for_csv(db: Session) -> list:
    """Used for CSV export — returns safe non-sensitive fields only."""
    return (
        db.query(
            User.id, User.full_name, User.email, User.role,
            User.is_active, User.is_verified, User.is_deleted,
            User.newsletter_opt_in, User.country, User.city,
            User.created_at,
        )
        .filter(User.is_deleted == False)
        .order_by(User.created_at.desc())
        .all()
    )


def get_newsletter_subscribers_for_csv(db: Session) -> list:
    return (
        db.query(User.id, User.full_name, User.email, User.country, User.city, User.created_at)
        .filter(User.newsletter_opt_in == True, User.is_deleted == False)
        .order_by(User.created_at.desc())
        .all()
    )

