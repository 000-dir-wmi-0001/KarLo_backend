from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database_path = tmp_path / "test_karlo.db"

    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("ORIGIN_URL", "http://localhost:3000")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path.as_posix()}")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    monkeypatch.setenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    monkeypatch.setenv("COOKIE_SECURE", "false")
    monkeypatch.setenv("COOKIE_SAMESITE", "lax")
    monkeypatch.delenv("COOKIE_DOMAIN", raising=False)

    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            del sys.modules[name]

    app_main = importlib.import_module("app.main")
    db_base = importlib.import_module("app.db.base")
    db_session = importlib.import_module("app.db.session")

    db_base.Base.metadata.create_all(bind=db_session.engine)

    with TestClient(app_main.app) as test_client:
        yield test_client

    db_base.Base.metadata.drop_all(bind=db_session.engine)


def register_user(client: TestClient, email: str, password: str, full_name: str = "Test User"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
        },
    )


def login_user(client: TestClient, email: str, password: str):
    return client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )