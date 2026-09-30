import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register_login_and_home():
    email = "test@example.com"
    r = client.post("/api/register", json={"name":"Test User","email":email,"password":"secret123"})
    assert r.status_code in (201, 409)
    token = r.json().get("access_token")
    if not token:
        r = client.post("/api/login", json={"email":email,"password":"secret123"})
        assert r.status_code == 200
        token = r.json()["access_token"]

    headers={"Authorization":f"Bearer {token}"}
    r = client.post("/api/generate-home", headers=headers, json={
        "budget":10000,
        "rooms":"Living room: 1 table and 2 lights",
        "style":"modern",
        "requirements":"warm lighting"
    })
    assert r.status_code == 200
    body=r.json()
    assert body["planner"]=="home"
    assert body["recommendations"]
    assert body["budget_used"] <= 10000

def test_unauthorized_planner():
    r=client.post("/api/generate-party", json={
        "budget":10000,"guests":20,"event_type":"birthday"
    })
    assert r.status_code == 401
