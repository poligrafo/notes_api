from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies.auth_deps import get_db, get_current_user
from src.app.core.security import hash_password, verify_password, create_access_token
from src.app.schemas.auth_schemas import UserCreateSchema, TokenSchema, UserSchema
from src.app.db.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserSchema)
async def register(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)):
    """Регистрация пользователя"""
    existing_user = await session.execute(select(User).where(User.username == user_data.username))
    user = existing_user.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    role = user_data.role if hasattr(user_data, "role") and user_data.role in ["User", "Admin"] else "User"

    new_user = User(username=user_data.username, password_hash=hash_password(user_data.password), role=role)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)):
    """Авторизация пользователя"""
    user_result = await session.execute(select(User).where(User.username == user_data.username))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    password_hash = user.password_hash

    if not verify_password(user_data.password, password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
async def get_me(user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return user
