from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies.auth_deps import require_role, get_db
from src.app.schemas.note_schemas import NoteSchema
from src.app.db.models import Note

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/notes", response_model=list[NoteSchema])
async def get_all_notes(
    session: AsyncSession = Depends(get_db),
    _: str = Depends(require_role("Admin"))
):
    """Администратор получает все заметки (включая удаленные)"""
    result = await session.execute(select(Note))
    return result.scalars().all()


@router.get("/notes/{note_id}", response_model=NoteSchema)
async def get_specific_note(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    _: str = Depends(require_role("Admin"))
):
    """Администратор получает конкретную заметку"""
    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.get("/users/{user_id}/notes", response_model=list[NoteSchema])
async def get_user_notes(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    _: str = Depends(require_role("Admin"))
):
    """Администратор получает все заметки конкретного пользователя"""
    result = await session.execute(select(Note).where(Note.user_id == user_id))
    return result.scalars().all()


@router.put("/notes/{note_id}/restore")
async def restore_note(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    _: str = Depends(require_role("Admin"))
):
    """Администратор восстанавливает удаленную заметку"""
    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if not note.is_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note is not deleted")

    note.is_deleted = False
    await session.commit()
    return {"message": "Note restored"}
