import pytest


@pytest.mark.asyncio
async def test_create_note(test_client):
    """Тест создания заметки"""
    # Логинимся и получаем токен
    login_response = await test_client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    token = login_response.json()["access_token"]

    # Создаём заметку
    response = await test_client.post("/notes", json={
        "title": "Test Note",
        "body": "This is a test note"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.json()["message"] == "Note created"
