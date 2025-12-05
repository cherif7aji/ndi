from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services.submission_service import SubmissionService
from schemas import ExerciceSubmission, NoteCalculeeResponse
from models import Utilisateur
from .auth_controller import get_current_active_user

router = APIRouter(prefix="/submissions", tags=["Submissions"])

def get_submission_service(db: Session = Depends(get_db)) -> SubmissionService:
    return SubmissionService(db)

@router.post("/exercice", response_model=NoteCalculeeResponse, status_code=status.HTTP_201_CREATED)
def soumettre_exercice(
    submission: ExerciceSubmission,
    current_user: Utilisateur = Depends(get_current_active_user),
    submission_service: SubmissionService = Depends(get_submission_service)
):
    """Soumettre les réponses d'un exercice et calculer la note"""
    return submission_service.soumettre_exercice(current_user.id, submission)

@router.get("/mes-notes", response_model=List[dict])
def get_mes_notes(
    current_user: Utilisateur = Depends(get_current_active_user),
    submission_service: SubmissionService = Depends(get_submission_service)
):
    """Récupérer toutes mes notes"""
    return submission_service.get_user_notes(current_user.id)

@router.get("/exercice/{exercice_id}/note")
def get_note_exercice(
    exercice_id: int,
    current_user: Utilisateur = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer ma note pour un exercice spécifique"""
    from models import Note
    
    note = db.query(Note).filter(
        Note.utilisateur_id == current_user.id,
        Note.exercice_id == exercice_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No note found for this exercise"
        )
    
    return {
        "id": note.id,
        "exercice_id": note.exercice_id,
        "historique_notes": note.historique_notes or [],
        "note_actuelle": note.note_actuelle,
        "meilleure_note": note.meilleure_note,
        "note_maximale": note.note_maximale,
        "pourcentage_actuel": round(note.pourcentage_actuel, 2),
        "temps_passe": note.temps_passe,
        "nombre_tentatives": note.nombre_tentatives,
        "completed_at": note.completed_at
    }

# Export du router
submission_router = router
