from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Exercice(Base):
    """Table des exercices pratiques"""
    __tablename__ = "exercices"
    
    id = Column(Integer, primary_key=True, index=True)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    type_exercice = Column(String(50), nullable=False)  # QCM, pratique, recherche_faille
    difficulte = Column(String(50))  # facile, moyen, difficile
    points_max = Column(Integer, default=100)
    temps_limite = Column(Integer)  # en minutes
    ordre = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    
    # Relations
    cours = relationship("Cours", back_populates="exercices")
    questions = relationship("Question", back_populates="exercice", cascade="all, delete-orphan")
    solutions = relationship("Solution", back_populates="exercice", cascade="all, delete-orphan")
    images = relationship("Image", back_populates="exercice", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="exercice", cascade="all, delete-orphan")
    paragraphes = relationship("Paragraphe", back_populates="exercice", cascade="all, delete-orphan")
