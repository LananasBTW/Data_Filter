import config

def type_is_number(type: str):
    return type in {"int", "float"}

def get_type_str(value):
    """Retourne le type sous forme de string lisible (int, str, list, etc.)"""
    if isinstance(value, bool): return "bool"
    if isinstance(value, int): return "int"
    if isinstance(value, float): return "float"
    if isinstance(value, str): return "str"
    if isinstance(value, list): return "list"
    if isinstance(value, dict): return "dict"
    if value is None: return "None"
    return "unknown"

def get_all_fields(data):
    """Récupère la liste triée de toutes les clés uniques présentes dans les données."""
    if not data: return []
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())
    return sorted(list(all_keys))

def get_column_types(data):
    """
    Détermine les types de données pour chaque colonne dans les données fournies.
    Retourne un dictionnaire où les clés sont les noms des colonnes et les valeurs sont des chaînes décrivant les types.
    """
    columns = get_all_fields(data)
    column_types = {}
    for col in columns:
        # Collecter tous les types uniques trouvés dans cette colonne
        base_types = set()
        list_content_types = set()
        
        for row in data:
            if col in row and row[col] is not None:
                type_str = get_type_str(row[col])
                if type_str == "list" and isinstance(row[col], list):
                    base_types.add("list")
                    # Collecter tous les types d'éléments dans la liste
                    for item in row[col]:
                        list_content_types.add(get_type_str(item))
                else:
                    base_types.add(type_str)
            column_types[col] = {
                "base": base_types,
                "sub": list_content_types
            }
    return column_types