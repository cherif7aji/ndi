from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Question
from schemas import QuestionCreate, QuestionResponse, QuestionUpdate

class QuestionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_question(self, question_data: QuestionCreate) -> Question:
        """Créer une nouvelle question"""
        db_question = Question(**question_data.dict())
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question
    
    def get_question_by_id(self, question_id: int) -> Question:
        """Récupérer une question par ID"""
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        return question
    
    def get_all_questions(self) -> List[Question]:
        """Récupérer toutes les questions"""
        return self.db.query(Question).all()
    
    def update_question(self, question_id: int, question_data: QuestionUpdate) -> Question:
        """Mettre à jour une question"""
        question = self.get_question_by_id(question_id)
        
        update_data = question_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(question, field):
                setattr(question, field, value)
        
        self.db.commit()
        self.db.refresh(question)
        return question
    
    def delete_question(self, question_id: int) -> bool:
        """Supprimer une question"""
        question = self.get_question_by_id(question_id)
        self.db.delete(question)
        self.db.commit()
        return True
    
    def validate_answer(self, question_id: int, user_answer: str) -> dict:
        """Valider la réponse d'un utilisateur"""
        question = self.get_question_by_id(question_id)
        
        is_correct = False
        feedback = ""
        
        if question.type_question == "multiple_choice":
            is_correct = user_answer.upper() == question.bonne_reponse
            if is_correct:
                feedback = "Bonne réponse !"
            else:
                feedback = f"Mauvaise réponse. La bonne réponse était {question.bonne_reponse}"
        
        elif question.type_question in ["text", "code"]:
            # Pour les questions ouvertes, comparaison simple
            # En production, on pourrait utiliser des algorithmes plus sophistiqués
            if question.reponse_attendue:
                is_correct = user_answer.lower().strip() == question.reponse_attendue.lower().strip()
                if is_correct:
                    feedback = "Bonne réponse !"
                else:
                    feedback = "Réponse incorrecte. Vérifiez votre réponse."
            else:
                # Pas de réponse attendue définie, nécessite une correction manuelle
                feedback = "Réponse enregistrée. Correction manuelle requise."
        
        return {
            "question_id": question_id,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "points_earned": question.points if is_correct else 0,
            "max_points": question.points,
            "feedback": feedback
        }
    
    def get_question_stats(self, question_id: int) -> dict:
        """Obtenir les statistiques d'une question"""
        question = self.get_question_by_id(question_id)
        
        # Ici on pourrait calculer des stats basées sur les réponses des utilisateurs
        # Pour l'instant, retournons des infos de base
        return {
            "question_id": question_id,
            "type": question.type_question,
            "points": question.points,
            "exercice_id": question.exercice_id,
            "ordre": question.ordre
        }
