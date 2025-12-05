from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class ParagrapheBase(BaseModel):
    titre: str
    contenu: str
    type_paragraphe: Optional[str] = None  # introduction, explication, exemple, conclusion, instruction
    est_visible: bool = True
    ordre: int = 1

class ParagrapheCreate(ParagrapheBase):
    cours_id: Optional[int] = None
    exercice_id: Optional[int] = None
    
    @model_validator(mode='after')
    def validate_parent_reference(self):
        """Valider qu'au moins une référence parent est fournie"""
        cours_id = self.cours_id
        exercice_id = self.exercice_id
        
        # Exactement une des deux références doit être fournie
        if not cours_id and not exercice_id:
            raise ValueError('cours_id ou exercice_id doit être fourni')
        if cours_id and exercice_id:
            raise ValueError('cours_id et exercice_id ne peuvent pas être fournis en même temps')
        
        return self

class ParagrapheUpdate(BaseModel):
    titre: Optional[str] = None
    contenu: Optional[str] = None
    type_paragraphe: Optional[str] = None
    est_visible: Optional[bool] = None
    ordre: Optional[int] = None

class ParagrapheResponse(ParagrapheBase):
    id: int
    cours_id: Optional[int] = None
    exercice_id: Optional[int] = None
    
    class Config:
        from_attributes = True
