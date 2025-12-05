from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import uuid
import base64

from database import get_db
from services import CoursService
from schemas import CoursCreate, CoursResponse, CoursUpdate, CoursCreateWithContent, CoursWithContentResponse, CoursCreateComplete
from models import Utilisateur
from .auth_controller import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/cours", tags=["Cours"])

def get_cours_service(db: Session = Depends(get_db)) -> CoursService:
    return CoursService(db)

@router.post("/", response_model=CoursResponse, status_code=status.HTTP_201_CREATED)
def create_cours(
    cours_data: CoursCreate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    cours_service: CoursService = Depends(get_cours_service)
):
    """Créer un nouveau cours (admin seulement)"""
    return cours_service.create_cours(cours_data)

@router.get("/{cours_id}", response_model=CoursResponse)
def get_cours_by_id(
    cours_id: int,
    cours_service: CoursService = Depends(get_cours_service)
):
    """Récupérer un cours par ID"""
    return cours_service.get_cours_by_id(cours_id)

@router.get("/", response_model=List[CoursResponse])
def get_all_cours(
    cours_service: CoursService = Depends(get_cours_service)
):
    """Récupérer tous les cours"""
    return cours_service.get_all_cours()

@router.put("/{cours_id}", response_model=CoursResponse)
def update_cours(
    cours_id: int,
    cours_data: CoursUpdate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    cours_service: CoursService = Depends(get_cours_service)
):
    """Mettre à jour un cours (admin seulement)"""
    return cours_service.update_cours(cours_id, cours_data)

@router.delete("/{cours_id}")
def delete_cours(
    cours_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    cours_service: CoursService = Depends(get_cours_service)
):
    """Supprimer un cours"""
    cours_service.delete_cours(cours_id)
    return {"message": "Cours deleted successfully"}

# ===== ENDPOINTS AVEC CONTENU =====

@router.post("/with-content", response_model=CoursWithContentResponse, status_code=status.HTTP_201_CREATED)
def create_cours_with_content(
    cours_data: CoursCreateWithContent,
    current_user: Utilisateur = Depends(get_current_admin_user),
    cours_service: CoursService = Depends(get_cours_service)
):
    """Créer un cours avec contenu complet en JSON - Admin seulement"""
    return cours_service.create_cours_with_content(cours_data)

@router.get("/{cours_id}/with-content", response_model=CoursWithContentResponse)
def get_cours_with_content(
    cours_id: int,
    cours_service: CoursService = Depends(get_cours_service)
):
    """Récupérer un cours avec tout son contenu"""
    return cours_service.get_cours_with_content(cours_id)

@router.put("/{cours_id}/with-content", response_model=CoursWithContentResponse)
def update_cours_with_content(
    cours_id: int,
    cours_data: CoursCreateWithContent,
    current_user: Utilisateur = Depends(get_current_admin_user),
    cours_service: CoursService = Depends(get_cours_service)
):
    """Mettre à jour un cours et son contenu - Admin seulement"""
    return cours_service.update_cours_with_content(cours_id, cours_data)

@router.delete("/{cours_id}/with-content")
def delete_cours_with_content(
    cours_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    cours_service: CoursService = Depends(get_cours_service)
):
    """Supprimer un cours et tout son contenu - Admin seulement"""
    cours_service.delete_cours(cours_id)
    return {"message": "Cours and all content deleted successfully"}

@router.get("/content/all", response_model=List[CoursWithContentResponse])
def get_all_cours_with_content(
    cours_service: CoursService = Depends(get_cours_service)
):
    """Récupérer tous les cours avec leur contenu complet"""
    return cours_service.get_all_cours_with_content()

# Export du router
cours_router = router
