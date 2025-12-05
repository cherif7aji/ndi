from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Image
from schemas import ImageCreate, ImageResponse, ImageUpdate

class ImageService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_image(self, image_data: ImageCreate) -> Image:
        """Créer une nouvelle image"""
        db_image = Image(**image_data.dict())
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        return db_image
    
    def get_image_by_id(self, image_id: int) -> Image:
        """Récupérer une image par ID"""
        image = self.db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        return image
    
    def get_all_images(self) -> List[Image]:
        """Récupérer toutes les images"""
        return self.db.query(Image).all()
    
    def update_image(self, image_id: int, image_data: ImageUpdate) -> Image:
        """Mettre à jour une image"""
        image = self.get_image_by_id(image_id)
        
        update_data = image_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(image, field):
                setattr(image, field, value)
        
        self.db.commit()
        self.db.refresh(image)
        return image
    
    def delete_image(self, image_id: int) -> bool:
        """Supprimer une image"""
        image = self.get_image_by_id(image_id)
        self.db.delete(image)
        self.db.commit()
        return True
