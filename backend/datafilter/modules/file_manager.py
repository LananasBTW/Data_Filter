import os
import shutil
# Import relatif car config est dans le même dossier
from . import config
# Import relatif pour aller chercher dans le sous-dossier formats
from .formats import fcsv, fjson, fxml, fyml

def cleanTmpDir():
    if os.path.exists(config.TMP_DIR):
        shutil.rmtree(config.TMP_DIR, ignore_errors=True)

def load_data(path):
    if not path:
        raise ValueError("Path cannot be empty")
    
    # Si le chemin est relatif (ex: "data/students.csv"), on le colle au DATA_DIR
    # Cela permet de trouver le fichier même si on lance le script depuis ailleurs
    if not os.path.isabs(path) and not os.path.exists(path):
        potential_path = os.path.join(config.DATA_DIR, os.path.basename(path))
        if os.path.exists(potential_path):
            path = potential_path

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
    
    # Nettoyage et préparation du chemin de sortie
    filename = os.path.basename(path)
    name, extension = os.path.splitext(filename.lower())
    
    # On sauvegarde toujours dans le dossier output défini dans config
    # pour éviter de mettre le bazar partout
    output_path = os.path.join(config.OUTPUT_DIR, filename)
    
    match extension:
        case '.csv': return fcsv.save(data, name)
        case '.json': return fjson.save(data, name)
        case '.fxml': return fxml.save(data, name)
        case '.fyml': return fyml.save(data, name)
        case _:
            raise ValueError(f"Format de fichier non supporté: {extension}")