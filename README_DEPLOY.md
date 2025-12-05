# 🚀 Déploiement Automatique - CyberSec Academy

## 📦 Déploiement en 3 étapes

### 1️⃣ Sur le VPS - Cloner le projet
```bash
# Se connecter au VPS
ssh user@72.61.197.180

# Cloner le projet
git clone <url-de-votre-repo> cybersec-academy
cd cybersec-academy
```

### 2️⃣ Lancer le script de déploiement
```bash
./deploy.sh
```

### 3️⃣ C'est tout! 🎉

Le script va automatiquement:
- ✅ Installer Docker et Docker Compose (si nécessaire)
- ✅ Arrêter les anciens conteneurs
- ✅ Build les images Docker
- ✅ Démarrer les services
- ✅ Afficher les URLs d'accès

## 🌐 Accès à l'application

Après le déploiement:
- **Frontend**: http://72.61.197.180:4000
- **Backend**: http://72.61.197.180:9000
- **API Docs**: http://72.61.197.180:9000/docs

## 🔧 Commandes utiles

```bash
# Voir les logs en temps réel
docker compose logs -f

# Arrêter l'application
docker compose down

# Redémarrer
docker compose restart

# Voir le statut
docker compose ps

# Mettre à jour l'application
git pull
./deploy.sh
```

## 🔒 Sécurité - Ouvrir les ports

```bash
# Avec UFW (Ubuntu/Debian)
sudo ufw allow 4000/tcp
sudo ufw allow 9000/tcp
sudo ufw enable
sudo ufw status

# Avec firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=4000/tcp
sudo firewall-cmd --permanent --add-port=9000/tcp
sudo firewall-cmd --reload
```

## 🐛 Dépannage

### Le script ne se lance pas
```bash
chmod +x deploy.sh
./deploy.sh
```

### Problème de permissions Docker
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Voir les erreurs détaillées
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Redémarrer complètement
```bash
docker compose down -v
docker system prune -a -f
./deploy.sh
```

## 📝 Structure des ports

- **Port 4000**: Frontend React (sans nginx)
- **Port 9000**: Backend FastAPI
- Base de données: SQLite (dans le conteneur backend)

## 🔄 Mise à jour de l'application

```bash
# Sur le VPS
cd cybersec-academy
git pull
./deploy.sh
```

C'est aussi simple que ça! 🎉
