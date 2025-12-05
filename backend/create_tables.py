#!/usr/bin/env python3
"""
Script pour créer les tables de la base de données avec la nouvelle structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from database import settings
from models import Base

def create_tables():
    """Créer toutes les tables de la base de données"""
    try:
        # Créer la connexion à la base de données
        engine = create_engine(settings.database_url)
        
        print("🔄 Création des tables de la base de données...")
        
        # Créer toutes les tables définies dans les modèles
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables créées avec succès!")
        
        # Afficher les tables créées
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("\n📊 Tables créées:")
        for table in tables:
            print(f"  - {table}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création des tables")
    print("=" * 50)
    create_tables()
