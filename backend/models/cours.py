from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Cours(Base):
    """Table des cours de sécurité"""
    __tablename__ = "cours"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    niveau = Column(String(50))  # débutant, intermédiaire, avancé
    duree_estimee = Column(Integer)  # en minutes
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    
    # Relations
    paragraphes = relationship("Paragraphe", back_populates="cours")
    videos = relationship("Video", back_populates="cours")
    images = relationship("Image", back_populates="cours")
    exercices = relationship("Exercice", back_populates="cours")
