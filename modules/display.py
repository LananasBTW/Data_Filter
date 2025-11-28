import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_to_str(value):
    if isinstance(value, bool):
        return "booléen"
    elif isinstance(value, int):
        return "entier"
    elif isinstance(value, float):
        return "décimal"
    elif isinstance(value, str):
        return "texte"
    elif isinstance(value, list):
        return "liste"
    elif isinstance(value, dict):
        return "dictionnaire"
    elif value is None:
        return "nul"
    return "inconnu"

def welcome():
    print("\nBienvenue dans l'application Data Filter !\n")

def show_current_file(current_filepath, data=None):
    if not current_filepath or not data:
        print("⚠️ Aucun fichier chargé.\n")
    else:
        print(f"📂 Fichier actuel : {current_filepath}\n")
        print(f"📊 Nombre d'éléments : {len(data)}\n")

def menu(current_filepath, data=None):
    print("[ Menu Principal ]\n")
    show_current_file(current_filepath, data)
    print("1. Charger des données")
    print("2. Afficher les données")
    print("3. Afficher les statistiques")
    print("4. Filtrer les données")
    print("5. Trier les données")
    print("6. Sauvegarder les données")
    print("0. Quitter")
    
    choice = input("\nVeuillez entrer votre choix (1-6 ou 0): ")
    print()
    return choice

def request_file_path(action: str):
    path = input(f"Veuillez entrer le chemin du fichier à {action} : ")
    return path

def print_data(data, current_filepath):
    if not data:
        raise Exception("Aucune donnée à afficher.\n")
    
    clear()
    print("[ Données ]\n")
    show_current_file(current_filepath, data)
    
    # 1. Détermination des colonnes
    all_keys = set()
    for ligne in data:
        all_keys.update(ligne.keys())

    columns = sorted(list(all_keys))

    # 2. Détermination des types des colonnes
    column_types = {}
    for col in columns:
        # Prendre le type de la première valeur non-None trouvée
        column_types[col] = "Inconnu"
        for ligne in data:
            if col in ligne and ligne[col] is not None:
                column_types[col] = type_to_str(ligne[col])
                break

    # 3. Calcul des largeurs de colonnes
    widths = {col: max(len(col), len(column_types[col])) for col in columns}
    for row in data:
        for col in columns:
            value = str(row[col]) if col in row else ""
            if not value: value = ""
            
            if len(value) > widths[col]:
                widths[col] = len(value)
    
    for ligne in data:
        for col in columns:
            valeur = str(ligne[col]) if col in ligne else ""
            if not valeur: valeur = ""
            widths[col] = max(widths[col], len(valeur))

    # Un petit peu de PADDING
    padding = 4
    for col in widths:
        widths[col] += padding

    # 3. Création des lignes de séparation (ex: +-------+--------+)
    ligne_sep = "+" + "+".join(["-" * widths[c] for c in columns]) + "+"

    # 4. Affichage du Header
    print(ligne_sep)
    header = "|" + "|".join([f"{col:^{widths[col]}}" for col in columns]) + "|"
    print(header)
    print(ligne_sep)

    # 5. Affichage des types de données
    type_row = "|"
    for col in columns:
        type_str = f"{column_types[col]}"
        type_row += f"{type_str:^{widths[col]}}|"
    print(type_row)
    print(ligne_sep)

    # 6. Affichage des Données
    for ligne in data:
        row_str = "|"
        for col in columns:
            valeur = str(ligne[col]) if col in ligne else ""
            if not valeur: valeur = ""
            # < : align left, ^ : centered, > : align right
            if column_types[col] == "texte":
                row_str += f"{' ' * (padding//2)}{valeur:<{widths[col] - padding//2}}|"
            else:
                row_str += f"{valeur:^{widths[col]}}|" 
        print(row_str)
    print(ligne_sep + "\n")