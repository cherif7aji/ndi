#!/usr/bin/env python3
"""
Script de migration pour simplifier la table utilisateurs
Supprime les colonnes nom, prenom, email pour ne garder que username et password
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from database import settings

def migrate_user_table():
    """Migrer la table utilisateurs pour supprimer nom, prenom, email"""
    
    # Créer la connexion à la base de données
    engine = create_engine(settings.database_url)
    
    try:
        with engine.connect() as connection:
            # Commencer une transaction
            trans = connection.begin()
            
            try:
                print("🔄 Début de la migration de la table utilisateurs...")
                
                # Vérifier si les colonnes existent avant de les supprimer
                result = connection.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'utilisateurs' 
                    AND column_name IN ('nom', 'prenom', 'email')
                """))
                
                existing_columns = [row[0] for row in result]
                print(f"📋 Colonnes à supprimer trouvées: {existing_columns}")
                
                # Supprimer les colonnes si elles existent
                for column in ['nom', 'prenom', 'email']:
                    if column in existing_columns:
                        print(f"🗑️  Suppression de la colonne '{column}'...")
                        connection.execute(text(f"ALTER TABLE utilisateurs DROP COLUMN IF EXISTS {column}"))
                
                # Valider la transaction
                trans.commit()
                print("✅ Migration terminée avec succès!")
                
                # Vérifier la structure finale
                result = connection.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'utilisateurs'
                    ORDER BY ordinal_position
                """))
                
                print("\n📊 Structure finale de la table utilisateurs:")
                print("Colonne | Type | Nullable")
                print("-" * 40)
                for row in result:
                    print(f"{row[0]} | {row[1]} | {row[2]}")
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Erreur lors de la migration: {e}")
                raise
                
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🛡️  Migration CyberSec Academy - Simplification table utilisateurs")
    print("=" * 60)
    
    # Demander confirmation
    response = input("⚠️  Cette opération va supprimer les colonnes nom, prenom, email. Continuer? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'oui']:
        migrate_user_table()
    else:
        print("❌ Migration annulée.")
        sys.exit(0)
