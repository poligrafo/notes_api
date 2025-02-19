import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    """Тест регистрации нового пользователя"""
    response = await async_client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200, f"Register failed: {response.json()}"



@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    """Тест логина"""
    response = await async_client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
