# Projet Data Filter

[![Python package](https://github.com/LananasBTW/Data_Filter/actions/workflows/python-package.yml/badge.svg)](https://github.com/LananasBTW/Data_Filter/actions/workflows/python-package.yml)

## LANCER LE PROJET :
```pwsh
pip install -r requirements.txt
python main.py
```

## 📋 Description du Projet

Projet Python réalisé dans le cadre de la formation **3ème année IABD** à l'ESGI (2025).

L'objectif est de créer un programme permettant de charger, sauvegarder, filtrer, trier et afficher des données structurées provenant de différents formats de fichiers.

## 🎯 Objectifs Pédagogiques

Ce projet vise à mettre en application les notions vues en cours de scripting Python :
- Manipulation de fichiers et formats de données.
- Traitement de structures de données (listes de dictionnaires).
- Implémentation d'algorithmes de tri et de filtrage.

## 🗂️ Types de Données Supportées

Les données sont considérées comme une série (tableau) de données structurées possédant les mêmes champs.
Le programme supporte les types de valeurs suivants :
- **Entiers**
- **Réels**
- **Chaînes de caractères**
- **Booléens**
- **Listes** de valeurs des types ci-dessus

## ⚙️ Fonctionnalités

### 1. Chargement et Sauvegarde
- **Obligatoire** : Formats CSV et JSON.
- **Avancé (Bonus)** : Formats XML et YAML.

### 2. Statistiques
Le programme affiche la structure des données et des statistiques par champ :
- **Nombres** : min, max, moyenne.
- **Booléens** : pourcentage de vrai et de faux.
- **Listes** : statistiques sur la taille des listes (min, max, moyenne).

### 3. Filtrage
Permet de ne garder qu'un sous-ensemble des données.
- **Niveau de base** : Comparaison avec une valeur (ordre lexicographique pour les chaînes, nombre d'éléments pour les listes).
- **Niveau avancé** :
    - Chaînes : contient, commence/finit par.
    - Listes : règles complexes (tous les éléments, min/max/moyenne).
    - Comparaison entre deux champs.
    - Comparaison avec des statistiques globales (ex: plus vieux que la moyenne).
    - Combinaison de champs (ex: prix × quantité > seuil).

### 4. Tri
- **Niveau de base** : Tri par la valeur d'un champ.
- **Niveau avancé** : Tri sur une combinaison de champs ou tri multi-critères (ex: nom puis prénom).

### 5. Interface Utilisateur
Le choix de l'interface est libre :
- Ligne de commande
- Menu
- Interface graphique
*La qualité et la facilité d'utilisation entrent en compte dans la notation.*

### 6. Améliorations (Bonus)
- Historique des filtrages avec undo/redo.
- Possibilité d'ajouter ou retirer des champs dynamiquement.

## 🚀 Exécution du Programme

Le programme est un script exécutable en console via l'interpréteur Python. Il ne dépend pas de Jupyter Notebook.

```bash
python run.py
````

## 📊 Critères d'Évaluation

**Pour avoir la moyenne :**
Réalisation convenable (sans bugs, bon découpage) des fonctionnalités de base (chargement/sauvegarde CSV/JSON, stats de base, filtrage simple, tri simple).

**Pour avoir plus de la moyenne :**
Ajout d'améliorations et fonctionnalités avancées (formats XML/YAML, filtres complexes, tris multi-critères, interface soignée, undo/redo, etc.).

## 🛠️ Technologies

  - **Langage** : Python
  - **Modules** : Utilisation de modules standards (csv, json) et optionnels selon les besoins (xml, yaml, etc.).

-----

*Basé sur le sujet [Projet data filter](./documentation/Sujet.pdf)*
