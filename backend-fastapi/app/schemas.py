from pydantic import BaseModel, Field
from typing import Optional

class NoteBase(BaseModel):
    title: str = Field(default="Untitled", max_length=200)
    content: str = ""

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteOut(NoteBase):
    id: int
    is_public: bool
    share_id: Optional[str] = None

    class Config:
        from_attributes = True

class ShareToggleOut(BaseModel):
    id: int
    is_public: bool
    share_url: str
