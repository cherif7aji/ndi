from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from fastapi import UploadFile

class CoursBase(BaseModel):
    titre: str
    description: Optional[str] = None
    niveau: Optional[str] = None
    duree_estimee: Optional[int] = None

class CoursCreate(CoursBase):
    pass

class CoursUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    niveau: Optional[str] = None
    duree_estimee: Optional[int] = None

class CoursResponse(CoursBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Schémas pour création avec contenu
class CoursCreateWithContent(CoursBase):
    """Créer un cours avec son contenu"""
    paragraphes: List[dict] = Field(default_factory=list)
    videos: List[dict] = Field(default_factory=list)
    images: List[dict] = Field(default_factory=list)

class CoursWithContentResponse(CoursResponse):
    """Cours avec son contenu complet"""
    paragraphes: Optional[List[dict]] = []
    videos: Optional[List[dict]] = []
    images: Optional[List[dict]] = []
    exercices: Optional[List[dict]] = []

class CoursCreateWithFiles(CoursBase):
    """Créer un cours avec upload de fichiers"""
    pass

class CoursCreateComplete(BaseModel):
    """Créer un cours avec tout le contenu en JSON"""
    titre: str
    description: Optional[str] = None
    niveau: Optional[str] = None
    duree_estimee: Optional[int] = None
    paragraphes: Optional[List[dict]] = []
    videos: Optional[List[dict]] = []
    images_base64: Optional[List[dict]] = []  # Images encodées en base64
