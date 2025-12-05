#!/usr/bin/env python3
"""
Script pour créer un utilisateur normal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Utilisateur
from services import AuthService

def create_user():
    """Créer un utilisateur normal"""
    db: Session = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        print("🔐 Création d'un utilisateur")
        print("=" * 30)
        
        username = input("Username: ").strip()
        if not username:
            print("❌ Username requis")
            return
            
        password = input("Password: ").strip()
        if not password:
            print("❌ Password requis")
            return
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(Utilisateur).filter(
            Utilisateur.username == username
        ).first()
        
        if existing_user:
            print("❌ Username déjà utilisé")
            return
        
        # Créer l'utilisateur
        hashed_password = auth_service.get_password_hash(password)
        user = Utilisateur(
            username=username,
            password_hash=hashed_password,
            role="user"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("✅ Utilisateur créé avec succès!")
        print(f"👤 Username: {username}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création d'un utilisateur")
    print("=" * 50)
    create_user()
