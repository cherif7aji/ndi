# 🛡️ CyberSec Academy - Frontend

Interface React moderne pour la plateforme d'apprentissage de cybersécurité.

## 🚀 Démarrage rapide

### Prérequis
- Node.js 16+ 
- Backend FastAPI en cours d'exécution sur le port 8000

### Installation
```bash
npm install
npm start
```

L'application sera disponible sur [http://localhost:3000](http://localhost:3000)

## 🏗️ Architecture

### Structure du projet
```
src/
├── components/          # Composants réutilisables
│   ├── Sidebar.js      # Navigation latérale
│   ├── Navbar.js       # Barre de navigation
│   └── *.css           # Styles des composants
├── pages/              # Pages de l'application
│   └── Home.js         # Page d'accueil
├── services/           # Services API
│   └── api.js          # Configuration Axios et services
└── styles/             # Styles globaux
    ├── index.css       # Variables CSS et thème
    └── App.css         # Styles de l'application
```

### Composants principaux

#### 🔧 Sidebar
- Navigation latérale pliable/dépliable
- Menu avec icônes et descriptions
- Thème cybersécurité avec effets lumineux
- Responsive pour mobile

#### 📱 Navbar  
- Barre de recherche
- Notifications
- Menu utilisateur avec dropdown
- Bouton menu mobile

## 🎨 Thème cybersécurité

### Palette de couleurs
- **Vert cyber** (`#00ff41`) - Accents principaux
- **Bleu cyber** (`#00d4ff`) - Éléments interactifs  
- **Violet cyber** (`#9d4edd`) - Avatar et spéciaux
- **Rouge cyber** (`#ff073a`) - Alertes et dangers

### Effets visuels
- Animations de glow et pulsation
- Dégradés et ombres lumineuses
- Effet Matrix subtil en arrière-plan
- Transitions fluides

## 🔌 Connexion Backend

### Configuration API
- **Base URL** : `http://localhost:8000`
- **Proxy** : Configuré dans package.json
- **Auth** : JWT avec intercepteurs Axios
- **Timeout** : 10 secondes

### Services disponibles
- `AuthService` - Authentification
- `CoursService` - Gestion des cours
- `ExerciceService` - Gestion des exercices  
- `UserService` - Gestion des utilisateurs

### Exemple d'utilisation
```javascript
import { CoursService } from './services/api';

// Récupérer tous les cours
const cours = await CoursService.getAll();
```

## 📱 Responsive Design

- **Desktop** : Sidebar complète (280px)
- **Tablet** : Sidebar réduite (80px) 
- **Mobile** : Sidebar en overlay

## 🛠️ Développement

### Scripts disponibles
```bash
npm start      # Serveur de développement
npm build      # Build de production
npm test       # Tests unitaires
```

### Ajout de nouvelles pages
1. Créer le composant dans `src/pages/`
2. Ajouter la route dans `App.js`
3. Mettre à jour la navigation dans `Sidebar.js`

### Variables CSS personnalisées
Toutes les couleurs et styles sont définis dans `src/styles/index.css` avec des variables CSS pour une maintenance facile.

## 🔐 Sécurité

- Gestion automatique des tokens JWT
- Redirection automatique si non authentifié
- Validation côté client des formulaires
- Protection CSRF via tokens

## 📋 TODO

- [ ] Pages de contenu (Cours, Exercices, Lab, Users)
- [ ] Système d'authentification complet
- [ ] Gestion des erreurs globale
- [ ] Tests unitaires
- [ ] Documentation API

---

**Prêt pour le développement !** 🚀

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
