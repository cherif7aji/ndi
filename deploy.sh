#!/bin/bash

# Script de déploiement automatique - CyberSec Academy
# Usage: ./deploy.sh

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement de CyberSec Academy..."
echo "======================================"

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    echo "Installation de Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}✅ Docker installé${NC}"
fi

# Détecter la commande docker compose (v1 ou v2)
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    echo -e "${RED}❌ Docker Compose n'est pas installé${NC}"
    echo "Installation de Docker Compose..."
    sudo apt-get update
    sudo apt-get install -y docker-compose-plugin
    DOCKER_COMPOSE="docker compose"
    echo -e "${GREEN}✅ Docker Compose installé${NC}"
fi

echo -e "${BLUE}📦 Utilisation de: ${DOCKER_COMPOSE}${NC}"

# Arrêter et supprimer les anciens conteneurs s'ils existent
echo -e "${BLUE}🛑 Arrêt et suppression des anciens conteneurs...${NC}"
$DOCKER_COMPOSE down 2>/dev/null || true

# Supprimer les conteneurs orphelins avec podman/docker
echo -e "${BLUE}🧹 Nettoyage des conteneurs orphelins...${NC}"
docker rm -f cybersec_backend cybersec_frontend 2>/dev/null || true
podman rm -f cybersec_backend cybersec_frontend 2>/dev/null || true

# Nettoyer les anciennes images (optionnel)
echo -e "${BLUE}🧹 Nettoyage des anciennes images...${NC}"
docker system prune -f

# Build des images
echo -e "${BLUE}🔨 Build des images Docker...${NC}"
$DOCKER_COMPOSE build --no-cache

# Démarrer les conteneurs
echo -e "${BLUE}🚀 Démarrage des conteneurs...${NC}"
$DOCKER_COMPOSE up -d

# Attendre que les services soient prêts
echo -e "${BLUE}⏳ Attente du démarrage des services...${NC}"
sleep 10

# Vérifier le statut
echo -e "${BLUE}📊 Statut des conteneurs:${NC}"
$DOCKER_COMPOSE ps

# Afficher les logs
echo -e "${BLUE}📋 Derniers logs:${NC}"
$DOCKER_COMPOSE logs --tail=20

# Récupérer l'IP du serveur
SERVER_IP=$(hostname -I | awk '{print $1}')

echo ""
echo -e "${GREEN}======================================"
echo "✅ Déploiement terminé avec succès!"
echo "======================================${NC}"
echo ""
echo -e "${GREEN}🌐 Accès à l'application:${NC}"
echo -e "   Frontend: ${BLUE}http://${SERVER_IP}:4000${NC}"
echo -e "   Backend:  ${BLUE}http://${SERVER_IP}:9000${NC}"
echo -e "   API Docs: ${BLUE}http://${SERVER_IP}:9000/docs${NC}"
echo ""
echo -e "${GREEN}📊 Commandes utiles:${NC}"
echo "   Voir les logs:        docker compose logs -f"
echo "   Arrêter:              docker compose down"
echo "   Redémarrer:           docker compose restart"
echo "   Voir le statut:       docker compose ps"
echo ""
