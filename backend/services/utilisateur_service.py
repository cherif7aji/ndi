from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Utilisateur
from schemas import UtilisateurCreate, UtilisateurResponse

class UtilisateurService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_utilisateur(self, utilisateur_data: UtilisateurCreate) -> Utilisateur:
        """Créer un nouvel utilisateur"""
        db_utilisateur = Utilisateur(**utilisateur_data.dict())
        self.db.add(db_utilisateur)
        self.db.commit()
        self.db.refresh(db_utilisateur)
        return db_utilisateur
    
    def get_utilisateur_by_id(self, utilisateur_id: int) -> Utilisateur:
        """Récupérer un utilisateur par ID"""
        utilisateur = self.db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur not found"
            )
        return utilisateur
    
    def get_all_utilisateurs(self) -> List[Utilisateur]:
        """Récupérer tous les utilisateurs"""
        return self.db.query(Utilisateur).all()
    
    def update_utilisateur(self, utilisateur_id: int, utilisateur_data: dict) -> Utilisateur:
        """Mettre à jour un utilisateur"""
        utilisateur = self.get_utilisateur_by_id(utilisateur_id)
        
        for field, value in utilisateur_data.items():
            if hasattr(utilisateur, field) and value is not None:
                setattr(utilisateur, field, value)
        
        self.db.commit()
        self.db.refresh(utilisateur)
        return utilisateur
    
    def delete_utilisateur(self, utilisateur_id: int) -> bool:
        """Supprimer un utilisateur"""
        utilisateur = self.get_utilisateur_by_id(utilisateur_id)
        self.db.delete(utilisateur)
        self.db.commit()
        return True
