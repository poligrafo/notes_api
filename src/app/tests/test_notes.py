import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_note(async_client: AsyncClient):
    """Тест создания заметки"""
    login_response = await async_client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    response = await async_client.post("/notes", json={
        "title": "Test Note",
        "body": "This is a test note"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"


@pytest.mark.asyncio
async def test_get_notes(async_client: AsyncClient):
    """Тест получения всех заметок пользователя"""
    login_response = await async_client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    response = await async_client.get("/notes", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_note(async_client: AsyncClient):
    """Тест обновления заметки"""

    # Логинимся
    login_response = await async_client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"User login failed: {login_response.json()}"
    token = login_response.json()["access_token"]

    # Создаем заметку
    note_response = await async_client.post(
        "/notes",
        json={"title": "Old Title", "body": "Old Body"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert note_response.status_code == 200, f"Note creation failed: {note_response.json()}"
    note_id = note_response.json()["id"]

    # Обновляем заметку
    update_response = await async_client.put(
        f"/notes/{note_id}",
        json={"title": "Updated Title", "body": "Updated Body"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == 200, f"Note update failed: {update_response.json()}"
    assert update_response.json()["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_note(async_client: AsyncClient):
    """Тест удаления заметки"""

    # Логинимся
    login_response = await async_client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    token = login_response.json()["access_token"]

    # Создаем заметку перед удалением
    create_response = await async_client.post(
        "/notes",
        json={"title": "Temporary Note", "body": "This note will be deleted"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200, f"Note creation failed: {create_response.json()}"
    note_id = create_response.json()["id"]

    # Удаляем заметку
    delete_response = await async_client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200, f"Note deletion failed: {delete_response.json()}"
    assert delete_response.json()["message"] == "Note deleted"

    # Проверяем, что заметки больше нет
    get_response = await async_client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404, "Note should not exist after deletion"

