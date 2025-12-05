from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import UtilisateurService
from schemas import UtilisateurCreate, UtilisateurResponse, UtilisateurUpdate
from models import Utilisateur
from .auth_controller import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_utilisateur_service(db: Session = Depends(get_db)) -> UtilisateurService:
    return UtilisateurService(db)

@router.post("/", response_model=UtilisateurResponse, status_code=status.HTTP_201_CREATED)
def create_utilisateur(
    utilisateur_data: UtilisateurCreate,
    current_user: Utilisateur = Depends(get_current_active_user),
    utilisateur_service: UtilisateurService = Depends(get_utilisateur_service)
):
    """Créer un nouvel utilisateur"""
    return utilisateur_service.create_utilisateur(utilisateur_data)

@router.get("/{utilisateur_id}", response_model=UtilisateurResponse)
def get_utilisateur_by_id(
    utilisateur_id: int,
    utilisateur_service: UtilisateurService = Depends(get_utilisateur_service)
):
    """Récupérer un utilisateur par ID"""
    return utilisateur_service.get_utilisateur_by_id(utilisateur_id)

@router.get("/", response_model=List[UtilisateurResponse])
def get_all_utilisateurs(
    utilisateur_service: UtilisateurService = Depends(get_utilisateur_service)
):
    """Récupérer tous les utilisateurs"""
    return utilisateur_service.get_all_utilisateurs()

@router.put("/{utilisateur_id}", response_model=UtilisateurResponse)
def update_utilisateur(
    utilisateur_id: int,
    utilisateur_data: UtilisateurUpdate,
    current_user: Utilisateur = Depends(get_current_active_user),
    utilisateur_service: UtilisateurService = Depends(get_utilisateur_service)
):
    """Mettre à jour un utilisateur"""
    return utilisateur_service.update_utilisateur(utilisateur_id, utilisateur_data.dict(exclude_unset=True))

@router.delete("/{utilisateur_id}")
def delete_utilisateur(
    utilisateur_id: int,
    current_user: Utilisateur = Depends(get_current_active_user),
    utilisateur_service: UtilisateurService = Depends(get_utilisateur_service)
):
    """Supprimer un utilisateur"""
    utilisateur_service.delete_utilisateur(utilisateur_id)
    return {"message": "Utilisateur deleted successfully"}

# Export du router
utilisateur_router = router
