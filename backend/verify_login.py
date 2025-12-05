#!/usr/bin/env python3
"""
Script pour tester l'authentification d'un utilisateur
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from services import AuthService

def test_login():
    """Tester l'authentification"""
    db: Session = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        print("🔐 Test d'authentification")
        print("=" * 40)
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        print("\n🔍 Tentative d'authentification...")
        
        # Tester l'authentification
        user = auth_service.authenticate_user(username, password)
        
        if user:
            print("✅ Authentification réussie!")
            print(f"👤 Username: {user.username}")
            print(f"🔑 Role: {user.role}")
            print(f"✓ Active: {user.is_active}")
            
            # Créer un token
            token = auth_service.login_user(username, password)
            print(f"\n🎫 Token généré:")
            print(f"   {token.access_token[:50]}...")
        else:
            print("❌ Authentification échouée!")
            print("   Vérifiez le username et le password")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Test d'authentification")
    print("=" * 50)
    test_login()
