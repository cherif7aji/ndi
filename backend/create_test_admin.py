#!/usr/bin/env python3
"""
Script pour créer un admin de test avec identifiants simples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Utilisateur
from services import AuthService

def create_test_admin():
    """Créer un admin de test"""
    db: Session = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        # Supprimer l'ancien admin de test s'il existe
        old_admin = db.query(Utilisateur).filter(Utilisateur.username == "admin").first()
        if old_admin:
            db.delete(old_admin)
            db.commit()
            print("🗑️  Ancien admin 'admin' supprimé")
        
        # Créer le nouvel admin de test
        username = "admin"
        password = "admin"
        
        hashed_password = auth_service.get_password_hash(password)
        admin_user = Utilisateur(
            username=username,
            password_hash=hashed_password,
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin de test créé avec succès!")
        print(f"👤 Username: {username}")
        print(f"🔑 Password: {password}")
        print(f"🎭 Role: admin")
        print("\n⚠️  ATTENTION: Ces identifiants sont pour TEST uniquement!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création admin de test")
    print("=" * 50)
    create_test_admin()
