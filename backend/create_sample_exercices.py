#!/usr/bin/env python3
"""
Script pour créer des exercices de test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Exercice, Question, Solution, Paragraphe, Cours

def create_sample_exercices():
    """Créer des exercices de test"""
    db: Session = SessionLocal()
    
    try:
        # Vérifier si un cours existe, sinon en créer un
        cours = db.query(Cours).first()
        if not cours:
            print("Création d'un cours de test...")
            cours = Cours(
                titre="Introduction à la Cybersécurité",
                description="Cours d'introduction aux concepts de base",
                niveau="Débutant",
                duree_estimee=120,
                ordre=1
            )
            db.add(cours)
            db.commit()
            db.refresh(cours)
            print(f"✅ Cours créé: {cours.titre} (ID: {cours.id})")
        else:
            print(f"📚 Utilisation du cours existant: {cours.titre} (ID: {cours.id})")
        
        # Exercice 1: QCM sur les bases de la sécurité
        print("\n🎯 Création de l'exercice 1: QCM Sécurité de base")
        ex1 = Exercice(
            cours_id=cours.id,
            titre="Quiz: Fondamentaux de la Sécurité",
            description="Testez vos connaissances sur les concepts de base de la cybersécurité",
            type_exercice="QCM",
            difficulte="facile",
            points_max=100,
            temps_limite=15,
            ordre=1
        )
        db.add(ex1)
        db.flush()
        
        # Questions pour exercice 1
        q1 = Question(
            exercice_id=ex1.id,
            texte_question="Qu'est-ce qu'une attaque par injection SQL ?",
            type_question="multiple_choice",
            points=25,
            ordre=1,
            option_a="Une attaque qui injecte du code SQL malveillant dans une application",
            option_b="Une attaque qui vole des mots de passe",
            option_c="Un virus informatique",
            option_d="Une technique de cryptage",
            bonne_reponse="A"
        )
        
        q2 = Question(
            exercice_id=ex1.id,
            texte_question="Que signifie XSS ?",
            type_question="multiple_choice",
            points=25,
            ordre=2,
            option_a="eXtreme Security System",
            option_b="Cross-Site Scripting",
            option_c="eXternal Server Script",
            option_d="X-Security Standard",
            bonne_reponse="B"
        )
        
        q3 = Question(
            exercice_id=ex1.id,
            texte_question="Quel est le rôle d'un pare-feu (firewall) ?",
            type_question="multiple_choice",
            points=25,
            ordre=3,
            option_a="Crypter les données",
            option_b="Filtrer le trafic réseau",
            option_c="Détecter les virus",
            option_d="Sauvegarder les données",
            bonne_reponse="B"
        )
        
        q4 = Question(
            exercice_id=ex1.id,
            texte_question="Qu'est-ce que l'authentification à deux facteurs (2FA) ?",
            type_question="multiple_choice",
            points=25,
            ordre=4,
            option_a="Utiliser deux mots de passe différents",
            option_b="Se connecter deux fois",
            option_c="Utiliser deux méthodes de vérification d'identité",
            option_d="Avoir deux comptes utilisateurs",
            bonne_reponse="C"
        )
        
        db.add_all([q1, q2, q3, q4])
        
        # Solution pour exercice 1
        sol1 = Solution(
            exercice_id=ex1.id,
            titre="Explications des réponses",
            explication="""
1. L'injection SQL permet d'injecter du code SQL malveillant dans les requêtes.
2. XSS signifie Cross-Site Scripting, une vulnérabilité web courante.
3. Un pare-feu filtre le trafic réseau entrant et sortant.
4. La 2FA utilise deux méthodes différentes (ex: mot de passe + code SMS).
            """,
            ressources_supplementaires="https://owasp.org/www-project-top-ten/"
        )
        db.add(sol1)
        
        # Exercice 2: Recherche de faille
        print("🎯 Création de l'exercice 2: Recherche de faille SQL")
        ex2 = Exercice(
            cours_id=cours.id,
            titre="Défi: Trouver la faille SQL",
            description="Analysez le code et identifiez la vulnérabilité d'injection SQL",
            type_exercice="recherche_faille",
            difficulte="moyen",
            points_max=150,
            temps_limite=30,
            ordre=2
        )
        db.add(ex2)
        db.flush()
        
        # Paragraphe avec code vulnérable
        para1 = Paragraphe(
            exercice_id=ex2.id,
            titre="Code vulnérable",
            contenu="""Voici un extrait de code PHP :

```php
$username = $_POST['username'];
$password = $_POST['password'];
$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($conn, $query);
```

Analysez ce code et identifiez la vulnérabilité.""",
            type_paragraphe="contenu",
            ordre=1
        )
        db.add(para1)
        
        q5 = Question(
            exercice_id=ex2.id,
            texte_question="Quelle est la principale vulnérabilité dans ce code ?",
            type_question="multiple_choice",
            points=50,
            ordre=1,
            option_a="Mot de passe en clair",
            option_b="Injection SQL",
            option_c="XSS",
            option_d="CSRF",
            bonne_reponse="B"
        )
        
        q6 = Question(
            exercice_id=ex2.id,
            texte_question="Quel payload pourrait exploiter cette faille ? (réponse libre)",
            type_question="text",
            points=50,
            ordre=2,
            reponse_attendue="' OR '1'='1"
        )
        
        q7 = Question(
            exercice_id=ex2.id,
            texte_question="Comment corriger cette vulnérabilité ? (réponse libre)",
            type_question="text",
            points=50,
            ordre=3,
            reponse_attendue="prepared statements"
        )
        
        db.add_all([q5, q6, q7])
        
        # Solution pour exercice 2
        sol2 = Solution(
            exercice_id=ex2.id,
            titre="Solution: Injection SQL",
            explication="""
La vulnérabilité est une injection SQL causée par la concaténation directe 
des entrées utilisateur dans la requête SQL.

Un attaquant peut entrer: ' OR '1'='1' -- 
pour bypasser l'authentification.
            """,
            code_solution="""// Code corrigé avec prepared statements
$stmt = $conn->prepare("SELECT * FROM users WHERE username=? AND password=?");
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
$result = $stmt->get_result();""",
            ressources_supplementaires="https://owasp.org/www-community/attacks/SQL_Injection"
        )
        db.add(sol2)
        
        # Exercice 3: Pratique XSS
        print("🎯 Création de l'exercice 3: Pratique XSS")
        ex3 = Exercice(
            cours_id=cours.id,
            titre="Pratique: Exploitation XSS",
            description="Créez un payload XSS pour afficher une alerte",
            type_exercice="pratique",
            difficulte="difficile",
            points_max=200,
            temps_limite=45,
            ordre=3
        )
        db.add(ex3)
        db.flush()
        
        para2 = Paragraphe(
            exercice_id=ex3.id,
            titre="Contexte",
            contenu="""Un site web affiche les commentaires des utilisateurs sans filtrage.
Le code HTML généré est:
<div class="comment">Votre commentaire ici</div>

Votre mission: créer un payload XSS qui affiche une alerte JavaScript.""",
            type_paragraphe="info",
            ordre=1
        )
        db.add(para2)
        
        q8 = Question(
            exercice_id=ex3.id,
            texte_question="Écrivez un payload XSS simple qui affiche une alerte",
            type_question="code",
            points=100,
            ordre=1,
            reponse_attendue="<script>alert('XSS')</script>"
        )
        
        q9 = Question(
            exercice_id=ex3.id,
            texte_question="Comment se protéger contre les attaques XSS ?",
            type_question="multiple_choice",
            points=50,
            ordre=2,
            option_a="Encoder/échapper les entrées utilisateur",
            option_b="Utiliser HTTPS",
            option_c="Changer régulièrement les mots de passe",
            option_d="Installer un antivirus",
            bonne_reponse="A"
        )
        
        q10 = Question(
            exercice_id=ex3.id,
            texte_question="Quelle en-tête HTTP aide à prévenir XSS ?",
            type_question="text",
            points=50,
            ordre=3,
            reponse_attendue="Content-Security-Policy"
        )
        
        db.add_all([q8, q9, q10])
        
        sol3 = Solution(
            exercice_id=ex3.id,
            titre="Solution XSS",
            explication="""
Payload de base: <script>alert('XSS')</script>

Protection:
1. Encoder les entrées utilisateur (htmlspecialchars en PHP)
2. Utiliser Content-Security-Policy
3. Valider et filtrer les entrées
4. Utiliser des frameworks avec protection intégrée
            """,
            code_solution="""// Protection en PHP
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');

// En-tête CSP
Content-Security-Policy: default-src 'self'; script-src 'self'""",
            ressources_supplementaires="https://owasp.org/www-community/attacks/xss/"
        )
        db.add(sol3)
        
        db.commit()
        
        print("\n✅ Exercices créés avec succès!")
        print(f"   - Exercice 1: {ex1.titre} ({ex1.difficulte}, {len([q1,q2,q3,q4])} questions)")
        print(f"   - Exercice 2: {ex2.titre} ({ex2.difficulte}, {len([q5,q6,q7])} questions)")
        print(f"   - Exercice 3: {ex3.titre} ({ex3.difficulte}, {len([q8,q9,q10])} questions)")
        print(f"\n🎓 Cours associé: {cours.titre}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🛡️  CyberSec Academy - Création d'exercices de test")
    print("=" * 60)
    create_sample_exercices()
