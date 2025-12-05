from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Note(Base):
    """Table des notes des utilisateurs"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    exercice_id = Column(Integer, ForeignKey("exercices.id"), nullable=False)
    historique_notes = Column(JSON, default=list)  # Liste des notes [note_récente, note_précédente, ...]
    note_maximale = Column(Float, nullable=False)
    temps_passe = Column(Integer)  # en secondes du dernier essai
    nombre_tentatives = Column(Integer, default=1)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relations
    utilisateur = relationship("Utilisateur", back_populates="notes")
    exercice = relationship("Exercice")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.historique_notes is None:
            self.historique_notes = []
    
    def ajouter_note(self, nouvelle_note: float):
        """Ajouter une nouvelle note au début de l'historique"""
        if self.historique_notes is None:
            self.historique_notes = []
        
        # Créer une nouvelle liste avec la nouvelle note au début
        nouvelles_notes = [nouvelle_note] + self.historique_notes
        
        # Limiter l'historique à 10 tentatives maximum (optionnel)
        if len(nouvelles_notes) > 10:
            nouvelles_notes = nouvelles_notes[:10]
        
        # Assigner la nouvelle liste
        self.historique_notes = nouvelles_notes
    
    @property
    def note_actuelle(self) -> float:
        """Récupérer la note la plus récente"""
        if self.historique_notes and len(self.historique_notes) > 0:
            return self.historique_notes[0]
        return 0.0
    
    @property
    def pourcentage_actuel(self) -> float:
        """Calculer le pourcentage de la note actuelle"""
        if self.note_maximale > 0:
            return (self.note_actuelle / self.note_maximale) * 100
        return 0.0
    
    @property
    def meilleure_note(self) -> float:
        """Récupérer la meilleure note de l'historique"""
        if self.historique_notes and len(self.historique_notes) > 0:
            return max(self.historique_notes)
        return 0.0
