from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies.auth_deps import require_role
from src.app.schemas.note_schemas import NoteSchema
from src.app.db.models import Note, User
from src.app.db.session import connection

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/notes", response_model=list[NoteSchema])
@connection
async def get_all_notes(session: AsyncSession = None, _: User = Depends(require_role("Admin"))):
    """Администратор получает все заметки (включая удаленные)"""
    result = await session.execute(select(Note))
    return result.scalars().all()


@router.get("/notes/{note_id}", response_model=NoteSchema)
@connection
async def get_specific_note(note_id: int, session: AsyncSession = None, _: User = Depends(require_role("Admin"))):
    """Администратор получает конкретную заметку"""
    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.get("/users/{user_id}/notes", response_model=list[NoteSchema])
@connection
async def get_user_notes(user_id: int, session: AsyncSession = None, _: User = Depends(require_role("Admin"))):
    """Администратор получает все заметки конкретного пользователя"""
    result = await session.execute(select(Note).where(Note.user_id == user_id))
    return result.scalars().all()


@router.put("/notes/{note_id}/restore")
@connection
async def restore_note(note_id: int, session: AsyncSession = None, _: User = Depends(require_role("Admin"))):
    """Администратор восстанавливает удаленную заметку"""
    note = await session.get(Note, note_id)
    if not note or not note.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or not deleted")

    note.is_deleted = False
    await session.commit()
    return {"message": "Note restored"}