from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Question(Base):
    """Table des questions pour les exercices"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    exercice_id = Column(Integer, ForeignKey("exercices.id"), nullable=False)
    texte_question = Column(Text, nullable=False)
    type_question = Column(String(50), nullable=False)  # multiple_choice, text, code
    points = Column(Integer, default=10)
    ordre = Column(Integer, nullable=False)
    
    # Pour les QCM
    option_a = Column(Text)
    option_b = Column(Text)
    option_c = Column(Text)
    option_d = Column(Text)
    bonne_reponse = Column(String(10))  # A, B, C, D ou texte libre
    
    # Pour les questions ouvertes
    reponse_attendue = Column(Text)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relations
    exercice = relationship("Exercice", back_populates="questions")
