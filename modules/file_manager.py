import os
import shutil
import config
from modules.formats import fcsv, fjson, fxml, fyml

def cleanTmpDir():
    if os.path.exists(config.TMP_DIR):
        shutil.rmtree(config.TMP_DIR, ignore_errors=True)

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

    dir_path = os.path.dirname(path)
    filename = os.path.basename(path)
    name, extension = os.path.splitext(filename.lower())
    
    if dir_path:
        output_dir = os.path.join(config.OUTPUT_DIR, dir_path)
        tmp_dir = os.path.join(config.TMP_DIR, dir_path)
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(tmp_dir, exist_ok=True)
        name = os.path.join(dir_path, name)
    else:
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(config.TMP_DIR, exist_ok=True)

    match extension:
        case '.csv': fcsv.save(data, name)
        case '.json': fjson.save(data, name)
        case '.fxml': fxml.save(data, name)
        case '.fyml': fyml.save(data, name)
        case _:
            cleanTmpDir()
            raise ValueError(f"Format de fichier non supporté: {extension}")
    
    cleanTmpDir()
    return os.path.join(config.OUTPUT_DIR, filename)