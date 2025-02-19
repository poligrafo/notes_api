# Notes API - Управление заметками

Notes API - это асинхронный API-сервис на FastAPI, который позволяет пользователям создавать, редактировать и удалять заметки с разграничением ролей (`User`, `Admin`).

## Используемый стек:
- **FastAPI** - асинхронный веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** + **Alembic** - ORM и миграции
- **Poetry** - управление зависимостями
- **Docker** + **Docker Compose** - контейнеризация
- **Pytest** + **HTTPX** - тестирование API

---

## 1 Настройка окружения

1. **Склонируйте репозиторий**:
   ```bash
   git clone https://github.com/your-username/notes-api.git
   cd notes-api
   ```

2. **Создайте файл .env на основе .env.example:**
   ```bash
   cp .env.example .env
   ```
3. Заполните .env своими данными (пример):
   ```bash
    DB_USER=postgres
    DB_PASSWORD=yourpassword
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=notes_db
    
    JWT_SECRET_KEY=supersecretkey
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60

   ```
## 2 Запуск проекта (Docker)

Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```
Проект запустится на http://localhost:8008.

## 3 Документация API
 Swagger UI доступен по адресу:
-> http://localhost:8008/docs

Redoc (альтернативная документация):
-> http://localhost:8008/redoc