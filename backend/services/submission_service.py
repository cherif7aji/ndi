from typing import List, Dict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models import Note, Exercice, Question
from schemas import ExerciceSubmission, ReponseSubmission

class SubmissionService:
    def __init__(self, db: Session):
        self.db = db
    
    def soumettre_exercice(self, user_id: int, submission: ExerciceSubmission) -> Dict:
        """Soumettre les réponses d'un exercice et calculer la note"""
        
        # Vérifier que l'exercice existe
        exercice = self.db.query(Exercice).filter(Exercice.id == submission.exercice_id).first()
        if not exercice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercice not found"
            )
        
        # Récupérer toutes les questions de l'exercice avec leurs solutions
        questions = self.db.query(Question).filter(Question.exercice_id == submission.exercice_id).all()
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No questions found for this exercise"
            )
        
        # Créer un dictionnaire des réponses correctes depuis les questions
        solutions_correctes = {}
        for question in questions:
            if question.bonne_reponse:
                solutions_correctes[question.id] = question.bonne_reponse.strip().upper()
            elif question.reponse_attendue:
                solutions_correctes[question.id] = question.reponse_attendue.strip().lower()
        
        # Calculer la note
        total_questions = len(questions)
        bonnes_reponses = 0
        mauvaises_reponses = 0
        
        # Créer un dictionnaire des réponses utilisateur
        reponses_utilisateur = {r.question_id: r.reponse_utilisateur.strip().upper() 
                               for r in submission.reponses}
        
        # Vérifier chaque réponse
        for question_id in solutions_correctes:
            reponse_correcte = solutions_correctes[question_id]
            reponse_user = reponses_utilisateur.get(question_id, "").strip().upper()
            
            if reponse_user == reponse_correcte:
                bonnes_reponses += 1
            else:
                mauvaises_reponses += 1
        
        # Calculer la note finale
        note_obtenue = bonnes_reponses
        note_maximale = total_questions
        
        # Vérifier si l'utilisateur a déjà une note pour cet exercice
        note_existante = self.db.query(Note).filter(
            Note.utilisateur_id == user_id,
            Note.exercice_id == submission.exercice_id
        ).first()
        
        if note_existante:
            # Ajouter la nouvelle note à l'historique
            note_existante.ajouter_note(note_obtenue)
            note_existante.note_maximale = note_maximale
            note_existante.temps_passe = submission.temps_passe
            note_existante.nombre_tentatives += 1
            note_existante.completed_at = datetime.now(timezone.utc)
            note_obj = note_existante
        else:
            # Créer une nouvelle note
            note_obj = Note(
                utilisateur_id=user_id,
                exercice_id=submission.exercice_id,
                historique_notes=[note_obtenue],  # Première note dans l'historique
                note_maximale=note_maximale,
                temps_passe=submission.temps_passe,
                nombre_tentatives=1,
                completed_at=datetime.now(timezone.utc)
            )
            self.db.add(note_obj)
        
        self.db.commit()
        self.db.refresh(note_obj)
        
        return {
            "id": note_obj.id,
            "exercice_id": note_obj.exercice_id,
            "historique_notes": note_obj.historique_notes or [],
            "note_actuelle": note_obj.note_actuelle,
            "note_obtenue": note_obj.note_actuelle,  # Alias pour le frontend
            "meilleure_note": note_obj.meilleure_note,
            "note_maximale": note_obj.note_maximale,
            "pourcentage_actuel": round(note_obj.pourcentage_actuel, 2),
            "pourcentage_obtenu": round(note_obj.pourcentage_actuel, 2),  # Alias pour le frontend
            "temps_passe": note_obj.temps_passe,
            "nombre_tentatives": note_obj.nombre_tentatives,
            "completed_at": note_obj.completed_at,
            "total_questions": total_questions,
            "nombre_questions": total_questions,  # Alias pour le frontend
            "bonnes_reponses": bonnes_reponses,
            "nombre_bonnes_reponses": bonnes_reponses,  # Alias pour le frontend
            "mauvaises_reponses": mauvaises_reponses
        }
    
    def get_user_notes(self, user_id: int) -> List[Dict]:
        """Récupérer toutes les notes d'un utilisateur"""
        notes = self.db.query(Note).filter(Note.utilisateur_id == user_id).all()
        
        result = []
        for note in notes:
            result.append({
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
            })
        
        return result
