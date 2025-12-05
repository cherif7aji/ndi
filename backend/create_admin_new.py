#!/usr/bin/env python3
"""
Script pour créer un nouvel utilisateur administrateur
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Utilisateur
from services import AuthService

def create_new_admin():
    """Créer un nouvel utilisateur administrateur"""
    db: Session = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        print("🔐 Création d'un nouvel administrateur")
        print("=" * 40)
        
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
            print(f"❌ Username '{username}' déjà utilisé")
            return
        
        # Créer l'utilisateur admin
        hashed_password = auth_service.get_password_hash(password)
        admin_user = Utilisateur(
            username=username,
            password_hash=hashed_password,
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Administrateur créé avec succès!")
        print(f"👤 Username: {username}")
        print(f"🔑 Role: admin")
        print("⚠️  Gardez ces identifiants en sécurité!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'administrateur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création d'un administrateur")
    print("=" * 50)
    create_new_admin()
