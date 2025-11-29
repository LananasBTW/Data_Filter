# 📚 Documentation Complète - Projet Data Filter

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du Projet](#architecture-du-projet)
3. [Installation et Configuration](#installation-et-configuration)
4. [Utilisation](#utilisation)
5. [Modules et Fonctionnalités](#modules-et-fonctionnalités)
6. [Formats de Fichiers Supportés](#formats-de-fichiers-supportés)
7. [Exemples d'Utilisation](#exemples-dutilisation)
8. [Structure des Données](#structure-des-données)

---

## 🎯 Vue d'ensemble

**Data Filter** est une application Python en ligne de commande permettant de manipuler des données structurées provenant de différents formats de fichiers. Le projet a été développé dans le cadre de la formation **3ème année IABD** à l'ESGI (2025).

### Objectifs Principaux

- Charger et sauvegarder des données depuis/vers plusieurs formats (CSV, JSON, XML, YAML)
- Analyser et afficher des statistiques sur les données
- Filtrer les données selon des critères complexes
- Trier les données sur un ou plusieurs champs
- Afficher les données dans un format tabulaire lisible

### Types de Données Supportés

- **Entiers** (`int`)
- **Réels** (`float`)
- **Chaînes de caractères** (`str`)
- **Booléens** (`bool`)
- **Listes** de valeurs des types ci-dessus (`list`)

---

## 🏗️ Architecture du Projet

### Structure des Répertoires

```
Data_Filter/
├── main.py                 # Point d'entrée principal
├── config.py              # Configuration globale
├── modules/               # Modules fonctionnels
│   ├── file_manager.py    # Gestionnaire de fichiers
│   ├── display.py         # Interface utilisateur
│   ├── stats.py           # Calcul des statistiques
│   ├── filter.py          # Filtrage des données
│   ├── sort.py            # Tri des données
│   └── formats/           # Gestionnaires de formats
│       ├── fcsv.py        # Format CSV
│       ├── fjson.py      # Format JSON
│       ├── fxml.py       # Format XML
│       └── fyml.py       # Format YAML
├── data/                  # Fichiers de données d'exemple
├── output/                # Fichiers sauvegardés
└── tmp/                   # Fichiers temporaires
```

### Flux de Données

```
Fichier Source → file_manager → Format Parser → Liste de Dictionnaires
                                                      ↓
                                              [Traitement]
                                                      ↓
                                    stats / filter / sort / display
                                                      ↓
                                              Liste de Dictionnaires
                                                      ↓
                                    Format Parser → file_manager → Fichier Destination
```

---

## ⚙️ Installation et Configuration

### Prérequis

- Python 3.7 ou supérieur
- Modules Python standards (inclus) :
  - `csv`
  - `json`
  - `xml.etree.ElementTree`
- Module optionnel (pour YAML) :
  - `pyyaml` (installer avec `pip install pyyaml`)

### Configuration

Le fichier `config.py` contient les paramètres globaux :

```python
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
TAB_PADDING = 2
OUTPUT_DIR = os.path.join(CURRENT_PATH, "output/")
TMP_DIR = os.path.join(CURRENT_PATH, "tmp/")
```

### Lancement

```bash
python main.py
```

---

## 🖥️ Utilisation

### Menu Principal

L'application propose un menu interactif avec les options suivantes :

1. **Charger des données** - Charge un fichier depuis le disque
2. **Afficher les données** - Affiche les données dans un tableau formaté
3. **Afficher les statistiques** - Affiche les statistiques par champ
4. **Filtrer les données** - Applique un filtre sur les données
5. **Trier les données** - Trie les données selon un champ
6. **Sauvegarder les données** - Sauvegarde les données dans un fichier
0. **Quitter** - Ferme l'application

### Workflow Typique

1. Charger un fichier de données (option 1)
2. Examiner les statistiques (option 3)
3. Filtrer les données selon des critères (option 4)
4. Trier les résultats (option 5)
5. Afficher les données filtrées/triées (option 2)
6. Sauvegarder les résultats (option 6)

---

## 📦 Modules et Fonctionnalités

### 1. `file_manager.py` - Gestionnaire de Fichiers

**Responsabilité** : Routage des opérations de chargement/sauvegarde vers les bons parsers.

#### Fonctions Principales

- `load_data(path)` : Charge un fichier selon son extension
  - Détecte automatiquement le format (`.csv`, `.json`, `.fxml`, `.fyml`)
  - Retourne une liste de dictionnaires
  
- `save_data(data, path)` : Sauvegarde des données dans un fichier
  - Détecte automatiquement le format selon l'extension
  - Utilise un répertoire temporaire pour éviter les corruptions

- `cleanTmpDir()` : Nettoie le répertoire temporaire

### 2. `display.py` - Interface Utilisateur

**Responsabilité** : Gestion de l'affichage et de l'interaction avec l'utilisateur.

#### Fonctions Principales

- `clear()` : Efface l'écran
- `welcome()` : Affiche le message de bienvenue
- `menu(current_filepath, data)` : Affiche le menu principal
- `print_data(data, current_filepath)` : Affiche les données en tableau ASCII
  - Détection automatique des colonnes
  - Calcul des largeurs optimales
  - Affichage des types de données
  - Alignement intelligent (nombres à droite, texte à gauche)
  
- `print_stats(report)` : Affiche les statistiques formatées
- `request_filter_criteria(data)` : Demande les critères de filtrage
- `request_sort_field(data)` : Demande le champ de tri
- `request_file_path(action)` : Demande le chemin d'un fichier

### 3. `stats.py` - Statistiques

**Responsabilité** : Analyse et calcul de statistiques sur les données.

#### Fonction Principale

- `analyze_structure(data)` : Analyse la structure des données et calcule des statistiques

**Statistiques par Type** :

- **Nombres** (`int`, `float`) :
  - `min` : Valeur minimale
  - `max` : Valeur maximale
  - `mean` : Moyenne arithmétique
  - `count` : Nombre de valeurs non-nulles
  - `null_count` : Nombre de valeurs nulles

- **Booléens** (`bool`) :
  - `true_count` : Nombre de valeurs `True`
  - `false_count` : Nombre de valeurs `False`
  - `true_percentage` : Pourcentage de `True`
  - `false_percentage` : Pourcentage de `False`

- **Listes** (`list`) :
  - `list_size_min` : Taille minimale des listes
  - `list_size_max` : Taille maximale des listes
  - `list_size_mean` : Taille moyenne des listes

- **Chaînes** (`str`) :
  - `sample_values` : Exemples de valeurs (jusqu'à 3)

### 4. `filter.py` - Filtrage

**Responsabilité** : Filtrage des données selon des critères.

#### Fonctions Principales

- `filter_data(data, field, operator, value)` : Filtre les données

**Opérateurs Supportés** :

- **Comparaisons de base** :
  - `=` : Égalité
  - `!=` : Différence
  - `<` : Inférieur
  - `>` : Supérieur
  - `<=` : Inférieur ou égal
  - `>=` : Supérieur ou égal

- **Chaînes de caractères** :
  - `contains` : Contient (insensible à la casse)
  - `starts_with` : Commence par (insensible à la casse)
  - `ends_with` : Finit par (insensible à la casse)

- **Listes** :
  - `list_all` : Tous les éléments satisfont une condition
  - `list_any` : Au moins un élément satisfait une condition

**Gestion des Types** :
- Pour les nombres : comparaison numérique
- Pour les chaînes : comparaison lexicographique
- Pour les listes : comparaison sur la taille de la liste

- `filter_by_stats(data, field, operator, stat_type)` : Filtre en comparant avec les statistiques globales
  - Permet de filtrer par rapport à la moyenne, min, max d'un champ

### 5. `sort.py` - Tri

**Responsabilité** : Tri des données.

#### Fonction Principale

- `sort_data(data, field=None, reverse=False, fields=None)` : Trie les données

**Fonctionnalités** :
- Tri simple sur un champ
- Tri multi-critères (plusieurs champs)
- Tri croissant ou décroissant
- Gestion des valeurs `None` (placées à la fin)
- Tri sur la taille des listes

**Exemple de tri multi-critères** :
```python
sort_data(data, fields=[('lastname', False), ('firstname', False)])
```

### 6. Modules de Formats

#### `fcsv.py` - Format CSV

**Fonctions** :
- `load(path)` : Charge un fichier CSV
  - Utilise `csv.DictReader`
  - Conversion automatique des types via JSON parsing
  - Gère les nombres, booléens, et listes stockées en JSON
  
- `save(data, filename)` : Sauvegarde en CSV
  - Conversion des types complexes en JSON pour la sauvegarde
  - Utilise `csv.DictWriter`

**Fonctions utilitaires** :
- `convert_strToValue(value)` : Convertit une chaîne CSV en valeur Python
- `convert_valueToStr(value)` : Convertit une valeur Python en chaîne CSV

#### `fjson.py` - Format JSON

**Fonctions** :
- `load(path)` : Charge un fichier JSON
  - Utilise `json.load()`
  
- `save(data, filename, indent=4)` : Sauvegarde en JSON
  - Formatage avec indentation (4 espaces par défaut)

#### `fxml.py` - Format XML

**Fonctions** :
- `load(path)` : Charge un fichier XML
  - Utilise `xml.etree.ElementTree`
  - Structure attendue : `<data><item><champ>valeur</champ></item></data>`
  - Parse les types complexes via JSON
  
- `save(data, filename)` : Sauvegarde en XML
  - Crée une structure XML avec élément racine `<data>`
  - Chaque ligne devient un élément `<item>`
  - Chaque champ devient un sous-élément

**Structure XML générée** :
```xml
<?xml version='1.0' encoding='utf-8'?>
<data>
  <item>
    <champ1>valeur1</champ1>
    <champ2>valeur2</champ2>
  </item>
</data>
```

#### `fyml.py` - Format YAML

**Fonctions** :
- `load(path)` : Charge un fichier YAML
  - Utilise `yaml.safe_load()`
  - Nécessite `pyyaml` (gère l'erreur si absent)
  
- `save(data, filename)` : Sauvegarde en YAML
  - Formatage lisible avec `default_flow_style=False`
  - Support Unicode

**Fonctions utilitaires** :
- `_convert_value_to_yaml_compatible(value)` : Convertit une valeur pour YAML
- `_parse_yaml_value(value)` : Parse une valeur YAML

---

## 📄 Formats de Fichiers Supportés

### CSV (`.csv`)

**Caractéristiques** :
- Format tabulaire standard
- Première ligne = en-têtes
- Types complexes encodés en JSON dans les cellules

**Exemple** :
```csv
firstname,lastname,age,apprentice,grades
Alice,Dupont,21,true,"[15, 17, 14]"
```

### JSON (`.json`)

**Caractéristiques** :
- Format natif pour les structures de données
- Support complet de tous les types Python
- Formatage avec indentation

**Exemple** :
```json
[
  {
    "firstname": "Alice",
    "lastname": "Dupont",
    "age": 21,
    "apprentice": true,
    "grades": [15, 17, 14]
  }
]
```

### XML (`.fxml`)

**Caractéristiques** :
- Format structuré avec balises
- Types complexes encodés en JSON dans le texte des éléments
- Encodage UTF-8

**Exemple** :
```xml
<?xml version='1.0' encoding='utf-8'?>
<data>
  <item>
    <firstname>Alice</firstname>
    <lastname>Dupont</lastname>
    <age>21</age>
    <apprentice>true</apprentice>
    <grades>[15, 17, 14]</grades>
  </item>
</data>
```

### YAML (`.fyml`)

**Caractéristiques** :
- Format lisible par l'humain
- Support natif des types Python
- Nécessite `pyyaml`

**Exemple** :
```yaml
- firstname: Alice
  lastname: Dupont
  age: 21
  apprentice: true
  grades:
    - 15
    - 17
    - 14
```

---

## 💡 Exemples d'Utilisation

### Exemple 1 : Charger et Afficher des Données

```
1. Choisir "1. Charger des données"
2. Entrer le chemin : data/students.json
3. Choisir "2. Afficher les données"
```

### Exemple 2 : Filtrer par Âge

```
1. Charger data/students.json
2. Choisir "4. Filtrer les données"
3. Champ : age
4. Opérateur : > (choix 4)
5. Valeur : 22
```

### Exemple 3 : Trier par Nom de Famille

```
1. Charger data/students.json
2. Choisir "5. Trier les données"
3. Champ : lastname
4. Ordre : croissant (c)
```

### Exemple 4 : Statistiques sur les Notes

```
1. Charger data/students.json
2. Choisir "3. Afficher les statistiques"
3. Examiner les statistiques du champ "grades"
   - Taille moyenne des listes
   - Taille min/max
```

### Exemple 5 : Conversion de Format

```
1. Charger data/students.csv
2. Filtrer/trier selon besoin
3. Choisir "6. Sauvegarder les données"
4. Entrer : output/students_filtered.json
   → Les données sont converties en JSON
```

---

## 📊 Structure des Données

### Format Interne

Les données sont toujours représentées comme une **liste de dictionnaires** :

```python
[
    {
        "champ1": valeur1,
        "champ2": valeur2,
        ...
    },
    {
        "champ1": valeur1,
        "champ2": valeur2,
        ...
    }
]
```

### Types de Valeurs

- **Nombres** : `int` ou `float`
- **Chaînes** : `str`
- **Booléens** : `bool` (Python natif)
- **Listes** : `list` de valeurs homogènes ou hétérogènes
- **Valeurs nulles** : `None`

### Exemple Concret

```python
[
    {
        "firstname": "Alice",
        "lastname": "Dupont",
        "age": 21,
        "apprentice": True,
        "grades": [15, 17, 14]
    },
    {
        "firstname": "Bob",
        "lastname": "Martin",
        "age": 23,
        "apprentice": False,
        "grades": [8, 9, 11, 10]
    }
]
```

---

## 🔧 Détails Techniques

### Gestion des Erreurs

- **Fichier introuvable** : `FileNotFoundError` avec message explicite
- **Format non supporté** : `ValueError` avec liste des formats supportés
- **Données invalides** : Gestion gracieuse avec messages d'erreur
- **Module manquant** : Message d'erreur avec instructions d'installation (YAML)

### Gestion des Fichiers Temporaires

- Utilisation d'un répertoire temporaire (`tmp/`) pour éviter les corruptions
- Écriture dans `tmp/` puis déplacement atomique vers `output/`
- Nettoyage automatique après sauvegarde

### Performance

- Chargement en mémoire (adapté aux fichiers de taille raisonnable)
- Tri en place avec `sorted()` (stable et efficace)
- Filtrage par itération (pas de copie inutile)

---

## 📝 Notes de Développement

### Points d'Attention

1. **Conversion CSV** : Les types complexes doivent être encodés en JSON dans les cellules CSV
2. **Encodage** : Tous les fichiers texte utilisent UTF-8
3. **Compatibilité** : Les formats sont interconvertibles sans perte de données
4. **Extension YAML** : Utilise `.fyml` pour éviter les conflits avec d'autres outils

### Améliorations Possibles

- Historique des opérations (undo/redo)
- Filtres combinés (ET/OU)
- Export vers d'autres formats (Excel, etc.)
- Interface graphique (GUI)
- Traitement de fichiers volumineux (streaming)

---

## 📚 Références

- Documentation Python : https://docs.python.org/3/
- Module CSV : https://docs.python.org/3/library/csv.html
- Module JSON : https://docs.python.org/3/library/json.html
- Module XML : https://docs.python.org/3/library/xml.etree.elementtree.html
- PyYAML : https://pyyaml.org/

---

*Documentation générée pour le projet Data Filter - ESGI 2025*

