import os
import config
import modules.utils as utils

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_to_str(value):
    return utils.get_type_str(value)

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
    print()
    return path



def print_data(data, current_filepath):
    if not data:
        raise Exception("Aucune donnée à afficher.\n")
    
    clear()
    print("[ Données ]\n")
    show_current_file(current_filepath, data)
    
    # 1. Détermination des colonnes
    columns = utils.get_all_columns(data)

    # 2. Détermination des types des colonnes
    col_types = utils.get_column_types(data)
    col_types_str = {}
    for col, types in col_types.items():
        # Construire la chaîne de types
        type_parts = []
        if "list" in types["base"]:
            if types["sub"]:
                list_types_str = ",".join(sorted(types["sub"]))
                type_parts.append(f"list of {list_types_str}")
            else:
                type_parts.append("list")
            # Ajouter les autres types non-list
            other_types = sorted(types["base"] - {"list"})
            type_parts.extend(other_types)
        else:
            type_parts = sorted(types["base"])
        
        # Afficher tous les types séparés par " | "
        if type_parts:
            col_types_str[col] = " | ".join(type_parts)
        else:
            col_types_str[col] = "unknown"

    # 3. Calcul des largeurs de colonnes
    widths = {col: max(len(col), len(col_types_str[col])) for col in columns}
    for row in data:
        for col in columns:
            value = str(row[col]) if col in row else ""
            if not value: value = ""
            
            if len(value) > widths[col]:
                widths[col] = len(value)
    
    for ligne in data:
        for col in columns:
            value = str(ligne[col]) if col in ligne else ""
            if not value: value = ""
            widths[col] = max(widths[col], len(value))

    # Un petit peu de PADDING
    for col in widths:
        widths[col] += config.TAB_PADDING * 2

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
        type_str = f"{col_types_str[col]}"
        type_row += f"{type_str:^{widths[col]}}|"
    print(type_row)
    print(ligne_sep)

    # 6. Affichage des Données
    for ligne in data:
        row_str = "|"
        for col in columns:
            type = col_types_str[col].split()[0]
            value = ligne[col] if col in ligne else ""
            value = 1 if value == True else 0 if value == False else value
            value = str(value)

            # < : align left, ^ : centered, > : align right
            if type in ["bool", "int"]:
                row_str += f"{' ' * (config.TAB_PADDING//2)}{value:^{widths[col] - config.TAB_PADDING//2}}|"
            else:
                row_str += f"{' ' * (config.TAB_PADDING//2)}{value:<{widths[col] - config.TAB_PADDING//2}}|"
    
        print(row_str)
    
    print(ligne_sep + "\n")