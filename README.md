# DataFilter

Application web de filtrage et d'analyse de données avec interface Vue.js et API Django REST.

## 🌐 Application en ligne

**[https://datafilter.ptitgourmand.uk/](https://datafilter.ptitgourmand.uk/)**

## 📋 Fonctionnalités

- **Chargement de fichiers** : Support CSV, JSON, XML, YAML
- **Filtrage dynamique** : Filtrer les données par colonne et valeur
- **Tri de colonnes** : Trier les données par n'importe quelle colonne
- **Statistiques** : Analyse automatique avec graphiques
- **Export** : Sauvegarder les données filtrées en JSON
- **Pagination** : Navigation fluide dans les grands datasets

## 🛠️ Stack Technique

- **Frontend** : Vue.js 3 + Vite + Chart.js + Bootstrap
- **Backend** : Django 5.2 + Django REST Framework
- **Déploiement** : Docker + Cloudflare Tunnel
- **Base de données** : SQLite

## 🚀 Déploiement

L'application est déployée via Docker Compose avec deux conteneurs :

- **Frontend** : `datafilter-frontend` (Node 22 + Vite)
- **Backend** : `datafilter-backend` (Python 3.11 + Django)

```bash
docker-compose up -d --build
```

## 📡 API Endpoints

Base URL : `https://api.ptitgourmand.uk/datafilter/`

- `GET /files/` - Liste des fichiers disponibles
- `POST /preview/` - Aperçu du contenu d'un fichier
- `POST /load/` - Charger les données d'un fichier
- `POST /filter/` - Filtrer les données
- `POST /sort/` - Trier les données
- `GET /stats/` - Obtenir les statistiques
- `POST /save/` - Sauvegarder les données
---

*Projet hébergé sur Raspberry Pi 5 via Cloudflare Tunnel - container docker `cloudflared`*