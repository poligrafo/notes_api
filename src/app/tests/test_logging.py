import pytest
import os

LOG_FILE = "logs/app.log"


@pytest.mark.asyncio
async def test_logging(test_client):
    """Тест логирования в файл"""
    # Делаем тестовый запрос
    await test_client.get("/")

    # Проверяем, что лог записался
    assert os.path.exists(LOG_FILE), "Файл логов не найден"

    with open(LOG_FILE, "r") as f:
        logs = f.read()
        assert "GET /" in logs, "Запрос не залогировался"
