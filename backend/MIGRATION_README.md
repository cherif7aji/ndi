# 🔄 Migration Utilisateurs - CyberSec Academy

## 📋 Changements apportés

### Modèle Utilisateur simplifié
La table `utilisateurs` a été simplifiée pour ne conserver que les champs essentiels :

**Avant :**
```python
class Utilisateur(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)          # ❌ SUPPRIMÉ
    prenom = Column(String(100), nullable=False)       # ❌ SUPPRIMÉ  
    email = Column(String(255), unique=True, nullable=False)  # ❌ SUPPRIMÉ
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    # ... autres champs
```

**Après :**
```python
class Utilisateur(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)  # ✅ CONSERVÉ
    password_hash = Column(String(255), nullable=False)         # ✅ CONSERVÉ
    role = Column(String(20), default="user")                   # ✅ CONSERVÉ
    # ... autres champs (jokers, timestamps, etc.)
```

### Schémas Pydantic mis à jour

**UtilisateurCreate :**
```python
class UtilisateurCreate(BaseModel):
    username: str    # ✅ Seul champ requis
    password: str    # ✅ Seul champ requis
```

**UtilisateurResponse :**
```python
class UtilisateurResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    is_active: bool
    joker_1: bool
    joker_2: bool  
    joker_3: bool
```

## 🛠️ Scripts de migration

### 1. Migration de la base de données
```bash
python migrate_user_table.py
```
- Supprime les colonnes `nom`, `prenom`, `email`
- Sauvegarde automatique avant modification
- Vérification de la structure finale

### 2. Création d'un administrateur
```bash
python create_admin_simple.py
```
- Crée un admin avec `username: admin` et `password: admin123`
- Vérifie qu'aucun admin n'existe déjà

### 3. Création d'utilisateurs normaux
```bash
python create_user.py
```
- Interface interactive pour créer des utilisateurs
- Demande seulement `username` et `password`

## 🔧 Services mis à jour

### AuthService.register_user()
```python
def register_user(self, user_data: UtilisateurCreate) -> Utilisateur:
    # Vérification uniquement sur username (plus d'email)
    existing_user = self.db.query(Utilisateur).filter(
        Utilisateur.username == user_data.username
    ).first()
    
    # Création simplifiée
    db_user = Utilisateur(
        username=user_data.username,
        password_hash=hashed_password,
        role="user"
    )
```

## 📡 API Endpoints

### POST /auth/register
```json
{
  "username": "monusername",
  "password": "monpassword"
}
```

### POST /auth/login  
```json
{
  "username": "monusername",
  "password": "monpassword"
}
```

### GET /auth/me
```json
{
  "id": 1,
  "username": "monusername",
  "role": "user",
  "created_at": "2024-12-04T19:00:00Z",
  "is_active": true,
  "joker_1": true,
  "joker_2": true,
  "joker_3": true
}
```

## ⚠️ Points d'attention

### Données existantes
- Les utilisateurs existants perdront leurs informations `nom`, `prenom`, `email`
- Seuls `username`, `password_hash` et autres champs système sont conservés
- Faire une sauvegarde avant migration !

### Validation frontend
- Mettre à jour les formulaires d'inscription
- Supprimer les champs nom, prénom, email
- Adapter la validation côté client

### Tests
- Tester l'inscription avec les nouveaux champs
- Vérifier la connexion existante
- Valider les endpoints API

## 🚀 Avantages

1. **Simplicité** - Interface d'inscription plus simple
2. **Performance** - Moins de données à valider/stocker  
3. **Maintenance** - Moins de champs à gérer
4. **Sécurité** - Moins d'informations personnelles stockées
5. **Rapidité** - Inscription plus rapide pour les utilisateurs

---

**Migration prête !** ✅
