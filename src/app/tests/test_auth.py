import pytest


@pytest.mark.asyncio
async def test_register_user(test_client):
    """Тест регистрации пользователя"""
    response = await test_client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass",
        "role": "User"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "User created"


@pytest.mark.asyncio
async def test_login_user(test_client):
    """Тест авторизации (получение JWT)"""
    response = await test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

