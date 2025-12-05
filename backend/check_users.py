#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs existants
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Utilisateur

def check_users():
    """Vérifier les utilisateurs existants"""
    db: Session = SessionLocal()
    
    try:
        users = db.query(Utilisateur).all()
        
        print(f"📊 Nombre d'utilisateurs: {len(users)}")
        print("-" * 50)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Role: {user.role}")
            print(f"Active: {user.is_active}")
            print(f"Created: {user.created_at}")
            
            # Vérifier si les anciens champs existent encore
            if hasattr(user, 'nom'):
                print(f"Nom: {user.nom}")
            if hasattr(user, 'prenom'):
                print(f"Prénom: {user.prenom}")
            if hasattr(user, 'email'):
                print(f"Email: {user.email}")
                
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Vérification des utilisateurs")
    print("=" * 60)
    check_users()
