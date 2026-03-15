from __future__ import annotations

from conftest import login_user, register_user


def test_auth_and_task_geofence_flow(client):
    register_response = register_user(client, "user1@example.com", "Password123", "User One")
    assert register_response.status_code == 201

    login_response = login_user(client, "user1@example.com", "Password123")
    assert login_response.status_code == 200
    assert login_response.cookies.get("access_token")

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 200
    user_id = me_response.json()["id"]

    create_task_response = client.post(
        "/api/v1/task/create",
        json={
            "title": "Buy groceries",
            "description": "Milk and bread",
            "latitude": 18.5204,
            "longitude": 73.8567,
            "radius_meters": 500,
            "remind_on_arrival": True,
        },
    )
    assert create_task_response.status_code == 201
    assert create_task_response.json()["data"]["user_id"] == user_id

    list_response = client.get("/api/v1/task/")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    geofence_response = client.post(
        "/api/v1/task/check-geofence",
        json={"latitude": 18.5204, "longitude": 73.8567},
    )
    assert geofence_response.status_code == 200
    assert geofence_response.json()["total_triggered"] == 1


def test_private_user_routes_enforce_self_or_admin(client):
    register_user(client, "owner@example.com", "Password123", "Owner User")
    register_user(client, "other@example.com", "Password123", "Other User")

    login_user(client, "owner@example.com", "Password123")
    users_response = client.get("/api/v1/user/")
    assert users_response.status_code == 403

    own_user = client.get("/api/v1/auth/me").json()
    own_response = client.get(f"/api/v1/user/{own_user['id']}")
    assert own_response.status_code == 200

    client.post("/api/v1/auth/logout")
    login_user(client, "other@example.com", "Password123")
    other_user = client.get("/api/v1/auth/me").json()

    client.post("/api/v1/auth/logout")
    login_user(client, "owner@example.com", "Password123")

    other_response = client.get(f"/api/v1/user/{other_user['id']}")
    assert other_response.status_code == 403


def test_non_admin_cannot_read_contact_or_contribute_lists(client):
    register_user(client, "reader@example.com", "Password123", "Reader User")
    login_user(client, "reader@example.com", "Password123")

    contact_response = client.get("/api/v1/contact/")
    contribute_response = client.get("/api/v1/contribute/")

    assert contact_response.status_code == 403
    assert contribute_response.status_code == 403


def test_geocode_endpoint_with_mocked_provider(client, monkeypatch):
    register_user(client, "geo@example.com", "Password123", "Geo User")
    login_user(client, "geo@example.com", "Password123")

    from app.karlo_c.services.geocoding import geocoding_service

    class MockResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return [
                {
                    "display_name": "Pune, Maharashtra, India",
                    "lat": "18.5204",
                    "lon": "73.8567",
                }
            ]

    monkeypatch.setattr(geocoding_service.requests, "get", lambda *args, **kwargs: MockResponse())

    response = client.get("/api/v1/geocode/search", params={"q": "Pune"})
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["results"][0]["display_name"] == "Pune, Maharashtra, India"


def test_home_cure_admin_routes_reject_regular_users(client):
    register_response = client.post(
        "/home_cure/auth/register",
        json={
            "full_name": "Home Cure User",
            "email": "homecure@example.com",
            "password": "Password123",
        },
    )
    assert register_response.status_code == 201
    home_cure_user_id = register_response.json()["data"]["id"]

    login_response = client.post(
        "/home_cure/auth/login",
        json={
            "email": "homecure@example.com",
            "password": "Password123",
        },
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    me_response = client.put(
        f"/home_cure/auth/{home_cure_user_id}/update",
        json={"full_name": "Updated Home Cure User"},
        headers=headers,
    )
    assert me_response.status_code == 200
    assert me_response.json()["full_name"] == "Updated Home Cure User"

    admin_response = client.get("/home_cure/admin/dashboard/kpis", headers=headers)
    assert admin_response.status_code == 403