from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class VideoBase(BaseModel):
    titre: str
    url_video: str
    description: Optional[str] = None
    type_video: Optional[str] = None  # tutorial, demonstration, solution, explanation
    duree: Optional[int] = None  # en secondes
    thumbnail_url: Optional[str] = None
    plateforme: Optional[str] = None  # youtube, vimeo, local, etc.
    video_id: Optional[str] = None
    ordre: int = 1

class VideoCreate(VideoBase):
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

class VideoUpdate(BaseModel):
    titre: Optional[str] = None
    url_video: Optional[str] = None
    description: Optional[str] = None
    type_video: Optional[str] = None
    duree: Optional[int] = None
    thumbnail_url: Optional[str] = None
    plateforme: Optional[str] = None
    video_id: Optional[str] = None
    ordre: Optional[int] = None

class VideoResponse(VideoBase):
    id: int
    cours_id: Optional[int] = None
    exercice_id: Optional[int] = None
    
    class Config:
        from_attributes = True
