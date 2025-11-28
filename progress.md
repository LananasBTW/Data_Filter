### 📋 Liste des choses à faire / améliorer

#### 1. Gestion des Données (Priorité Haute)
* **Réparer le chargement CSV (`fcsv.py`) :** Actuellement, `csv.DictReader` lit tout en `string`.
    * Il faut convertir les nombres ("21" $\to$ `21`).
    * Il faut convertir les booléens ("true" $\to$ `True`).
    * **Critique :** Il faut parser les listes stockées en chaînes (ex: `"[10, 12]"` $\to$ liste Python `[10, 12]`). Le module `json` ou `ast` peut aider ici.
* **Implémenter XML et YAML (`fxml.py`, `fyml.py`) :** Ces fichiers sont vides. C'est du bonus mais nécessaire pour une très bonne note.

#### 2. Logique de Traitement (Le cœur du sujet)
* **Créer `modules/stats.py` :** Le fichier est importé dans main mais non fourni (ou vide). Il faut implémenter :
    * Moyenne/Min/Max pour les nombres.
    * Pourcentage Vrai/Faux pour les booléens.
    * Stats sur la **taille** des listes (ex: moyenne du nombre de notes).
* **Créer `modules/sort.py` :**
    * Tri simple sur un champ.
    * Tri avancé (multi-critères ou sur une combinaison).
* **Créer `modules/filter.py` :**
    * Comparaison simple (=, <, >).
    * Filtres avancés (contient, commence par, règles sur les listes).

#### 3. Interface et Expérience Utilisateur
* **Améliorer l'affichage (`display.py`) :** Votre fonction `print_data` est déjà pas mal, mais peut être peaufinée (gestion des listes vides, alignement des nombres à droite).
* **Interaction Filtres/Tris :** Dans `main.py`, la récupération des critères (ex: "quel champ ?", "quelle valeur ?") doit être robuste (gérer les erreurs de saisie).

---

### 👥 Proposition de répartition (3 Personnes)

Pour éviter les conflits Git (tout le monde modifie le même fichier), je propose une séparation par **responsabilité**.

#### 👤 Personne A : "Le Gestionnaire de Fichiers" (Backend I/O)
*Son but : S'assurer que peu importe le fichier (CSV, JSON, XML), le programme reçoit une liste de dictionnaires propre.*

1.  **Terminer `fcsv.py` :** C'est la tâche la plus urgente. Implémenter la conversion automatique des types (int, float, bool, listes JSON-in-CSV) après la lecture via `csv.DictReader`.
2.  **Implémenter `fxml.py` :** Charger et sauvegarder du XML.
3.  **Implémenter `fyml.py` :** Charger et sauvegarder du YAML (nécessite souvent `pip install pyyaml`, à vérifier si autorisé, sinon parsing manuel simple).
4.  **Tests unitaires I/O :** Vérifier que charger `students.csv` donne exactement le même résultat que `students.json`.

#### 👤 Personne B : "Le Data Scientist" (Logique Mathématique)
*Son but : Faire parler les données (Stats et Tri).*

1.  **Coder `modules/stats.py` :** Créer la fonction `analyze_structure(data)` qui parcourt les données et génère le dictionnaire de statistiques selon les types (Entier, Bool, Liste).
2.  **Coder `modules/sort.py` :** Implémenter la fonction de tri.
    * Débuter par `sorted(data, key=lambda x: x[champ])`.
    * Gérer le sens (croissant/décroissant).
    * Gérer les cas d'erreurs (si le champ n'existe pas sur une ligne).

#### 👤 Personne C : "L'Architecte Interface & Filtres" (Frontend CLI & Query)
*Son but : Gérer l'interaction utilisateur et la sélection des données.*

1.  **Coder `modules/filter.py` :** C'est le module le plus complexe logiquement. Il faut une fonction qui prend `data`, un `champ`, un `opérateur` et une `valeur`, et renvoie une nouvelle liste.
2.  **Améliorer `main.py` et `display.py` :**
    * Intégrer les appels aux filtres.
    * Créer des menus pour choisir le type de filtre (ex: "1. Egal", "2. Supérieur à", "3. Contient").
    * Peaufiner l'affichage du tableau ASCII pour qu'il soit parfait.

### 📅 Résumé du plan d'action

| Rôle | Fichiers principaux impactés | Tâche prioritaire immédiate |
| :--- | :--- | :--- |
| **Personne A** | `fcsv.py`, `fxml.py`, `fyml.py` | Faire marcher la conversion des types dans le CSV (le TODO ligne 9 de `fcsv.py`). |
| **Personne B** | `stats.py`, `sort.py` | Créer le fichier `stats.py` et calculer min/max/moyenne. |
| **Personne C** | `filter.py`, `display.py`, `main.py` | Créer `filter.py` pour pouvoir filtrer par nom ou âge. |