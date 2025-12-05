from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Paragraphe
from schemas import ParagrapheCreate, ParagrapheResponse, ParagrapheUpdate

class ParagrapheService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_paragraphe(self, paragraphe_data: ParagrapheCreate) -> Paragraphe:
        """Créer un nouveau paragraphe"""
        db_paragraphe = Paragraphe(**paragraphe_data.dict())
        self.db.add(db_paragraphe)
        self.db.commit()
        self.db.refresh(db_paragraphe)
        return db_paragraphe
    
    def get_paragraphe_by_id(self, paragraphe_id: int) -> Paragraphe:
        """Récupérer un paragraphe par ID"""
        paragraphe = self.db.query(Paragraphe).filter(Paragraphe.id == paragraphe_id).first()
        if not paragraphe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paragraphe not found"
            )
        return paragraphe
    
    def get_all_paragraphes(self) -> List[Paragraphe]:
        """Récupérer tous les paragraphes"""
        return self.db.query(Paragraphe).all()
    
    def update_paragraphe(self, paragraphe_id: int, paragraphe_data: ParagrapheUpdate) -> Paragraphe:
        """Mettre à jour un paragraphe"""
        paragraphe = self.get_paragraphe_by_id(paragraphe_id)
        
        update_data = paragraphe_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(paragraphe, field):
                setattr(paragraphe, field, value)
        
        self.db.commit()
        self.db.refresh(paragraphe)
        return paragraphe
    
    def delete_paragraphe(self, paragraphe_id: int) -> bool:
        """Supprimer un paragraphe"""
        paragraphe = self.get_paragraphe_by_id(paragraphe_id)
        self.db.delete(paragraphe)
        self.db.commit()
        return True
