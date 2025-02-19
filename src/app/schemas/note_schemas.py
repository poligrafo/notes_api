from pydantic import BaseModel, ConfigDict
from typing import Optional


class NoteCreateSchema(BaseModel):
    """Схема для создания заметки"""
    title: str
    body: str


class NoteUpdateSchema(BaseModel):
    """Схема для обновления заметки"""
    title: Optional[str] = None
    body: Optional[str] = None


class NoteSchema(BaseModel):
    """Схема ответа о заметке"""
    id: int
    title: str
    body: str
    user_id: int
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
