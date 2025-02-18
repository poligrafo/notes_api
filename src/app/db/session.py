from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


engine = create_async_engine(settings.get_db_url(), echo=False, future=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Декоратор для автоматического управления сессиями
def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
