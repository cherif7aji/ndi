from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import VideoService
from schemas import VideoCreate, VideoResponse, VideoUpdate
from models import Utilisateur
from .auth_controller import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/videos", tags=["Videos"])

def get_video_service(db: Session = Depends(get_db)) -> VideoService:
    return VideoService(db)

@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
    video_data: VideoCreate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    video_service: VideoService = Depends(get_video_service)
):
    """Créer une nouvelle vidéo (admin seulement)"""
    return video_service.create_video(video_data)

@router.get("/{video_id}", response_model=VideoResponse)
def get_video_by_id(
    video_id: int,
    video_service: VideoService = Depends(get_video_service)
):
    """Récupérer une vidéo par ID"""
    return video_service.get_video_by_id(video_id)

@router.get("/", response_model=List[VideoResponse])
def get_all_videos(
    video_service: VideoService = Depends(get_video_service)
):
    """Récupérer toutes les vidéos"""
    return video_service.get_all_videos()

@router.put("/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: int,
    video_data: VideoUpdate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    video_service: VideoService = Depends(get_video_service)
):
    """Mettre à jour une vidéo (admin seulement)"""
    return video_service.update_video(video_id, video_data)

@router.delete("/{video_id}")
def delete_video(
    video_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    video_service: VideoService = Depends(get_video_service)
):
    """Supprimer une vidéo (admin seulement)"""
    video_service.delete_video(video_id)
    return {"message": "Video deleted successfully"}

# Export du router
video_router = router
