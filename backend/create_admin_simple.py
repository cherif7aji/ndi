#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur simplifié
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Utilisateur
from services import AuthService

def create_admin_user():
    """Créer un utilisateur administrateur"""
    db: Session = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        # Vérifier si un admin existe déjà
        existing_admin = db.query(Utilisateur).filter(Utilisateur.role == "admin").first()
        if existing_admin:
            print(f"❌ Un administrateur existe déjà: {existing_admin.username}")
            return
        
        # Données de l'administrateur (simplifiées)
        admin_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        # Créer l'utilisateur admin
        hashed_password = auth_service.get_password_hash(admin_data["password"])
        admin_user = Utilisateur(
            username=admin_data["username"],
            password_hash=hashed_password,
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Utilisateur administrateur créé avec succès!")
        print(f"👤 Username: {admin_data['username']}")
        print(f"🔑 Password: {admin_data['password']}")
        print("⚠️  Changez le mot de passe après la première connexion!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'administrateur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création d'un administrateur")
    print("=" * 50)
    create_admin_user()
