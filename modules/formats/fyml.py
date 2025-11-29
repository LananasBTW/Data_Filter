import os
import json
import config

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def _convert_value_to_yaml_compatible(value):
    """
    Convertit une valeur Python en format compatible YAML.
    """
    if isinstance(value, bool):
        return value
    elif isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        return value
    elif isinstance(value, list):
        return [_convert_value_to_yaml_compatible(item) for item in value]
    elif isinstance(value, dict):
        return {k: _convert_value_to_yaml_compatible(v) for k, v in value.items()}
    elif value is None:
        return None
    else:
        return str(value)


def _parse_yaml_value(value):
    """
    Parse une valeur YAML en valeur Python.
    """
    if isinstance(value, (bool, int, float, list, dict)) or value is None:
        return value
    elif isinstance(value, str):
        # Essayer de parser comme JSON pour les types complexes
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value
    else:
        return value


def load(path):
    """
    Charge un fichier YAML et retourne une liste de dictionnaires.
    
    Args:
        path: Chemin vers le fichier YAML
        
    Returns:
        list: Liste de dictionnaires représentant les données
    """
    if not YAML_AVAILABLE:
        raise ImportError(
            "Le module 'pyyaml' n'est pas installé. "
            "Installez-le avec: pip install pyyaml"
        )
    
    with open(path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    
    # Si les données sont une liste, les retourner directement
    if isinstance(yaml_data, list):
        # Parser chaque élément
        data = []
        for item in yaml_data:
            if isinstance(item, dict):
                parsed_item = {}
                for key, value in item.items():
                    parsed_item[key] = _parse_yaml_value(value)
                data.append(parsed_item)
            else:
                data.append(item)
        return data
    
    # Si c'est un dictionnaire unique, le mettre dans une liste
    elif isinstance(yaml_data, dict):
        parsed_item = {}
        for key, value in yaml_data.items():
            parsed_item[key] = _parse_yaml_value(value)
        return [parsed_item]
    
    # Sinon, retourner une liste vide ou avec la valeur
    return yaml_data if isinstance(yaml_data, list) else [yaml_data]


def save(data, filename):
    """
    Sauvegarde une liste de dictionnaires dans un fichier YAML.
    
    Args:
        data: Liste de dictionnaires à sauvegarder
        filename: Nom du fichier (sans extension)
        
    Returns:
        str: Chemin du fichier sauvegardé
    """
    if not YAML_AVAILABLE:
        raise ImportError(
            "Le module 'pyyaml' n'est pas installé. "
            "Installez-le avec: pip install pyyaml"
        )
    
    # Convertir les données en format compatible YAML
    yaml_data = []
    for row in data:
        yaml_row = {}
        for key, value in row.items():
            yaml_row[key] = _convert_value_to_yaml_compatible(value)
        yaml_data.append(yaml_row)
    
    # Chemins pour le fichier temporaire et final
    tmp_path = os.path.join(config.TMP_DIR, filename + ".fyml")
    path = os.path.join(config.OUTPUT_DIR, filename + ".fyml")
    
    # Écrire dans le fichier temporaire
    with open(tmp_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Déplacer vers le répertoire de sortie
    os.replace(tmp_path, path)
    
    return path
