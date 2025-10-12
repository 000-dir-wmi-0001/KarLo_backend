from fastapi import APIRouter

dashboard_router = APIRouter(prefix="/dashboard", tags=["Admin Dashboard"])


@dashboard_router.get("/kpis")
def get_kpis():
    """Return basic KPIs for admin dashboard. This is a simple implementation
    to satisfy frontend requests. Add real analytics logic later.
    """
    return {
        "total_users": 1000,
        "total_technicians": 50,
        "active_bookings": 25,
        "total_revenue": 50000.00,
        "average_rating": 4.7,
        "bookings_today": 5,
        "new_users_this_month": 100,
    }
