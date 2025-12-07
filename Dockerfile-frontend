# Frontend Dockerfile
FROM node:22-alpine

WORKDIR /app

# On copie d'abord les fichiers de dépendances pour profiter du cache Docker
COPY frontend/package*.json .

# Installation propre des dépendances
RUN npm install

# On copie le reste (le code source)
COPY frontend/ .

# Variable d'environnement pour l'URL de l'API
ENV VITE_API_URL=http://localhost:8000/datafilter

# On expose le port de Vite
EXPOSE 5173

# Commande de démarrage
# --host est OBLIGATOIRE pour que Docker expose le site vers l'extérieur
CMD ["npm", "run", "dev", "--", "--host"]