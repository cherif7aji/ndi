from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import ImageService
from schemas import ImageCreate, ImageResponse, ImageUpdate
from models import Utilisateur
from .auth_controller import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/images", tags=["Images"])

def get_image_service(db: Session = Depends(get_db)) -> ImageService:
    return ImageService(db)

@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
def create_image(
    image_data: ImageCreate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    image_service: ImageService = Depends(get_image_service)
):
    """Créer une nouvelle image (admin seulement)"""
    return image_service.create_image(image_data)

@router.get("/{image_id}", response_model=ImageResponse)
def get_image_by_id(
    image_id: int,
    image_service: ImageService = Depends(get_image_service)
):
    """Récupérer une image par ID"""
    return image_service.get_image_by_id(image_id)

@router.get("/", response_model=List[ImageResponse])
def get_all_images(
    image_service: ImageService = Depends(get_image_service)
):
    """Récupérer toutes les images"""
    return image_service.get_all_images()

@router.put("/{image_id}", response_model=ImageResponse)
def update_image(
    image_id: int,
    image_data: ImageUpdate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    image_service: ImageService = Depends(get_image_service)
):
    """Mettre à jour une image (admin seulement)"""
    return image_service.update_image(image_id, image_data)

@router.delete("/{image_id}")
def delete_image(
    image_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    image_service: ImageService = Depends(get_image_service)
):
    """Supprimer une image (admin seulement)"""
    image_service.delete_image(image_id)
    return {"message": "Image deleted successfully"}

# Export du router
image_router = router
