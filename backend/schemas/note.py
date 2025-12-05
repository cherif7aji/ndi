from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteBase(BaseModel):
    note_obtenue: float
    note_maximale: float
    temps_passe: Optional[int] = None
    nombre_tentatives: int = 1

class NoteCreate(NoteBase):
    exercice_id: int

class NoteUpdate(BaseModel):
    note_obtenue: Optional[float] = None
    note_maximale: Optional[float] = None
    pourcentage: Optional[float] = None
    temps_passe: Optional[int] = None
    nombre_tentatives: Optional[int] = None

class NoteResponse(NoteBase):
    id: int
    utilisateur_id: int
    exercice_id: int
    completed_at: datetime
    
    class Config:
        from_attributes = True
