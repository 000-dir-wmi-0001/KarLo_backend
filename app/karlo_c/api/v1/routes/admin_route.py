"""
Admin dashboard FastAPI routes.
All endpoints require is_superuser via require_superuser(request, db).
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.karlo_c.api.v1.authz import require_superuser
from app.karlo_c.schemas import admin_schema
from app.karlo_c.repositories.admin import admin_repository as repo

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


# ──────────────────────────────────────────
# Overview  (Phase 1)
# ──────────────────────────────────────────

@admin_router.get("/overview/stats", response_model=admin_schema.AdminOverviewStats)
def overview_stats(request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    return repo.get_overview_stats(db)


# ──────────────────────────────────────────
# User management  (Phase 1)
# ──────────────────────────────────────────

@admin_router.get("/users", response_model=admin_schema.AdminUserListResponse)
def list_users(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str = Query(""),
    role: str = Query(""),
    is_active: Optional[bool] = Query(None),
    is_deleted: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    users, total = repo.get_admin_users(
        db, skip=skip, limit=limit,
        search=search, role=role,
        is_active=is_active, is_deleted=is_deleted,
    )
    return {"users": users, "total": total}


@admin_router.get("/users/{user_id}", response_model=admin_schema.AdminUserResponse)
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    user = repo.get_admin_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@admin_router.put("/users/{user_id}", response_model=admin_schema.AdminUserResponse)
def update_user(
    user_id: int,
    data: admin_schema.AdminUserUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    updated = repo.admin_update_user(db, user_id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@admin_router.delete("/users/{user_id}", response_model=admin_schema.AdminActionResponse)
def soft_delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    ok = repo.soft_delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": f"User {user_id} soft-deleted"}


@admin_router.delete("/users/{user_id}/hard", response_model=admin_schema.AdminActionResponse)
def hard_delete_user(
    user_id: int,
    body: admin_schema.AdminHardDeleteRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    if not body.confirm:
        raise HTTPException(status_code=400, detail="Send { confirm: true } to permanently delete")
    ok = repo.hard_delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": f"User {user_id} permanently deleted"}


@admin_router.post("/users/{user_id}/restore", response_model=admin_schema.AdminUserResponse)
def restore_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    user = repo.restore_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ──────────────────────────────────────────
# Task analytics  (Phase 2)
# ──────────────────────────────────────────

@admin_router.get("/tasks/stats", response_model=admin_schema.AdminTaskStats)
def task_stats(request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    return repo.get_task_stats(db)


@admin_router.delete("/tasks/{task_id}", response_model=admin_schema.AdminActionResponse)
def force_delete_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    ok = repo.admin_delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "message": f"Task {task_id} deleted"}


# ──────────────────────────────────────────
# Reminder analytics  (Phase 2)
# ──────────────────────────────────────────

@admin_router.get("/reminders/stats", response_model=admin_schema.AdminReminderStats)
def reminder_stats(request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    return repo.get_reminder_stats(db)


# ──────────────────────────────────────────
# Contact inbox  (Phase 2)
# ──────────────────────────────────────────

@admin_router.get("/contacts", response_model=admin_schema.AdminContactListResponse)
def list_contacts(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    contacts, total = repo.get_all_contacts_admin(db, skip, limit)
    return {"contacts": contacts, "total": total}


@admin_router.patch("/contacts/{contact_id}/read", response_model=admin_schema.AdminContactResponse)
def mark_read(contact_id: int, request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    contact = repo.mark_contact_read(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@admin_router.delete("/contacts/{contact_id}", response_model=admin_schema.AdminActionResponse)
def delete_contact(contact_id: int, request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    ok = repo.delete_contact_admin(db, contact_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"success": True, "message": f"Contact {contact_id} deleted"}


@admin_router.get("/contributions", response_model=admin_schema.AdminContributeListResponse)
def list_contributions(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    contribs, total = repo.get_all_contributions_admin(db, skip, limit)
    return {"contributions": contribs, "total": total}


# ──────────────────────────────────────────
# Newsletter  (Phase 3)
# ──────────────────────────────────────────

@admin_router.get("/newsletter/subscribers", response_model=admin_schema.AdminNewsletterListResponse)
def list_newsletter_subscribers(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=2000),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    subscribers, total = repo.get_newsletter_subscribers(db, skip, limit)
    return {"subscribers": subscribers, "total": total}


@admin_router.get("/newsletter/subscribers/export")
def export_newsletter_subscribers_csv(request: Request, db: Session = Depends(get_db)):
    """Download newsletter subscriber list as CSV."""
    import csv, io
    from fastapi.responses import StreamingResponse

    require_superuser(request, db)
    rows = repo.get_newsletter_subscribers_for_csv(db)

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "full_name", "email", "country", "city", "joined"])
    for r in rows:
        writer.writerow([r[0], r[1] or "", r[2] or "", r[3] or "", r[4] or "", str(r[5] or "")])

    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=newsletter_subscribers.csv"},
    )


# ──────────────────────────────────────────
# Security Audit Log  (Phase 3)
# ──────────────────────────────────────────

@admin_router.get("/security/logs", response_model=admin_schema.AdminSecurityLogListResponse)
def list_security_logs(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    action: str = Query(""),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    logs, total = repo.get_security_logs(db, skip=skip, limit=limit, action_filter=action)
    return {"logs": logs, "total": total}


# ──────────────────────────────────────────
# Geofence Density Heatmap  (Phase 3)
# ──────────────────────────────────────────

@admin_router.get("/heatmap/tasks", response_model=admin_schema.AdminHeatmapResponse)
def heatmap_tasks(
    request: Request,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    return repo.get_task_heatmap(db, days=days)


@admin_router.get("/heatmap/reminders", response_model=admin_schema.AdminHeatmapResponse)
def heatmap_reminders(
    request: Request,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    return repo.get_reminder_heatmap(db, days=days)


@admin_router.get("/heatmap/tasks/export")
def export_heatmap_tasks_geojson(
    request: Request,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    """Export aggregated task geofence heatmap as GeoJSON FeatureCollection."""
    import json
    from fastapi.responses import Response

    require_superuser(request, db)
    data = repo.get_task_heatmap(db, days=days)
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [cell["lng_bucket"], cell["lat_bucket"]]},
            "properties": {"count": cell["count"]},
        }
        for cell in data["cells"]
    ]
    geojson = {"type": "FeatureCollection", "features": features}
    return Response(
        content=json.dumps(geojson),
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=task_geofence_heatmap.geojson"},
    )


# ──────────────────────────────────────────
# Platform Settings  (Phase 4)
# ──────────────────────────────────────────

@admin_router.get("/settings", response_model=admin_schema.AdminPlatformSettings)
def get_settings(request: Request, db: Session = Depends(get_db)):
    require_superuser(request, db)
    return repo.get_platform_settings(db)


@admin_router.patch("/settings", response_model=admin_schema.AdminActionResponse)
def update_settings(
    body: admin_schema.AdminPlatformSettingsUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    require_superuser(request, db)
    if body.maintenance_mode is not None:
        repo.update_maintenance_mode(body.maintenance_mode)
        token_payload = getattr(request.state, "user", {}) or {}
        repo.write_security_log(
            db,
            admin_user_id=int(token_payload.get("sub", 0)),
            admin_email=str(token_payload.get("email", "")),
            action="update_maintenance_mode",
            detail=f"maintenance_mode set to {body.maintenance_mode}",
        )
    return {"success": True, "message": "Settings updated"}


# ──────────────────────────────────────────
# CSV Exports  (Phase 4)
# ──────────────────────────────────────────

@admin_router.get("/users/export")
def export_users_csv(request: Request, db: Session = Depends(get_db)):
    """Download user list as CSV (no passwords, no encrypted content)."""
    import csv, io
    from fastapi.responses import StreamingResponse

    require_superuser(request, db)
    rows = repo.get_users_for_csv(db)

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "full_name", "email", "role", "is_active", "is_verified",
                     "newsletter_opt_in", "country", "city", "joined"])
    for r in rows:
        writer.writerow([r[0], r[1] or "", r[2] or "", r[3] or "", r[4], r[5], r[6], r[7] or "", r[8] or "", str(r[10] or "")])

    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=karlo_users.csv"},
    )

