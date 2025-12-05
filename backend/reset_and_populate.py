#!/usr/bin/env python3
"""
Script pour vider et repeupler la base de données avec des cours et exercices QCM
IMPORTANT: Ne touche PAS aux cours "MP - " (Mise en pratique)
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def login_admin():
    """Se connecter en tant qu'admin"""
    admin_accounts = [
        {"username": "hacker", "password": "password123"},
        {"username": "usert", "password": "usert"},
        {"username": "admin", "password": "admin123"}
    ]
    
    for login_data in admin_accounts:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if me_response.status_code == 200 and me_response.json().get("role") == "admin":
                print(f"✅ Connecté en tant qu'admin: {login_data['username']}")
                return token
    
    print("❌ Aucun compte admin trouvé")
    return None

def delete_existing_content(headers):
    """Supprimer tous les cours SAUF ceux commençant par 'MP - '"""
    print("\n🗑️  Suppression des cours existants (sauf Mise en pratique)...")
    
    # Récupérer tous les cours
    response = requests.get(f"{BASE_URL}/cours", headers=headers)
    if response.status_code == 200:
        cours_list = response.json()
        deleted_count = 0
        kept_count = 0
        
        for cours in cours_list:
            if cours['titre'].startswith('MP - '):
                print(f"   ⏭️  Conservé: {cours['titre']}")
                kept_count += 1
            else:
                # Supprimer le cours
                del_response = requests.delete(f"{BASE_URL}/cours/{cours['id']}/with-content", headers=headers)
                if del_response.status_code == 200:
                    print(f"   ❌ Supprimé: {cours['titre']}")
                    deleted_count += 1
        
        print(f"\n   📊 Résumé: {deleted_count} cours supprimés, {kept_count} cours conservés")

def create_courses(headers):
    """Créer des cours avec paragraphes et images"""
    
    courses = [
        {
            "titre": "Introduction à la Cybersécurité",
            "description": "Découvrez les fondamentaux de la sécurité informatique et les principales menaces",
            "niveau": "Débutant",
            "duree_estimee": 30,
            "paragraphes": [
                {
                    "titre": "Qu'est-ce que la cybersécurité ?",
                    "contenu": "La cybersécurité est l'ensemble des moyens techniques, organisationnels, juridiques et humains nécessaires pour protéger les systèmes informatiques, les réseaux et les données contre les accès non autorisés, les attaques et les dommages. Elle vise à garantir la confidentialité, l'intégrité et la disponibilité des informations.",
                    "type_paragraphe": "contenu",
                    "ordre": 1
                },
                {
                    "titre": "Les trois piliers de la sécurité",
                    "contenu": "La sécurité informatique repose sur trois principes fondamentaux appelés la triade CIA :\n\n1. Confidentialité : Garantir que seules les personnes autorisées peuvent accéder aux informations\n2. Intégrité : Assurer que les données ne sont pas modifiées de manière non autorisée\n3. Disponibilité : S'assurer que les systèmes et données sont accessibles quand nécessaire",
                    "type_paragraphe": "contenu",
                    "ordre": 2
                },
                {
                    "titre": "Les principales menaces",
                    "contenu": "Les cyberattaques les plus courantes incluent :\n\n- Malwares (virus, trojans, ransomwares)\n- Phishing et ingénierie sociale\n- Attaques par déni de service (DDoS)\n- Injections SQL et XSS\n- Attaques de type Man-in-the-Middle\n- Exploitation de vulnérabilités zero-day",
                    "type_paragraphe": "contenu",
                    "ordre": 3
                },
                {
                    "titre": "⚠️ Importance de la sécurité",
                    "contenu": "Les cyberattaques peuvent avoir des conséquences graves : vol de données personnelles, pertes financières, atteinte à la réputation, interruption de services critiques. Il est essentiel de comprendre les risques et d'appliquer les bonnes pratiques de sécurité.",
                    "type_paragraphe": "avertissement",
                    "ordre": 4
                }
            ]
        },
        {
            "titre": "Authentification et Gestion des Sessions",
            "description": "Apprenez les mécanismes d'authentification sécurisée et la gestion des sessions utilisateur",
            "niveau": "Intermédiaire",
            "duree_estimee": 45,
            "paragraphes": [
                {
                    "titre": "Méthodes d'authentification",
                    "contenu": "L'authentification permet de vérifier l'identité d'un utilisateur. Les principales méthodes incluent :\n\n1. Authentification par mot de passe : La plus courante mais aussi la plus vulnérable\n2. Authentification multi-facteurs (MFA) : Combine plusieurs facteurs (mot de passe + code SMS + biométrie)\n3. Authentification par certificat : Utilise des certificats numériques\n4. Authentification biométrique : Empreintes digitales, reconnaissance faciale",
                    "type_paragraphe": "contenu",
                    "ordre": 1
                },
                {
                    "titre": "Tokens JWT",
                    "contenu": "JSON Web Token (JWT) est un standard ouvert (RFC 7519) qui définit une manière compacte et autonome de transmettre des informations entre parties sous forme d'objet JSON. Les JWTs sont composés de trois parties : Header, Payload et Signature. Ils sont largement utilisés pour l'authentification dans les API REST.",
                    "type_paragraphe": "contenu",
                    "ordre": 2
                },
                {
                    "titre": "Gestion sécurisée des mots de passe",
                    "contenu": "Les bonnes pratiques pour les mots de passe :\n\n- Utiliser un algorithme de hachage fort (bcrypt, Argon2)\n- Ajouter un salt unique pour chaque mot de passe\n- Implémenter une politique de complexité\n- Limiter les tentatives de connexion\n- Ne JAMAIS stocker les mots de passe en clair\n- Utiliser HTTPS pour la transmission",
                    "type_paragraphe": "contenu",
                    "ordre": 3
                },
                {
                    "titre": "ℹ️ Sessions et cookies",
                    "contenu": "Les sessions permettent de maintenir l'état d'authentification. Les cookies de session doivent être configurés avec les flags HttpOnly, Secure et SameSite pour prévenir les attaques XSS et CSRF. La durée de vie des sessions doit être limitée et les tokens doivent être régénérés.",
                    "type_paragraphe": "info",
                    "ordre": 4
                }
            ]
        },
        {
            "titre": "Sécurité des Applications Web",
            "description": "Découvrez les vulnérabilités web courantes et comment les prévenir",
            "niveau": "Intermédiaire",
            "duree_estimee": 60,
            "paragraphes": [
                {
                    "titre": "OWASP Top 10",
                    "contenu": "L'OWASP (Open Web Application Security Project) publie régulièrement une liste des 10 vulnérabilités web les plus critiques :\n\n1. Broken Access Control\n2. Cryptographic Failures\n3. Injection\n4. Insecure Design\n5. Security Misconfiguration\n6. Vulnerable Components\n7. Authentication Failures\n8. Software and Data Integrity Failures\n9. Logging and Monitoring Failures\n10. Server-Side Request Forgery (SSRF)",
                    "type_paragraphe": "contenu",
                    "ordre": 1
                },
                {
                    "titre": "Injection SQL",
                    "contenu": "L'injection SQL est une technique d'attaque qui exploite une faille de sécurité dans une application interagissant avec une base de données. L'attaquant insère du code SQL malveillant dans les entrées utilisateur pour manipuler les requêtes. Prévention : utiliser des requêtes préparées et valider toutes les entrées.",
                    "type_paragraphe": "contenu",
                    "ordre": 2
                },
                {
                    "titre": "Cross-Site Scripting (XSS)",
                    "contenu": "Le XSS permet d'injecter du code JavaScript malveillant dans une page web. Il existe trois types : Reflected XSS, Stored XSS et DOM-based XSS. Pour se protéger : encoder toutes les sorties, utiliser Content Security Policy (CSP), et valider les entrées utilisateur.",
                    "type_paragraphe": "contenu",
                    "ordre": 3
                },
                {
                    "titre": "⚠️ Validation des entrées",
                    "contenu": "Ne jamais faire confiance aux données utilisateur ! Toutes les entrées doivent être validées côté serveur, même si une validation côté client existe. Utilisez des whitelists plutôt que des blacklists, et appliquez le principe du moindre privilège.",
                    "type_paragraphe": "avertissement",
                    "ordre": 4
                }
            ]
        }
    ]
    
    print("\n📚 Création des cours...")
    created_courses = []
    
    for course_data in courses:
        course_data["videos"] = []
        course_data["images_base64"] = []
        
        response = requests.post(
            f"{BASE_URL}/cours/with-content",
            json=course_data,
            headers=headers
        )
        
        if response.status_code == 201:
            cours = response.json()
            created_courses.append(cours)
            print(f"   ✅ {cours['titre']} (ID: {cours['id']})")
        else:
            print(f"   ❌ Erreur: {course_data['titre']}")
    
    return created_courses

def create_exercises(courses, headers):
    """Créer des exercices QCM pour chaque cours"""
    
    exercises_data = [
        {
            "cours_index": 0,  # Introduction à la Cybersécurité
            "exercices": [
                {
                    "titre": "Quiz - Fondamentaux de la cybersécurité",
                    "description": "Testez vos connaissances sur les bases de la cybersécurité",
                    "type_exercice": "QCM",
                    "difficulte": "facile",
                    "points_max": 100,
                    "temps_limite": 10,
                    "questions": [
                        {
                            "texte_question": "Que signifie l'acronyme CIA en cybersécurité ?",
                            "type_question": "multiple_choice",
                            "points": 25,
                            "ordre": 1,
                            "option_a": "Confidentialité, Intégrité, Disponibilité",
                            "option_b": "Central Intelligence Agency",
                            "option_c": "Cryptographie, Identification, Authentification",
                            "option_d": "Contrôle, Inspection, Analyse",
                            "bonne_reponse": "A"
                        },
                        {
                            "texte": "Quel est le principal objectif de la confidentialité ?",
                            "type_question": "choix_unique",
                            "points": 25,
                            "ordre": 2,
                            "solutions": [
                                {"texte": "Garantir que seules les personnes autorisées accèdent aux données", "est_correcte": True, "ordre": 1},
                                {"texte": "Assurer que les données sont toujours disponibles", "est_correcte": False, "ordre": 2},
                                {"texte": "Vérifier que les données ne sont pas modifiées", "est_correcte": False, "ordre": 3},
                                {"texte": "Crypter toutes les communications", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Quelles sont les principales menaces en cybersécurité ? (Plusieurs réponses)",
                            "type_question": "choix_multiple",
                            "points": 25,
                            "ordre": 3,
                            "solutions": [
                                {"texte": "Malwares", "est_correcte": True, "ordre": 1},
                                {"texte": "Phishing", "est_correcte": True, "ordre": 2},
                                {"texte": "Mises à jour système", "est_correcte": False, "ordre": 3},
                                {"texte": "Attaques DDoS", "est_correcte": True, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Qu'est-ce qu'un ransomware ?",
                            "type_question": "choix_unique",
                            "points": 25,
                            "ordre": 4,
                            "solutions": [
                                {"texte": "Un malware qui chiffre les données et demande une rançon", "est_correcte": True, "ordre": 1},
                                {"texte": "Un logiciel de protection antivirus", "est_correcte": False, "ordre": 2},
                                {"texte": "Une technique de phishing", "est_correcte": False, "ordre": 3},
                                {"texte": "Un type de firewall", "est_correcte": False, "ordre": 4}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "cours_index": 1,  # Authentification et Gestion des Sessions
            "exercices": [
                {
                    "titre": "Quiz - Authentification sécurisée",
                    "description": "Évaluez vos connaissances sur l'authentification et les tokens",
                    "type_exercice": "QCM",
                    "difficulte": "moyen",
                    "points_max": 100,
                    "temps_limite": 15,
                    "questions": [
                        {
                            "texte": "Qu'est-ce que l'authentification multi-facteurs (MFA) ?",
                            "type_question": "choix_unique",
                            "points": 20,
                            "ordre": 1,
                            "solutions": [
                                {"texte": "Une méthode combinant plusieurs facteurs d'authentification", "est_correcte": True, "ordre": 1},
                                {"texte": "Un mot de passe très complexe", "est_correcte": False, "ordre": 2},
                                {"texte": "Un système de double mot de passe", "est_correcte": False, "ordre": 3},
                                {"texte": "Une authentification par email uniquement", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "De quoi est composé un JWT (JSON Web Token) ?",
                            "type_question": "choix_multiple",
                            "points": 20,
                            "ordre": 2,
                            "solutions": [
                                {"texte": "Header", "est_correcte": True, "ordre": 1},
                                {"texte": "Payload", "est_correcte": True, "ordre": 2},
                                {"texte": "Signature", "est_correcte": True, "ordre": 3},
                                {"texte": "Timestamp", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Quel algorithme est recommandé pour hasher les mots de passe ?",
                            "type_question": "choix_unique",
                            "points": 20,
                            "ordre": 3,
                            "solutions": [
                                {"texte": "bcrypt ou Argon2", "est_correcte": True, "ordre": 1},
                                {"texte": "MD5", "est_correcte": False, "ordre": 2},
                                {"texte": "SHA-1", "est_correcte": False, "ordre": 3},
                                {"texte": "Base64", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Pourquoi ne faut-il JAMAIS stocker les mots de passe en clair ?",
                            "type_question": "choix_unique",
                            "points": 20,
                            "ordre": 4,
                            "solutions": [
                                {"texte": "En cas de fuite, tous les comptes seraient compromis", "est_correcte": True, "ordre": 1},
                                {"texte": "C'est illégal dans tous les pays", "est_correcte": False, "ordre": 2},
                                {"texte": "Cela prend trop d'espace de stockage", "est_correcte": False, "ordre": 3},
                                {"texte": "Les bases de données ne le permettent pas", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Quels flags de sécurité doivent être configurés sur les cookies de session ?",
                            "type_question": "choix_multiple",
                            "points": 20,
                            "ordre": 5,
                            "solutions": [
                                {"texte": "HttpOnly", "est_correcte": True, "ordre": 1},
                                {"texte": "Secure", "est_correcte": True, "ordre": 2},
                                {"texte": "SameSite", "est_correcte": True, "ordre": 3},
                                {"texte": "Public", "est_correcte": False, "ordre": 4}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "cours_index": 2,  # Sécurité des Applications Web
            "exercices": [
                {
                    "titre": "Quiz - Vulnérabilités Web OWASP",
                    "description": "Testez vos connaissances sur les vulnérabilités web courantes",
                    "type_exercice": "QCM",
                    "difficulte": "moyen",
                    "points_max": 100,
                    "temps_limite": 15,
                    "questions": [
                        {
                            "texte": "Qu'est-ce qu'une injection SQL ?",
                            "type_question": "choix_unique",
                            "points": 20,
                            "ordre": 1,
                            "solutions": [
                                {"texte": "Une attaque qui insère du code SQL malveillant dans les entrées", "est_correcte": True, "ordre": 1},
                                {"texte": "Une méthode de sauvegarde de base de données", "est_correcte": False, "ordre": 2},
                                {"texte": "Un type de requête optimisée", "est_correcte": False, "ordre": 3},
                                {"texte": "Une technique de chiffrement", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Comment se protéger contre les injections SQL ?",
                            "type_question": "choix_multiple",
                            "points": 20,
                            "ordre": 2,
                            "solutions": [
                                {"texte": "Utiliser des requêtes préparées", "est_correcte": True, "ordre": 1},
                                {"texte": "Valider toutes les entrées utilisateur", "est_correcte": True, "ordre": 2},
                                {"texte": "Utiliser un ORM", "est_correcte": True, "ordre": 3},
                                {"texte": "Désactiver la base de données", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Que signifie XSS ?",
                            "type_question": "choix_unique",
                            "points": 20,
                            "ordre": 3,
                            "solutions": [
                                {"texte": "Cross-Site Scripting", "est_correcte": True, "ordre": 1},
                                {"texte": "Extra Security System", "est_correcte": False, "ordre": 2},
                                {"texte": "XML Security Standard", "est_correcte": False, "ordre": 3},
                                {"texte": "eXtended SQL Syntax", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Quels sont les types de XSS ?",
                            "type_question": "choix_multiple",
                            "points": 20,
                            "ordre": 4,
                            "solutions": [
                                {"texte": "Reflected XSS", "est_correcte": True, "ordre": 1},
                                {"texte": "Stored XSS", "est_correcte": True, "ordre": 2},
                                {"texte": "DOM-based XSS", "est_correcte": True, "ordre": 3},
                                {"texte": "Server XSS", "est_correcte": False, "ordre": 4}
                            ]
                        },
                        {
                            "texte": "Quelle est la meilleure pratique pour valider les entrées utilisateur ?",
                            "type_question": "choix_unique",
                            "points": 20,
                            "ordre": 5,
                            "solutions": [
                                {"texte": "Utiliser une whitelist et valider côté serveur", "est_correcte": True, "ordre": 1},
                                {"texte": "Valider uniquement côté client", "est_correcte": False, "ordre": 2},
                                {"texte": "Faire confiance aux données utilisateur", "est_correcte": False, "ordre": 3},
                                {"texte": "Utiliser uniquement une blacklist", "est_correcte": False, "ordre": 4}
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    
    print("\n📝 Création des exercices QCM...")
    created_exercises = []
    
    for ex_data in exercises_data:
        cours_id = courses[ex_data["cours_index"]]["id"]
        
        for exercice in ex_data["exercices"]:
            exercice["cours_id"] = cours_id
            exercice["ordre"] = 1
            
            response = requests.post(
                f"{BASE_URL}/exercices/with-content",
                json=exercice,
                headers=headers
            )
            
            if response.status_code == 201:
                ex = response.json()
                created_exercises.append(ex)
                print(f"   ✅ {ex['titre']} (Cours: {courses[ex_data['cours_index']]['titre']})")
            else:
                print(f"   ❌ Erreur: {exercice['titre']}")
                print(f"      {response.text}")
    
    return created_exercises

def main():
    print("="*70)
    print("  🔄 Réinitialisation et population de la base de données")
    print("="*70)
    
    token = login_admin()
    if not token:
        print("❌ Impossible de continuer sans compte admin")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Étape 1: Supprimer l'ancien contenu (sauf MP)
    delete_existing_content(headers)
    
    # Étape 2: Créer les cours
    courses = create_courses(headers)
    
    # Étape 3: Créer les exercices
    exercises = create_exercises(courses, headers)
    
    print("\n" + "="*70)
    print("  ✅ Base de données réinitialisée avec succès!")
    print("="*70)
    print(f"\n📊 Résumé:")
    print(f"   - Cours créés: {len(courses)}")
    print(f"   - Exercices QCM créés: {len(exercises)}")
    print(f"   - Tutoriels Mise en pratique: Conservés intacts")
    print(f"\n🎯 Tous les exercices sont de type QCM avec questions à choix unique/multiple")

if __name__ == "__main__":
    main()
