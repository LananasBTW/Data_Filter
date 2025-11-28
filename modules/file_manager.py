import os
from modules.formats import fcsv, fjson, fxml, fyml


def load_data(path):
    if not path:
        raise ValueError("Path cannot be empty")
    
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
    
    name, extension = os.path.splitext(path.lower())

    match extension:
        case '.csv': return fcsv.load(path)
        case '.json': return fjson.load(path)
        case '.fxml': return fxml.load(path)
        case '.fyml': return fyml.load(path)
        case _: raise ValueError(f"Format de fichier non supporté: {extension}")


def save_data(data, path):
    if not path:
        raise ValueError("Path cannot be empty")
    
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    if not data:
        raise ValueError("No data to save")
    
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Data must be a list of dictionaries")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    name, extension = os.path.splitext(path.lower())

    match extension:
        case '.csv': fcsv.save(data, path)
        case '.json': fjson.save(data, path)
        case '.fxml': fxml.save(data, path)
        case '.fyml': fyml.save(data, path)
        case _: raise ValueError(f"Format de fichier non supporté: {extension}")
