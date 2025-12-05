#!/usr/bin/env python3
"""
Créer le tutoriel "MP - Mass Assignment" dans la base de données
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def login_admin():
    """Se connecter en tant qu'admin"""
    # Essayer plusieurs comptes admin possibles
    admin_accounts = [
        {"username": "admin", "password": "admin123"},
        {"username": "usert", "password": "usert"},
        {"username": "hacker", "password": "password123"}  # On sait qu'il est admin maintenant
    ]
    
    for login_data in admin_accounts:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            # Vérifier si c'est un admin
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if me_response.status_code == 200 and me_response.json().get("role") == "admin":
                print(f"✅ Connecté en tant qu'admin: {login_data['username']}")
                return token
    
    print("❌ Aucun compte admin trouvé")
    return None

def create_tutorial():
    """Créer le tutoriel Mass Assignment"""
    
    token = login_admin()
    if not token:
        print("❌ Impossible de se connecter")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Données du tutoriel
    tutorial_data = {
        "titre": "MP - Mass Assignment",
        "description": "Apprenez à exploiter et corriger la vulnérabilité Mass Assignment qui permet l'élévation de privilèges",
        "niveau": "Intermédiaire",
        "duree_estimee": 20,
        "paragraphes": [
            {
                "titre": "Qu'est-ce que Mass Assignment ?",
                "contenu": "Mass Assignment (affectation de masse) est une vulnérabilité qui se produit lorsqu'une application accepte automatiquement tous les paramètres envoyés par l'utilisateur sans validation appropriée. Un attaquant peut ainsi modifier des champs sensibles comme le rôle, les permissions, ou d'autres attributs critiques.",
                "type_paragraphe": "contenu",
                "ordre": 1
            },
            {
                "titre": "⚠️ Impact de la vulnérabilité",
                "contenu": "Cette faille permet à un utilisateur normal de s'octroyer des privilèges administrateur, de modifier des données sensibles, ou de contourner les contrôles d'accès. L'impact est CRITIQUE car elle peut compromettre entièrement la sécurité de l'application.",
                "type_paragraphe": "avertissement",
                "ordre": 2
            },
            {
                "titre": "Code vulnérable",
                "contenu": "Voici l'endpoint vulnérable dans notre application :\n\n@router.put('/auth/update-profile')\ndef update_profile(profile_data: dict, current_user: User, db: Session):\n    # VULNÉRABLE: Accepte tous les champs!\n    for key, value in profile_data.items():\n        if hasattr(current_user, key):\n            setattr(current_user, key, value)\n    db.commit()\n    return current_user\n\nLe problème : L'endpoint accepte un dictionnaire et applique TOUS les champs sans vérification.",
                "type_paragraphe": "contenu",
                "ordre": 3
            },
            {
                "titre": "Exploitation étape par étape",
                "contenu": "1. Créer un compte utilisateur normal\n2. Se connecter et récupérer le token JWT\n3. Envoyer une requête PUT /auth/update-profile avec le payload : {\"role\": \"admin\"}\n4. Vérifier que le rôle a été modifié avec GET /auth/me\n5. Vous êtes maintenant administrateur !",
                "type_paragraphe": "contenu",
                "ordre": 4
            },
            {
                "titre": "Démonstration pratique",
                "contenu": "Exemple de requête d'exploitation :\n\ncurl -X PUT http://localhost:8000/auth/update-profile \\\n  -H 'Authorization: Bearer YOUR_TOKEN' \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"role\": \"admin\"}'\n\nRésultat : L'utilisateur devient admin sans aucune vérification !",
                "type_paragraphe": "contenu",
                "ordre": 5
            },
            {
                "titre": "Comment corriger cette faille ?",
                "contenu": "Solution 1 - Whitelist des champs autorisés :\n\nALLOWED_FIELDS = ['username', 'email']\nfor key, value in profile_data.items():\n    if key in ALLOWED_FIELDS and hasattr(current_user, key):\n        setattr(current_user, key, value)\n\nSolution 2 - Utiliser un schéma Pydantic strict :\n\nclass ProfileUpdate(BaseModel):\n    username: Optional[str] = None\n    email: Optional[str] = None\n    # PAS de champ 'role' !\n\ndef update_profile(profile_data: ProfileUpdate, ...):\n    ...",
                "type_paragraphe": "contenu",
                "ordre": 6
            },
            {
                "titre": "Code sécurisé",
                "contenu": "Voici la version corrigée :\n\nfrom pydantic import BaseModel\n\nclass ProfileUpdate(BaseModel):\n    username: Optional[str] = None\n    email: Optional[str] = None\n\n@router.put('/auth/update-profile')\ndef update_profile(\n    profile_data: ProfileUpdate,\n    current_user: User,\n    db: Session\n):\n    # SÉCURISÉ: Seuls les champs définis sont acceptés\n    if profile_data.username:\n        current_user.username = profile_data.username\n    if profile_data.email:\n        current_user.email = profile_data.email\n    db.commit()\n    return current_user",
                "type_paragraphe": "contenu",
                "ordre": 7
            },
            {
                "titre": "ℹ️ Bonnes pratiques",
                "contenu": "1. Toujours utiliser des schémas Pydantic stricts\n2. Ne jamais accepter de dictionnaires génériques\n3. Implémenter une whitelist explicite des champs modifiables\n4. Séparer les endpoints admin des endpoints utilisateur\n5. Valider TOUS les inputs côté serveur\n6. Effectuer des tests de sécurité réguliers",
                "type_paragraphe": "info",
                "ordre": 8
            },
            {
                "titre": "Testez vos connaissances",
                "contenu": "Maintenant que vous comprenez la vulnérabilité Mass Assignment :\n\n1. Essayez d'exploiter l'endpoint /auth/update-profile\n2. Modifiez votre rôle en 'admin'\n3. Vérifiez vos nouveaux privilèges\n4. Réfléchissez à comment vous corrigeriez cette faille dans votre propre code\n\nN'oubliez pas : Cette vulnérabilité est présente dans de nombreuses applications réelles. Soyez vigilant !",
                "type_paragraphe": "contenu",
                "ordre": 9
            }
        ],
        "videos": [],
        "images_base64": []
    }
    
    print("📝 Création du tutoriel 'MP - Mass Assignment'...")
    
    response = requests.post(
        f"{BASE_URL}/cours/with-content",
        json=tutorial_data,
        headers=headers
    )
    
    if response.status_code == 201:
        cours = response.json()
        print(f"✅ Tutoriel créé avec succès!")
        print(f"   ID: {cours['id']}")
        print(f"   Titre: {cours['titre']}")
        print(f"   Paragraphes: {len(tutorial_data['paragraphes'])}")
        print(f"\n🎯 Le tutoriel est maintenant disponible dans 'Mise en pratique'")
        return cours['id']
    else:
        print(f"❌ Erreur lors de la création: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("="*60)
    print("  Création du tutoriel Mass Assignment")
    print("="*60)
    create_tutorial()
