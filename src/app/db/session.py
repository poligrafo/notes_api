from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.app.core.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL, echo=False, future=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
