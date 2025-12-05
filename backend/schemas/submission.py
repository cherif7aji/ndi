from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReponseSubmission(BaseModel):
    """Réponse soumise par l'utilisateur"""
    question_id: int
    reponse_utilisateur: str

class ExerciceSubmission(BaseModel):
    """Soumission complète d'un exercice"""
    exercice_id: int
    reponses: List[ReponseSubmission]
    temps_passe: Optional[int] = None  # en secondes

class NoteCalculeeResponse(BaseModel):
    """Réponse avec la note calculée"""
    id: int
    exercice_id: int
    historique_notes: List[float]  # Liste des notes [récente, ancienne, ...]
    note_actuelle: float  # Note la plus récente
    note_obtenue: Optional[float] = None  # Alias pour le frontend
    meilleure_note: float  # Meilleure note de l'historique
    note_maximale: float
    pourcentage_actuel: float  # Pourcentage de la note actuelle
    pourcentage_obtenu: Optional[float] = None  # Alias pour le frontend
    temps_passe: Optional[int]
    nombre_tentatives: int
    completed_at: datetime
    
    # Détails de la dernière soumission
    total_questions: int
    nombre_questions: Optional[int] = None  # Alias pour le frontend
    bonnes_reponses: int
    nombre_bonnes_reponses: Optional[int] = None  # Alias pour le frontend
    mauvaises_reponses: int
    
    class Config:
        from_attributes = True
