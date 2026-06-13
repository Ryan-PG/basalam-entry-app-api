import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_admin(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/register",
        json={"username": "admin1", "email": "admin@example.com", "password": "StrongPassword123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "admin@example.com"

@pytest.mark.asyncio
async def test_login_admin(async_client: AsyncClient):
    await async_client.post(
        "/api/v1/auth/register",
        json={"username": "admin2", "email": "admin2@example.com", "password": "StrongPassword123"}
    )
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "admin2@example.com", "password": "StrongPassword123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_submit_feedback(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/feedbacks",
        json={"title": "UI Bug", "message": "The button is misaligned"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "submitted"

@pytest.mark.asyncio
async def test_admin_flow(async_client: AsyncClient):
    # 1. Register and Login
    await async_client.post("/api/v1/auth/register", json={"username": "admin3", "email": "admin3@example.com", "password": "StrongPassword123"})
    login_resp = await async_client.post("/api/v1/auth/login", json={"email": "admin3@example.com", "password": "StrongPassword123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Feedback
    fb_resp = await async_client.post("/api/v1/feedbacks", json={"title": "Test", "message": "Message Test"})
    fb_id = fb_resp.json()["id"]

    # 3. List Feedbacks
    list_resp = await async_client.get("/api/v1/feedbacks", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # 4. Update Feedback Status
    patch_resp = await async_client.patch(f"/api/v1/feedbacks/{fb_id}/status", json={"status": "under_review"}, headers=headers)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "under_review"