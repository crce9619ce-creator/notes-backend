from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
from typing import Optional

def get_notes(db: Session):
    return db.execute(select(models.Note).order_by(models.Note.updated_at.desc())).scalars().all()

def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    return db.get(models.Note, note_id)

def get_note_by_share_id(db: Session, share_id: str) -> Optional[models.Note]:
    stmt = select(models.Note).where(models.Note.share_id == share_id, models.Note.is_public == True)
    return db.execute(stmt).scalars().first()

def create_note(db: Session, data: schemas.NoteCreate) -> models.Note:
    note = models.Note(title=data.title, content=data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def update_note(db: Session, note: models.Note, data: schemas.NoteUpdate) -> models.Note:
    if data.title is not None:
        note.title = data.title
    if data.content is not None:
        note.content = data.content
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note: models.Note) -> None:
    db.delete(note)
    db.commit()
