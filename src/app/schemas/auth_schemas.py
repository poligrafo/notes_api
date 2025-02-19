from typing import Literal

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Схема JWT-токена"""
    access_token: str
    token_type: str = "bearer"


class UserCreateSchema(BaseModel):
    """Схема регистрации пользователя"""
    username: str
    password: str
    role: Literal["User", "Admin"] = "User"


class UserSchema(BaseModel):
    """Схема ответа о пользователе"""
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True
