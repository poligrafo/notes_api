from typing import Literal

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
