import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_get_all_notes(async_client: AsyncClient):
    """Тест получения всех заметок (админ)"""
    login_response = await async_client.post("/auth/login", json={
        "username": "admin",
        "password": "adminpassword"
    })
    token = login_response.json()["access_token"]

    response = await async_client.get("/admin/notes", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_admin_restore_note(async_client: AsyncClient):
    """Тест восстановления удаленной заметки (админ)"""

    # Логинимся под админом
    login_response = await async_client.post("/auth/login", json={"username": "admin", "password": "adminpassword"})
    assert login_response.status_code == 200, f"Admin login failed: {login_response.json()}"
    token = login_response.json()["access_token"]

    # Создаем заметку
    note_response = await async_client.post(
        "/notes",
        json={"title": "Deleted Note", "body": "This note will be deleted"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert note_response.status_code == 200, f"Note creation failed: {note_response.json()}"
    note_id = note_response.json()["id"]

    # Удаляем заметку
    delete_response = await async_client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200, f"Note deletion failed: {delete_response.json()}"

    # Восстанавливаем заметку
    restore_response = await async_client.put(
        f"/admin/notes/{note_id}/restore",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert restore_response.status_code == 200, f"Note restore failed: {restore_response.json()}"

