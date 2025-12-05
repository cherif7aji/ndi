from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import QuestionService
from schemas import QuestionCreate, QuestionResponse, QuestionUpdate
from models import Utilisateur
from .auth_controller import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/questions", tags=["Questions"])

def get_question_service(db: Session = Depends(get_db)) -> QuestionService:
    return QuestionService(db)

@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    question_data: QuestionCreate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    question_service: QuestionService = Depends(get_question_service)
):
    """Créer une nouvelle question (admin seulement)"""
    return question_service.create_question(question_data)

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question_by_id(
    question_id: int,
    current_user: Utilisateur = Depends(get_current_active_user),
    question_service: QuestionService = Depends(get_question_service)
):
    """Récupérer une question par ID"""
    return question_service.get_question_by_id(question_id)

@router.get("/", response_model=List[QuestionResponse])
def get_all_questions(
    current_user: Utilisateur = Depends(get_current_active_user),
    question_service: QuestionService = Depends(get_question_service)
):
    """Récupérer toutes les questions"""
    return question_service.get_all_questions()

@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: Utilisateur = Depends(get_current_admin_user),
    question_service: QuestionService = Depends(get_question_service)
):
    """Mettre à jour une question (admin seulement)"""
    return question_service.update_question(question_id, question_data)

@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    current_user: Utilisateur = Depends(get_current_admin_user),
    question_service: QuestionService = Depends(get_question_service)
):
    """Supprimer une question (admin seulement)"""
    question_service.delete_question(question_id)
    return {"message": "Question deleted successfully"}

# Export du router
question_router = router
