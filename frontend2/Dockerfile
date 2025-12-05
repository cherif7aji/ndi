# Utiliser Node.js 18
FROM node:18-alpine

WORKDIR /app

# Copier les fichiers package
COPY package*.json ./

# Installer les dépendances
RUN npm ci --silent

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 3000

# Démarrer l'application React en mode production
CMD ["npm", "start"]
