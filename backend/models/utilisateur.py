from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class Utilisateur(Base):
    """Table des utilisateurs avec authentification JWT"""
    __tablename__ = "utilisateurs"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # "user", "admin"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    
    # Système de jokers
    joker_1 = Column(Boolean, default=True, nullable=False)
    joker_2 = Column(Boolean, default=True, nullable=False)
    joker_3 = Column(Boolean, default=True, nullable=False)
    
    # Relations
    notes = relationship("Note", back_populates="utilisateur")
