from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Paragraphe(Base):
    """Table unifiée des paragraphes pour cours et exercices"""
    __tablename__ = "paragraphes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Références optionnelles (une seule sera remplie)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=True)
    exercice_id = Column(Integer, ForeignKey("exercices.id"), nullable=True)
    
    # Contenu du paragraphe
    titre = Column(String(200), nullable=False)
    contenu = Column(Text, nullable=False)
    type_paragraphe = Column(String(50))  # introduction, explication, exemple, conclusion, instruction
    est_visible = Column(Boolean, default=True)  # pour masquer/afficher conditionnellement
    ordre = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relations
    cours = relationship("Cours", back_populates="paragraphes")
    exercice = relationship("Exercice", back_populates="paragraphes")
    
    # Index pour performance
    __table_args__ = (
        Index('idx_cours_id_paragraphe', 'cours_id'),
        Index('idx_exercice_id_paragraphe', 'exercice_id'),
    )
