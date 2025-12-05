from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Note
from schemas import NoteCreate, NoteResponse, NoteUpdate

class NoteService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_note(self, note_data: NoteCreate) -> Note:
        """Créer une nouvelle note"""
        db_note = Note(**note_data.dict())
        self.db.add(db_note)
        self.db.commit()
        self.db.refresh(db_note)
        return db_note
    
    def get_note_by_id(self, note_id: int) -> Note:
        """Récupérer une note par ID"""
        note = self.db.query(Note).filter(Note.id == note_id).first()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note
    
    def get_all_notes(self) -> List[Note]:
        """Récupérer toutes les notes"""
        return self.db.query(Note).all()
    
    def update_note(self, note_id: int, note_data: NoteUpdate) -> Note:
        """Mettre à jour une note"""
        note = self.get_note_by_id(note_id)
        
        update_data = note_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(note, field):
                setattr(note, field, value)
        
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def delete_note(self, note_id: int) -> bool:
        """Supprimer une note"""
        note = self.get_note_by_id(note_id)
        self.db.delete(note)
        self.db.commit()
        return True
