from typing import Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.core.security import decode_access_token
from src.app.db.session import async_session_maker
from src.app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    """Асинхронный Dependency для получения сессии БД"""
    async with async_session_maker() as session:
        yield session


async def get_current_user(
        token: str = Security(oauth2_scheme),
        session: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Получаем текущего пользователя по JWT"""
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user: Optional[User] = await session.get(User, int(payload["sub"]))

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def require_role(role: str):
    """Проверка ролей (работает как FastAPI Dependency)"""
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return role_checker
