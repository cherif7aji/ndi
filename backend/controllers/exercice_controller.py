from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import ExerciceService
from schemas import ExerciceCreate, ExerciceResponse, ExerciceUpdate, ExerciceWithContentResponse, ExerciceCreateWithContent
from models import Utilisateur
from .auth_controller import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/exercices", tags=["Exercices"])

def get_exercice_service(db: Session = Depends(get_db)) -> ExerciceService:
    return ExerciceService(db)

@router.post("/", response_model=ExerciceResponse, status_code=status.HTTP_201_CREATED)
def create_exercice(
    exercice_data: ExerciceCreate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Créer un nouvel exercice (admin seulement)"""
    return exercice_service.create_exercice(exercice_data)

@router.get("/{exercice_id}", response_model=ExerciceResponse)
def get_exercice_by_id(
    exercice_id: int,
    current_user: Utilisateur = Depends(get_current_active_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Récupérer un exercice par ID"""
    return exercice_service.get_exercice_by_id(exercice_id)

@router.get("/", response_model=List[ExerciceResponse])
def get_all_exercices(
    current_user: Utilisateur = Depends(get_current_active_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Récupérer tous les exercices"""
    return exercice_service.get_all_exercices()

@router.put("/{exercice_id}", response_model=ExerciceResponse)
def update_exercice(
    exercice_id: int,
    exercice_data: ExerciceUpdate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Mettre à jour un exercice (admin seulement)"""
    return exercice_service.update_exercice(exercice_id, exercice_data)

@router.delete("/{exercice_id}")
def delete_exercice(
    exercice_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Supprimer un exercice"""
    exercice_service.delete_exercice(exercice_id)
    return {"message": "Exercice deleted successfully"}

# ============ WITH-CONTENT ENDPOINTS ============

@router.post("/with-content", response_model=ExerciceWithContentResponse, status_code=status.HTTP_201_CREATED)
def create_exercice_with_content(
    exercice_data: ExerciceCreateWithContent,
    current_user: Utilisateur = Depends(get_current_admin_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Créer un exercice avec tout son contenu (questions, solutions, paragraphes, vidéos, images) - Admin seulement"""
    return exercice_service.create_exercice_with_content(exercice_data)

@router.get("/{exercice_id}/with-content", response_model=ExerciceWithContentResponse)
def get_exercice_with_content(
    exercice_id: int,
    current_user: Utilisateur = Depends(get_current_active_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Récupérer un exercice avec tout son contenu"""
    return exercice_service.get_exercice_with_content(exercice_id)

@router.put("/{exercice_id}/with-content", response_model=ExerciceWithContentResponse)
def update_exercice_with_content(
    exercice_id: int,
    exercice_data: ExerciceCreateWithContent,
    current_user: Utilisateur = Depends(get_current_admin_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Mettre à jour un exercice et son contenu - Admin seulement"""
    return exercice_service.update_exercice_with_content(exercice_id, exercice_data)

@router.delete("/{exercice_id}/with-content")
def delete_exercice_with_content(
    exercice_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Supprimer un exercice et tout son contenu - Admin seulement"""
    exercice_service.delete_exercice(exercice_id)
    return {"message": "Exercice and all content deleted successfully"}

@router.get("/content/all", response_model=List[ExerciceWithContentResponse])
def get_all_exercices_with_content(
    current_user: Utilisateur = Depends(get_current_active_user),
    exercice_service: ExerciceService = Depends(get_exercice_service)
):
    """Récupérer tous les exercices avec leur contenu complet"""
    return exercice_service.get_all_exercices_with_content()

# Export du router
exercice_router = router
