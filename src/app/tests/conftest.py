import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from main import app
from src.app.db.models import Base
from src.app.api.dependencies.deps import get_db


TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5434/test_db"

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Создает тестовую БД перед запуском всех тестов и очищает после"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    """Создает новую сессию БД для каждого теста"""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncClient:
    """HTTP-клиент с подмененной зависимостью `get_db`"""
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(base_url="http://localhost:8008") as client:
        yield client

    app.dependency_overrides.clear()


