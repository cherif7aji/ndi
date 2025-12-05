from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import ParagrapheService
from schemas import ParagrapheCreate, ParagrapheResponse, ParagrapheUpdate
from models import Utilisateur
from .auth_controller import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/paragraphes", tags=["Paragraphes"])

def get_paragraphe_service(db: Session = Depends(get_db)) -> ParagrapheService:
    return ParagrapheService(db)

@router.post("/", response_model=ParagrapheResponse, status_code=status.HTTP_201_CREATED)
def create_paragraphe(
    paragraphe_data: ParagrapheCreate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    paragraphe_service: ParagrapheService = Depends(get_paragraphe_service)
):
    """Créer un nouveau paragraphe (admin seulement)"""
    return paragraphe_service.create_paragraphe(paragraphe_data)

@router.get("/{id}", response_model=ParagrapheResponse)
def get_paragraphe_by_id(
    id: int,
    paragraphe_service: ParagrapheService = Depends(get_paragraphe_service)
):
    """Récupérer un paragraphe par ID"""
    return paragraphe_service.get_paragraphe_by_id(id)

@router.get("/", response_model=List[ParagrapheResponse])
def get_all_paragraphes(
    paragraphe_service: ParagrapheService = Depends(get_paragraphe_service)
):
    """Récupérer tous les paragraphes"""
    return paragraphe_service.get_all_paragraphes()

@router.put("/{id}", response_model=ParagrapheResponse)
def update_paragraphe(
    id: int,
    paragraphe_data: ParagrapheUpdate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    paragraphe_service: ParagrapheService = Depends(get_paragraphe_service)
):
    """Mettre à jour un paragraphe (admin seulement)"""
    return paragraphe_service.update_paragraphe(id, paragraphe_data)

@router.delete("/{id}")
def delete_paragraphe(
    id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    paragraphe_service: ParagrapheService = Depends(get_paragraphe_service)
):
    """Supprimer un paragraphe (admin seulement)"""
    paragraphe_service.delete_paragraphe(id)
    return {"message": "Paragraphe deleted successfully"}

# Export du router
paragraphe_router = router
