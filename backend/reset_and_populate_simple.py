#!/usr/bin/env python3
"""
Script simplifié pour créer cours et exercices QCM
"""

import requests

BASE_URL = "http://localhost:8000"

def login_admin():
    """Se connecter en tant qu'admin"""
    admin_accounts = [
        {"username": "hacker", "password": "password123"},
        {"username": "usert", "password": "usert"}
    ]
    
    for login_data in admin_accounts:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if me_response.status_code == 200 and me_response.json().get("role") == "admin":
                print(f"✅ Connecté: {login_data['username']}")
                return token
    return None

def delete_non_mp_courses(headers):
    """Supprimer tous les cours sauf MP"""
    response = requests.get(f"{BASE_URL}/cours", headers=headers)
    if response.status_code == 200:
        for cours in response.json():
            if not cours['titre'].startswith('MP - '):
                requests.delete(f"{BASE_URL}/cours/{cours['id']}/with-content", headers=headers)
                print(f"❌ Supprimé: {cours['titre']}")
            else:
                print(f"⏭️  Conservé: {cours['titre']}")

def create_content(headers):
    """Créer cours et exercices"""
    
    # Cours 1
    cours1 = {
        "titre": "Introduction à la Cybersécurité",
        "description": "Découvrez les fondamentaux de la sécurité informatique",
        "niveau": "Débutant",
        "duree_estimee": 30,
        "paragraphes": [
            {
                "titre": "Qu'est-ce que la cybersécurité ?",
                "contenu": "La cybersécurité protège les systèmes informatiques contre les menaces. Elle garantit la confidentialité, l'intégrité et la disponibilité des données.",
                "type_paragraphe": "contenu",
                "ordre": 1
            },
            {
                "titre": "Les principales menaces",
                "contenu": "Les cyberattaques courantes : malwares, phishing, DDoS, injections SQL, XSS, et exploitation de vulnérabilités.",
                "type_paragraphe": "contenu",
                "ordre": 2
            }
        ],
        "videos": [],
        "images_base64": []
    }
    
    r1 = requests.post(f"{BASE_URL}/cours/with-content", json=cours1, headers=headers)
    if r1.status_code == 201:
        c1_id = r1.json()['id']
        print(f"✅ Cours 1 créé (ID: {c1_id})")
        
        # Exercice 1
        ex1 = {
            "cours_id": c1_id,
            "titre": "Quiz - Fondamentaux",
            "description": "Testez vos connaissances",
            "type_exercice": "QCM",
            "difficulte": "facile",
            "points_max": 100,
            "temps_limite": 10,
            "ordre": 1,
            "questions": [
                {
                    "texte_question": "Que signifie CIA en cybersécurité ?",
                    "type_question": "multiple_choice",
                    "points": 50,
                    "ordre": 1,
                    "option_a": "Confidentialité, Intégrité, Disponibilité",
                    "option_b": "Central Intelligence Agency",
                    "option_c": "Cryptographie, Identification, Authentification",
                    "option_d": "Contrôle, Inspection, Analyse",
                    "bonne_reponse": "A"
                },
                {
                    "texte_question": "Qu'est-ce qu'un ransomware ?",
                    "type_question": "multiple_choice",
                    "points": 50,
                    "ordre": 2,
                    "option_a": "Un malware qui chiffre les données et demande une rançon",
                    "option_b": "Un logiciel antivirus",
                    "option_c": "Une technique de phishing",
                    "option_d": "Un type de firewall",
                    "bonne_reponse": "A"
                }
            ]
        }
        
        r_ex1 = requests.post(f"{BASE_URL}/exercices/with-content", json=ex1, headers=headers)
        if r_ex1.status_code == 201:
            print(f"✅ Exercice 1 créé")
        else:
            print(f"❌ Erreur exercice 1: {r_ex1.text}")
    
    # Cours 2
    cours2 = {
        "titre": "Authentification Sécurisée",
        "description": "Apprenez les mécanismes d'authentification",
        "niveau": "Intermédiaire",
        "duree_estimee": 45,
        "paragraphes": [
            {
                "titre": "Méthodes d'authentification",
                "contenu": "Authentification par mot de passe, MFA, certificats, biométrie. Le MFA combine plusieurs facteurs pour plus de sécurité.",
                "type_paragraphe": "contenu",
                "ordre": 1
            },
            {
                "titre": "Tokens JWT",
                "contenu": "JSON Web Token est un standard pour transmettre des informations sécurisées. Composé de Header, Payload et Signature.",
                "type_paragraphe": "contenu",
                "ordre": 2
            }
        ],
        "videos": [],
        "images_base64": []
    }
    
    r2 = requests.post(f"{BASE_URL}/cours/with-content", json=cours2, headers=headers)
    if r2.status_code == 201:
        c2_id = r2.json()['id']
        print(f"✅ Cours 2 créé (ID: {c2_id})")
        
        # Exercice 2
        ex2 = {
            "cours_id": c2_id,
            "titre": "Quiz - Authentification",
            "description": "Évaluez vos connaissances",
            "type_exercice": "QCM",
            "difficulte": "moyen",
            "points_max": 100,
            "temps_limite": 15,
            "ordre": 1,
            "questions": [
                {
                    "texte_question": "Qu'est-ce que le MFA ?",
                    "type_question": "multiple_choice",
                    "points": 50,
                    "ordre": 1,
                    "option_a": "Une méthode combinant plusieurs facteurs d'authentification",
                    "option_b": "Un mot de passe très complexe",
                    "option_c": "Un système de double mot de passe",
                    "option_d": "Une authentification par email uniquement",
                    "bonne_reponse": "A"
                },
                {
                    "texte_question": "Quel algorithme pour hasher les mots de passe ?",
                    "type_question": "multiple_choice",
                    "points": 50,
                    "ordre": 2,
                    "option_a": "bcrypt ou Argon2",
                    "option_b": "MD5",
                    "option_c": "SHA-1",
                    "option_d": "Base64",
                    "bonne_reponse": "A"
                }
            ]
        }
        
        r_ex2 = requests.post(f"{BASE_URL}/exercices/with-content", json=ex2, headers=headers)
        if r_ex2.status_code == 201:
            print(f"✅ Exercice 2 créé")
        else:
            print(f"❌ Erreur exercice 2: {r_ex2.text}")
    
    # Cours 3
    cours3 = {
        "titre": "Vulnérabilités Web OWASP",
        "description": "Découvrez les failles web courantes",
        "niveau": "Intermédiaire",
        "duree_estimee": 60,
        "paragraphes": [
            {
                "titre": "OWASP Top 10",
                "contenu": "Les 10 vulnérabilités web les plus critiques : Broken Access Control, Injection, XSS, CSRF, etc.",
                "type_paragraphe": "contenu",
                "ordre": 1
            },
            {
                "titre": "Injection SQL",
                "contenu": "Attaque qui insère du code SQL malveillant. Prévention : requêtes préparées et validation des entrées.",
                "type_paragraphe": "contenu",
                "ordre": 2
            }
        ],
        "videos": [],
        "images_base64": []
    }
    
    r3 = requests.post(f"{BASE_URL}/cours/with-content", json=cours3, headers=headers)
    if r3.status_code == 201:
        c3_id = r3.json()['id']
        print(f"✅ Cours 3 créé (ID: {c3_id})")
        
        # Exercice 3
        ex3 = {
            "cours_id": c3_id,
            "titre": "Quiz - Vulnérabilités Web",
            "description": "Testez vos connaissances OWASP",
            "type_exercice": "QCM",
            "difficulte": "moyen",
            "points_max": 100,
            "temps_limite": 15,
            "ordre": 1,
            "questions": [
                {
                    "texte_question": "Qu'est-ce qu'une injection SQL ?",
                    "type_question": "multiple_choice",
                    "points": 50,
                    "ordre": 1,
                    "option_a": "Une attaque qui insère du code SQL malveillant",
                    "option_b": "Une méthode de sauvegarde de base de données",
                    "option_c": "Un type de requête optimisée",
                    "option_d": "Une technique de chiffrement",
                    "bonne_reponse": "A"
                },
                {
                    "texte_question": "Que signifie XSS ?",
                    "type_question": "multiple_choice",
                    "points": 50,
                    "ordre": 2,
                    "option_a": "Cross-Site Scripting",
                    "option_b": "Extra Security System",
                    "option_c": "XML Security Standard",
                    "option_d": "eXtended SQL Syntax",
                    "bonne_reponse": "A"
                }
            ]
        }
        
        r_ex3 = requests.post(f"{BASE_URL}/exercices/with-content", json=ex3, headers=headers)
        if r_ex3.status_code == 201:
            print(f"✅ Exercice 3 créé")
        else:
            print(f"❌ Erreur exercice 3: {r_ex3.text}")

def main():
    print("="*60)
    print("  🔄 Réinitialisation de la base de données")
    print("="*60)
    
    token = login_admin()
    if not token:
        print("❌ Impossible de continuer")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🗑️  Suppression des cours (sauf MP)...")
    delete_non_mp_courses(headers)
    
    print("\n📚 Création du contenu...")
    create_content(headers)
    
    print("\n✅ Terminé!")
    print("   - 3 cours créés")
    print("   - 3 exercices QCM créés")
    print("   - Tutoriels MP conservés")

if __name__ == "__main__":
    main()
