from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Video(Base):
    """Table unifiée des vidéos pour cours et exercices"""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Références optionnelles (une seule sera remplie)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=True)
    exercice_id = Column(Integer, ForeignKey("exercices.id"), nullable=True)
    
    # Informations de la vidéo
    titre = Column(String(200), nullable=False)
    url_video = Column(String(500), nullable=False)
    description = Column(Text)
    type_video = Column(String(50))  # tutorial, demonstration, solution, explanation
    duree = Column(Integer)  # en secondes
    thumbnail_url = Column(String(500))  # URL de la miniature
    plateforme = Column(String(50))  # youtube, vimeo, local, etc.
    video_id = Column(String(100))  # ID de la vidéo sur la plateforme
    ordre = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relations
    cours = relationship("Cours", back_populates="videos")
    exercice = relationship("Exercice", back_populates="videos")
    
    # Index pour performance
    __table_args__ = (
        Index('idx_cours_id_video', 'cours_id'),
        Index('idx_exercice_id_video', 'exercice_id'),
    )
