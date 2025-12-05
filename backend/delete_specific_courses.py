#!/usr/bin/env python3
"""
Supprimer des cours spécifiques directement de la base de données
"""

from sqlalchemy import create_engine, text
from database import settings

# Connexion à la base de données
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)

def delete_courses():
    """Supprimer les cours spécifiques"""
    
    courses_to_delete = [
        "Sécurité des Applications Web - Formation Complète",
        "hello2"
    ]
    
    with engine.connect() as conn:
        for titre in courses_to_delete:
            # Récupérer l'ID du cours
            result = conn.execute(
                text("SELECT id FROM cours WHERE titre = :titre"),
                {"titre": titre}
            )
            row = result.fetchone()
            
            if row:
                cours_id = row[0]
                print(f"🔍 Trouvé: '{titre}' (ID: {cours_id})")
                
                # Supprimer les images liées
                conn.execute(
                    text("DELETE FROM images WHERE cours_id = :cours_id"),
                    {"cours_id": cours_id}
                )
                print(f"   ❌ Images supprimées")
                
                # Supprimer les vidéos liées
                conn.execute(
                    text("DELETE FROM videos WHERE cours_id = :cours_id"),
                    {"cours_id": cours_id}
                )
                print(f"   ❌ Vidéos supprimées")
                
                # Supprimer les paragraphes liés
                conn.execute(
                    text("DELETE FROM paragraphes WHERE cours_id = :cours_id"),
                    {"cours_id": cours_id}
                )
                print(f"   ❌ Paragraphes supprimés")
                
                # Supprimer les questions des exercices liés
                conn.execute(
                    text("""
                        DELETE FROM questions 
                        WHERE exercice_id IN (
                            SELECT id FROM exercices WHERE cours_id = :cours_id
                        )
                    """),
                    {"cours_id": cours_id}
                )
                print(f"   ❌ Questions supprimées")
                
                # Supprimer les exercices liés
                conn.execute(
                    text("DELETE FROM exercices WHERE cours_id = :cours_id"),
                    {"cours_id": cours_id}
                )
                print(f"   ❌ Exercices supprimés")
                
                # Supprimer le cours
                conn.execute(
                    text("DELETE FROM cours WHERE id = :cours_id"),
                    {"cours_id": cours_id}
                )
                print(f"   ✅ Cours '{titre}' supprimé complètement\n")
                
                conn.commit()
            else:
                print(f"⚠️  Cours '{titre}' non trouvé\n")

if __name__ == "__main__":
    print("="*60)
    print("  🗑️  Suppression de cours spécifiques")
    print("="*60)
    print()
    
    delete_courses()
    
    print("="*60)
    print("  ✅ Opération terminée")
    print("="*60)
