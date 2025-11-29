import os
import config

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_to_str(value):
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    elif value is None:
        return "None"
    return "unknown"

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
    all_keys = set()
    for ligne in data:
        all_keys.update(ligne.keys())

    columns = sorted(list(all_keys))

    # 2. Détermination des types des colonnes
    column_types = {}
    for col in columns:
        # Collecter tous les types uniques trouvés dans cette colonne
        base_types = set()
        list_item_types = set()
        
        for ligne in data:
            if col in ligne and ligne[col] is not None:
                type_str = type_to_str(ligne[col])
                if type_str == "list" and isinstance(ligne[col], list):
                    base_types.add("list")
                    # Collecter tous les types d'éléments dans la liste
                    for item in ligne[col]:
                        list_item_types.add(type_to_str(item))
                else:
                    base_types.add(type_str)
        
        # Construire la chaîne de types
        type_parts = []
        if "list" in base_types:
            if list_item_types:
                list_types_str = ",".join(sorted(list_item_types))
                type_parts.append(f"list of {list_types_str}")
            else:
                type_parts.append("list")
            # Ajouter les autres types non-list
            other_types = sorted(base_types - {"list"})
            type_parts.extend(other_types)
        else:
            type_parts = sorted(base_types)
        
        # Afficher tous les types séparés par " | "
        if type_parts:
            column_types[col] = " | ".join(type_parts)
        else:
            column_types[col] = "unknown"

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
        type_str = f"{column_types[col]}"
        type_row += f"{type_str:^{widths[col]}}|"
    print(type_row)
    print(ligne_sep)

    # 6. Affichage des Données
    for ligne in data:
        row_str = "|"
        for col in columns:
            type = column_types[col].split()[0]
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

def request_filter_criteria(data=None):
    """
    Demande à l'utilisateur les critères de filtrage.
    
    Args:
        data: Données actuelles (optionnel, pour afficher les champs disponibles)
        
    Returns:
        tuple: (field, operator, value) ou (field, value) pour compatibilité
    """
    print("[ Filtrage des données ]\n")
    
    # Afficher les champs disponibles si des données sont fournies
    if data and len(data) > 0:
        available_fields = sorted(list(data[0].keys()))
        print("Champs disponibles:", ", ".join(available_fields))
        print()
    
    field = input("Entrez le nom du champ à filtrer : ").strip()
    if not field:
        return None, None, None
    
    print("\nOpérateurs disponibles:")
    print("1. = (égal)")
    print("2. != (différent)")
    print("3. < (inférieur)")
    print("4. > (supérieur)")
    print("5. <= (inférieur ou égal)")
    print("6. >= (supérieur ou égal)")
    print("7. contains (contient - pour chaînes)")
    print("8. starts_with (commence par - pour chaînes)")
    print("9. ends_with (finit par - pour chaînes)")
    
    operator_choice = input("\nChoisissez un opérateur (1-9) : ").strip()
    
    operator_map = {
        '1': '=',
        '2': '!=',
        '3': '<',
        '4': '>',
        '5': '<=',
        '6': '>=',
        '7': 'contains',
        '8': 'starts_with',
        '9': 'ends_with'
    }
    
    operator = operator_map.get(operator_choice)
    if not operator:
        print("⚠️ Opérateur invalide, utilisation de '=' par défaut.")
        operator = '='
    
    # Demander la valeur
    value_str = input(f"Entrez la valeur de comparaison : ").strip()
    
    # Essayer de convertir la valeur selon le type
    value = value_str
    try:
        # Essayer d'abord comme nombre entier
        if '.' not in value_str:
            value = int(value_str)
        else:
            value = float(value_str)
    except ValueError:
        # Essayer comme booléen
        if value_str.lower() in ['true', 'vrai', '1', 'yes', 'oui']:
            value = True
        elif value_str.lower() in ['false', 'faux', '0', 'no', 'non']:
            value = False
        else:
            # Garder comme chaîne
            value = value_str
    
    print()
    return field, operator, value

def request_sort_field(data=None):
    """
    Demande à l'utilisateur le champ de tri.
    
    Args:
        data: Données actuelles (optionnel, pour afficher les champs disponibles)
        
    Returns:
        str: Nom du champ de tri
    """
    print("[ Tri des données ]\n")
    
    # Afficher les champs disponibles si des données sont fournies
    if data and len(data) > 0:
        available_fields = sorted(list(data[0].keys()))
        print("Champs disponibles:", ", ".join(available_fields))
        print()
    
    field = input("Entrez le nom du champ de tri : ").strip()
    
    if not field:
        return None, False
    
    order = input("Ordre de tri (c)roissant ou (d)écroissant ? [c] : ").strip().lower()
    reverse = order == 'd'
    
    print()
    return field, reverse

def print_stats(report):
    """
    Affiche les statistiques des données.
    
    Args:
        report: Dictionnaire de statistiques généré par stats.analyze_structure()
    """
    if not report:
        print("⚠️ Aucune statistique disponible.\n")
        return
    
    clear()
    print("[ Statistiques ]\n")
    
    for field, field_stats in sorted(report.items()):
        print(f"📊 Champ: {field}")
        print(f"   Type: {field_stats.get('type', 'unknown')}")
        print(f"   Nombre de valeurs: {field_stats.get('count', 0)}")
        
        if field_stats.get('null_count', 0) > 0:
            print(f"   Valeurs nulles: {field_stats.get('null_count', 0)}")
        
        field_type = field_stats.get('type')
        
        if field_type == 'number':
            if 'min' in field_stats:
                print(f"   Minimum: {field_stats['min']}")
            if 'max' in field_stats:
                print(f"   Maximum: {field_stats['max']}")
            if 'mean' in field_stats:
                print(f"   Moyenne: {field_stats['mean']:.2f}")
        
        elif field_type == 'bool':
            if 'true_percentage' in field_stats:
                print(f"   Vrai: {field_stats['true_count']} ({field_stats['true_percentage']:.1f}%)")
            if 'false_percentage' in field_stats:
                print(f"   Faux: {field_stats['false_count']} ({field_stats['false_percentage']:.1f}%)")
        
        elif field_type == 'list':
            if 'list_size_min' in field_stats:
                print(f"   Taille min: {field_stats['list_size_min']}")
            if 'list_size_max' in field_stats:
                print(f"   Taille max: {field_stats['list_size_max']}")
            if 'list_size_mean' in field_stats:
                print(f"   Taille moyenne: {field_stats['list_size_mean']:.2f}")
        
        elif field_type == 'str':
            if 'sample_values' in field_stats and field_stats['sample_values']:
                samples = ", ".join(field_stats['sample_values'][:3])
                print(f"   Exemples: {samples}")
        
        print()