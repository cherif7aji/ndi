#!/usr/bin/env python3
"""
Script de migration SQLite pour simplifier la table utilisateurs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
from database import settings

def migrate_sqlite_users():
    """Migrer la table utilisateurs SQLite"""
    
    # Extraire le chemin de la base SQLite
    db_path = settings.database_url.replace('sqlite:///', '')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Début de la migration SQLite...")
        
        # Vérifier la structure actuelle
        cursor.execute("PRAGMA table_info(utilisateurs)")
        columns = cursor.fetchall()
        
        print("📋 Structure actuelle:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Créer une nouvelle table avec la structure simplifiée
        print("\n🔧 Création de la nouvelle table...")
        cursor.execute("""
            CREATE TABLE utilisateurs_new (
                id INTEGER PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user' NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                joker_1 BOOLEAN DEFAULT 1 NOT NULL,
                joker_2 BOOLEAN DEFAULT 1 NOT NULL,
                joker_3 BOOLEAN DEFAULT 1 NOT NULL
            )
        """)
        
        # Copier les données existantes (seulement les colonnes communes)
        print("📋 Copie des données existantes...")
        cursor.execute("""
            INSERT INTO utilisateurs_new 
            (id, username, password_hash, role, created_at, is_active, joker_1, joker_2, joker_3)
            SELECT id, username, password_hash, role, created_at, is_active, joker_1, joker_2, joker_3
            FROM utilisateurs
        """)
        
        # Supprimer l'ancienne table et renommer la nouvelle
        print("🔄 Remplacement de la table...")
        cursor.execute("DROP TABLE utilisateurs")
        cursor.execute("ALTER TABLE utilisateurs_new RENAME TO utilisateurs")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier la nouvelle structure
        cursor.execute("PRAGMA table_info(utilisateurs)")
        new_columns = cursor.fetchall()
        
        print("\n✅ Migration terminée!")
        print("📊 Nouvelle structure:")
        for col in new_columns:
            print(f"  - {col[1]} ({col[2]})")
            
        # Vérifier les données
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        count = cursor.fetchone()[0]
        print(f"\n👥 {count} utilisateurs migrés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    print("🛡️  Migration SQLite - CyberSec Academy")
    print("=" * 50)
    
    response = input("⚠️  Cette opération va modifier la structure de la table utilisateurs. Continuer? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'oui']:
        migrate_sqlite_users()
    else:
        print("❌ Migration annulée.")
        sys.exit(0)
