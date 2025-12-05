from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Solution(Base):
    """Table des solutions détaillées pour les exercices"""
    __tablename__ = "solutions"
    
    id = Column(Integer, primary_key=True, index=True)
    exercice_id = Column(Integer, ForeignKey("exercices.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    explication = Column(Text, nullable=False)
    code_solution = Column(Text)  # pour les exercices de code
    ressources_supplementaires = Column(Text)  # liens, références
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relations
    exercice = relationship("Exercice", back_populates="solutions")
