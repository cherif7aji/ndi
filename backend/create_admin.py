#!/usr/bin/env python3
"""
Script pour créer un utilisateur admin directement en base de données
Usage: python create_admin.py
"""

from database import SessionLocal, engine
from models import Utilisateur
from services.auth_service import AuthService
import sys

def create_admin_user():
    """Créer un utilisateur admin directement en base"""
    db = SessionLocal()
    
    try:
        # Demander les informations
        print("🔐 Création d'un utilisateur administrateur")
        print("=" * 40)
        
        username = input("Username: ").strip()
        if not username:
            print("❌ Username requis")
            return
            
        nom = input("Nom: ").strip()
        if not nom:
            return
            
        prenom = input("Prénom: ").strip()
        if not prenom:
            print("❌ Prénom requis")
            return
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création d'un administrateur")
    print("=" * 50)
    create_admin_user()
    
    try:
        admins = db.query(Utilisateur).filter(Utilisateur.role == "admin").all()
        
        if not admins:
            print("ℹ️  Aucun administrateur trouvé")
            return
            
        print("👥 Administrateurs existants:")
        print("-" * 40)
        for admin in admins:
            print(f"   - {admin.username} ({admin.email}) - ID: {admin.id}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_admins()
    else:
        create_admin_user()
