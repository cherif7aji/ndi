from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class ImageBase(BaseModel):
    titre: Optional[str] = None
    nom_fichier: str
    extension: str  # .jpg, .png, etc.
    alt_text: Optional[str] = None
    description: Optional[str] = None
    type_image: Optional[str] = None  # illustration, screenshot, diagram, solution, hint
    taille_fichier: Optional[int] = None
    largeur: Optional[int] = None
    hauteur: Optional[int] = None
    ordre: int = 1

class ImageUpload(BaseModel):
    """Schéma pour l'upload d'image avec contenu Base64"""
    cours_id: Optional[int] = None
    exercice_id: Optional[int] = None
    titre: Optional[str] = None
    nom_fichier: str
    extension: str
    alt_text: Optional[str] = None
    description: Optional[str] = None
    type_image: Optional[str] = None
    contenu_base64: str  # Contenu de l'image en Base64
    ordre: int = 1
    
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

class ImageCreate(ImageBase):
    cours_id: Optional[int] = None
    exercice_id: Optional[int] = None
    contenu_base64: str  # Contenu de l'image en Base64
    
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

class ImageUpdate(BaseModel):
    titre: Optional[str] = None
    alt_text: Optional[str] = None
    description: Optional[str] = None
    type_image: Optional[str] = None
    ordre: Optional[int] = None

class ImageResponse(ImageBase):
    id: int
    cours_id: Optional[int] = None
    exercice_id: Optional[int] = None
    contenu_base64: Optional[str] = None  # Inclure le contenu base64 pour l'affichage
    
    class Config:
        from_attributes = True

class ImageWithContent(ImageResponse):
    """Image avec son contenu Base64 pour téléchargement"""
    contenu_base64: str
    
    class Config:
        from_attributes = True
