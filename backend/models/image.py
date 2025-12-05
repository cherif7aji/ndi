from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Image(Base):
    """Table unifiée des images pour cours et exercices avec stockage Base64"""
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Références optionnelles (une seule sera remplie)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=True)
    exercice_id = Column(Integer, ForeignKey("exercices.id"), nullable=True)
    
    # Informations de l'image
    titre = Column(String(200))
    nom_fichier = Column(String(255), nullable=False)
    extension = Column(String(10), nullable=False)  # .jpg, .png, etc.
    alt_text = Column(String(255))
    description = Column(Text)
    type_image = Column(String(50))  # illustration, screenshot, diagram, solution, hint
    
    # Stockage Base64 du fichier
    contenu_base64 = Column(Text, nullable=False)  # Fichier encodé en Base64
    
    # Métadonnées du fichier
    taille_fichier = Column(Integer)  # en bytes (taille originale)
    largeur = Column(Integer)  # pixels
    hauteur = Column(Integer)  # pixels
    
    ordre = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relations
    cours = relationship("Cours", back_populates="images")
    exercice = relationship("Exercice", back_populates="images")
    
    # Index pour performance
    __table_args__ = (
        Index('idx_cours_id', 'cours_id'),
        Index('idx_exercice_id', 'exercice_id'),
    )
