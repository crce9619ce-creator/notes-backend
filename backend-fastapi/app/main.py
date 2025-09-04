import os, uuid
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import models, schemas, crud

BASE_PUBLIC_URL = os.getenv("BASE_PUBLIC_URL")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API", version="1.0.0")

# CORS
allowed = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in allowed.split(",")] if allowed else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/notes", response_model=list[schemas.NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)

@app.post("/notes", response_model=schemas.NoteOut, status_code=201)
def create_note(data: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, data)

@app.get("/notes/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    return note

@app.put("/notes/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, data: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    return crud.update_note(db, note, data)

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    crud.delete_note(db, note)
    return

def _build_share_url(share_id: str) -> str:
    base = BASE_PUBLIC_URL.rstrip("/") if BASE_PUBLIC_URL else ""
    # If BASE_PUBLIC_URL is set, expose API URL; frontend will convert to its public route.
    return f"{base}/public/{share_id}" if base else f"/public/{share_id}"

@app.post("/notes/{note_id}/share", response_model=schemas.ShareToggleOut)
def toggle_share(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    if note.is_public and note.share_id:
        # turn off sharing
        note.is_public = False
        note.share_id = None
    else:
        # turn on sharing
        note.is_public = True
        note.share_id = uuid.uuid4().hex
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"id": note.id, "is_public": note.is_public, "share_url": _build_share_url(note.share_id) if note.is_public else ""}

@app.get("/public/{share_id}", response_model=schemas.NoteOut)
def view_public(share_id: str, db: Session = Depends(get_db)):
    note = crud.get_note_by_share_id(db, share_id)
    if not note:
        raise HTTPException(404, "Public note not found")
    return note
