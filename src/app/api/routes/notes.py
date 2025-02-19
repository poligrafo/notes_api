from typing import Sequence, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies.deps import get_current_user, get_db
from src.app.schemas.note_schemas import NoteCreateSchema, NoteUpdateSchema, NoteSchema
from src.app.db.models import Note, User

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("", response_model=NoteSchema)
async def create_note(
    note_data: NoteCreateSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> Note:
    """Создание заметки (только для текущего пользователя)"""
    new_note = Note(title=note_data.title, body=note_data.body, user_id=user.id, is_deleted=False)
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note


@router.get("", response_model=list[NoteSchema])
async def get_my_notes(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> Sequence[Note]:
    """Получение всех заметок текущего пользователя"""
    result = await session.execute(select(Note).where(Note.user_id == user.id, Note.is_deleted.is_(False)))
    return result.scalars().all()


@router.get("/{note_id}", response_model=NoteSchema)
async def get_note(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> Optional[Note]:
    """Получение одной заметки (только своей)"""
    note = await session.get(Note, note_id)
    if not note or note.user_id != user.id or note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteSchema)
async def update_note(
    note_id: int,
    note_data: NoteUpdateSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> Optional[Note]:
    """Обновление заметки (только своей)"""
    note = await session.get(Note, note_id)
    if not note or note.user_id != user.id or note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    updated = False

    if note_data.title is not None:
        note.title = note_data.title
        updated = True
    if note_data.body is not None:
        note.body = note_data.body
        updated = True

    if updated:
        await session.commit()
        await session.refresh(note)

    return note


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> dict:
    """Удаление заметки (пользователь помечает, но не удаляет)"""
    note = await session.get(Note, note_id)
    if not note or note.user_id != user.id or note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    note.is_deleted = True
    await session.commit()
    return {"message": "Note deleted"}