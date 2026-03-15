# KarLo Project Progress Tracker

Last updated: 2026-03-15

## Overall Status
- Project phase: Migration + Integration
- Frontend status: In progress (Next.js App Router migrated)
- Backend status: In progress (Core v1 APIs available)
- Deployment status: Not started

## Milestones

### 1. Foundation and Repo Setup
- [x] Frontend migrated from Vite React to Next.js App Router
- [x] Branch cleanup and merge to main/Stage completed
- [x] Basic project structure standardized
- [x] README files updated to reflect current architecture

### 2. Frontend (Next.js)
- [x] Global layout and route pages wired
- [x] Shared components/services structure added
- [x] Contribute form connected to backend API service
- [x] Contact form connected to backend API service
- [x] Login flow fully integrated with backend auth
- [x] Register flow fully integrated with backend auth
- [x] Dashboard module (MVP) implemented
- [x] Location selector UI implemented
- [x] Reminder UX (in-app + browser notifications)

### 3. Backend (FastAPI)
- [x] Auth routes available
- [x] User routes available
- [x] Contact routes available
- [x] Contribute routes available
- [x] Task/location reminder models added
- [x] Task/location reminder APIs added
- [ ] Authorization checks hardened for all private endpoints
- [ ] API test coverage for core flows

### 4. Location Features (Low-cost/Open)
- [x] Browser geolocation integration
- [x] Geofence distance check engine
- [ ] Open map integration (OSM/MapLibre)
- [ ] Geocoding with caching and rate limiting
- [x] Reminder trigger and dedupe logic

### 5. Quality and Release
- [ ] End-to-end test pass on local
- [ ] Staging deployment and smoke test
- [ ] Production deployment
- [ ] Monitoring/logging baseline

### 6. Runtime Setup
- [x] Backend virtual environment created
- [x] Backend dependencies installed in venv
- [x] Backend app starts with Uvicorn from venv
- [x] Email notification dependency removed from runtime path

## Current Sprint (Active)
- Goal: Stabilize Next.js frontend and align backend integration
- Target date: 2026-03-22

### Sprint Tasks
- [x] Update frontend README for Next.js architecture
- [x] Fix backend Python environment strategy (3.11 recommended)
- [x] Complete login/register API integration
- [x] Complete contact API integration
- [x] Add env template for frontend/backend
- [x] Define task/location data model draft
- [x] Start dashboard module MVP

## Blockers / Risks
- Python 3.14 dependency compatibility in backend environment
- Location reminders in browser require foreground app behavior
- Free-tier location/geocoding APIs may impose strict rate limits

## Change Log
### 2026-03-15
- Migrated frontend to Next.js App Router structure
- Standardized shared code under shared/
- Integrated contribute API service path in frontend
- Integrated contact API service path in frontend
- Integrated login/register flows with backend auth APIs
- Added task model + private task APIs (create/list/get/update/delete)
- Added dashboard task manager UI (create/list/complete/delete)
- Added browser geolocation and notification-permission UX
- Added backend geofence distance check endpoint with dedupe cooldown
- Added frontend/backend `.env.example` templates
- Added task/location data model draft document
- Updated frontend and backend READMEs to current architecture
- Created backend `.venv` and verified Uvicorn startup from the venv
- Removed email notification usage from backend runtime and config
- Settled main and Stage branches and merged migration
- Added PostCSS config to fix CSS processing in Next.js
- Added Python-version-aware PostgreSQL driver markers in requirements

## Notes
- Keep this file updated at the end of each working session.
- Use short, actionable updates only.
