from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from .database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, default="Untitled")
    content = Column(Text, nullable=False, default="")
    is_public = Column(Boolean, nullable=False, default=False)
    share_id = Column(String(64), index=True, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
