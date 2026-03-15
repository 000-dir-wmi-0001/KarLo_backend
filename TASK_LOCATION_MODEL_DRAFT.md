# Task, Location, Reminder Data Model Draft

## Scope
This draft defines the first production-ready schema for location-aware reminders in KarLo.

## Core Entity: Task
- id: integer primary key
- user_id: FK to user.id
- title: short required text
- description: optional text
- latitude: optional float, range -90 to 90
- longitude: optional float, range -180 to 180
- radius_meters: integer, default 150, valid 25-5000
- remind_on_arrival: boolean, default true
- is_completed: boolean, default false
- due_at: optional datetime (UTC)
- last_triggered_at: optional datetime (UTC)
- created_at: datetime (UTC)
- updated_at: datetime (UTC)

## Location Trigger Rules
- A task is location-triggerable when both latitude and longitude are present.
- Trigger condition: user enters geofence where distance <= radius_meters.
- Dedupe condition: ignore repeated triggers for same task within cooldown window (recommended 30 minutes).

## Reminder Strategy (MVP)
- Frontend requests browser notification permission.
- Frontend can poll task list and compare current location vs task geofences.
- Backend stores last_triggered_at to support dedupe and analytics.

## Open Items
- Add dedicated reminder event table for audit trail.
- Add task categories and priority fields.
- Add timezone handling strategy for due_at display.
