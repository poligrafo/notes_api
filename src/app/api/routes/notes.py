from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies.auth_deps import get_current_user, require_role, get_db
from src.app.schemas.note_schemas import NoteCreateSchema, NoteUpdateSchema, NoteSchema
from src.app.db.models import Note
from src.app.db.models import User
from src.app.db.session import connection

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteSchema)
@connection
async def create_note(
        note_data: NoteCreateSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = None
):
    """Создание заметки (только для текущего пользователя)"""
    new_note = Note(title=note_data.title, body=note_data.body, user_id=user.id)
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note


@router.get("/", response_model=list[NoteSchema])
@connection
async def get_my_notes(user: User = Depends(get_current_user), session: AsyncSession = None):
    """Получение всех заметок текущего пользователя"""
    result = await session.execute(select(Note).where(Note.user_id == user.id, Note.is_deleted == False))
    return result.scalars().all()


@router.get("/{note_id}", response_model=NoteSchema)
@connection
async def get_note(note_id: int, user: User = Depends(get_current_user), session: AsyncSession = None):
    """Получение одной заметки (только своей)"""
    note = await session.get(Note, note_id)
    if not note or note.user_id != user.id or note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteSchema)
@connection
async def update_note(
        note_id: int,
        note_data: NoteUpdateSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = None
):
    """Обновление заметки (только своей)"""
    note = await session.get(Note, note_id)
    if not note or note.user_id != user.id or note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if note_data.title:
        note.title = note_data.title
    if note_data.body:
        note.body = note_data.body

    await session.commit()
    await session.refresh(note)
    return note


@router.delete("/{note_id}")
@connection
async def delete_note(note_id: int, user: User = Depends(get_current_user), session: AsyncSession = None):
    """Удаление заметки (пользователь помечает, но не удаляет)"""
    note = await session.get(Note, note_id)
    if not note or note.user_id != user.id or note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    note.is_deleted = True
    await session.commit()
    return {"message": "Note deleted"}
