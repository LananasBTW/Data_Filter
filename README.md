# Projet Data Filter

## 📋 Description du Projet

Projet Python réalisé dans le cadre de la formation **3ème année IABD** à l'ESGI.

L'objectif de ce projet est de développer un programme permettant de **manipuler des données structurées** (chargement, sauvegarde, filtrage, tri et affichage) à partir de différents formats de fichiers.

## 🎯 Objectifs Pédagogiques

Ce projet permet de mettre en pratique les compétences suivantes :
- Manipulation de fichiers en Python (CSV, JSON, XML, YAML)
- Traitement et analyse de données structurées
- Conception d'algorithmes de filtrage et de tri
- Calcul de statistiques sur des données
- Développement d'une interface utilisateur
- Architecture et organisation de code Python

## 🗂️ Types de Données Supportées

Le programme traite des données structurées sous forme de **liste de dictionnaires**, où chaque entrée possède les mêmes champs.

### Structures de Données


### Types de Valeurs Supportées
- **Entiers** (int)
- **Réels** (float)
- **Chaînes de caractères** (str)
- **Booléens** (bool)
- **Listes** de valeurs des types ci-dessus

## ⚙️ Fonctionnalités

### 1. **Chargement et Sauvegarde**
- ✅ **Formats obligatoires** : CSV, JSON
- 🚀 **Formats bonus** : XML, YAML

### 2. **Statistiques**
Affichage de la structure des données avec :
- **Champs numériques** : minimum, maximum, moyenne
- **Champs booléens** : pourcentage de vrai et de faux
- **Champs listes** : statistiques sur la taille des listes (min, max, moyenne)

### 3. **Filtrage**
#### Fonctionnalités de base :
- Comparaison avec une valeur pour tous les types de champs
- Pour les chaînes : ordre lexicographique
- Pour les listes : comparaison du nombre d'éléments

#### Fonctionnalités avancées :
- **Chaînes** : contient, commence par, finit par
- **Listes** : règles complexes (tous les éléments, min/max/moyenne)
- **Comparaison entre champs** (ex: prénom avant nom alphabétiquement)
- **Comparaison avec statistiques globales** (ex: plus vieux que la moyenne)
- **Combinaison de champs** (ex: valeur globale = prix × quantité)

### 4. **Tri**
#### Fonctionnalités de base :
- Tri par valeur d'un champ

#### Fonctionnalités avancées :
- Tri par combinaison de champs (ex: valeur globale)
- Tri multi-critères (ex: nom puis prénom)

### 5. **Interface Utilisateur**
Choix libre parmi :
- Ligne de commande avec arguments
- Menu interactif en console
- Interface graphique (GUI)

### 6. **Améliorations Possibles** 🌟
- Historique des filtrages avec undo/redo
- Ajout/suppression dynamique de champs

## 📁 Structure du Projet

```
Projet Data Filter/
├── main.ipynb          # Notebook de démonstration (non obligatoire)
├── Students.py         # Script principal ou module
├── data/               # Dossiers de données
│   ├── students/       # Données d'étudiants
│   │   ├── data.csv
│   │   └── data.yml
│   └── items/          # Données d'articles
│       ├── data.csv
│       └── data.yml
├── documentation/      # Documentation du projet
└── README.md          # Ce fichier
```

## 🚀 Exécution du Programme

Le programme doit être un **script Python exécutable** en ligne de commande :

```bash
python Students.py [arguments]
```

⚠️ **Important** : Le programme ne doit **pas** dépendre de Jupyter ou d'un environnement similaire.

## 📊 Critères d'Évaluation

### Pour avoir la moyenne (10/20) :
- ✅ Chargement/Sauvegarde en CSV et JSON
- ✅ Affichage des statistiques de base
- ✅ Filtrage de base (comparaison avec une valeur)
- ✅ Tri de base (par un champ)
- ✅ Interface fonctionnelle
- ✅ Code sans bugs majeurs
- ✅ Bon découpage et organisation du code

### Pour aller au-delà (>10/20) :
- 🚀 Support XML et YAML
- 🚀 Filtrages avancés
- 🚀 Tris multi-critères
- 🚀 Interface utilisateur de qualité
- 🚀 Historique undo/redo
- 🚀 Gestion dynamique des champs

## 🛠️ Technologies Utilisées

- **Python 3.x**
- Modules standards : `csv`, `json`
- Modules optionnels : `xml`, `yaml`, `tkinter` (pour GUI), etc.

## 👨‍🎓 Informations

- **Formation** : 3ème année IABD
- **École** : ESGI
- **Année** : 2025

---

📝 **Note** : Ce README sera complété au fur et à mesure de l'avancement du projet avec les détails d'implémentation et les instructions d'utilisation spécifiques.
