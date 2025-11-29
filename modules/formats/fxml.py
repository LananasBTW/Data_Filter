import os
import xml.etree.ElementTree as ET
import json
import config

def load(path):
    """
    Charge un fichier XML et retourne une liste de dictionnaires.
    
    Args:
        path: Chemin vers le fichier XML
        
    Returns:
        list: Liste de dictionnaires représentant les données
    """
    tree = ET.parse(path)
    root = tree.getroot()
    
    data = []
    
    # Parcourir tous les éléments enfants de la racine
    for item in root:
        row = {}
        for child in item:
            # Récupérer le texte de l'élément
            text = child.text if child.text else ""
            
            # Essayer de parser comme JSON pour les types complexes (listes, booléens, etc.)
            try:
                value = json.loads(text)
            except (json.JSONDecodeError, ValueError):
                # Si ce n'est pas du JSON valide, traiter comme une chaîne
                value = text
            
            row[child.tag] = value
        
        data.append(row)
    
    return data


def save(data, filename):
    """
    Sauvegarde une liste de dictionnaires dans un fichier XML.
    
    Args:
        data: Liste de dictionnaires à sauvegarder
        filename: Nom du fichier (sans extension)
        
    Returns:
        str: Chemin du fichier sauvegardé
    """
    # Créer l'élément racine
    root = ET.Element("data")
    
    # Pour chaque dictionnaire dans les données
    for row in data:
        # Créer un élément "item" pour chaque ligne
        item = ET.SubElement(root, "item")
        
        # Pour chaque clé-valeur dans le dictionnaire
        for key, value in row.items():
            # Créer un sous-élément avec le nom de la clé
            field = ET.SubElement(item, str(key))
            
            # Convertir la valeur en chaîne
            # Pour les types complexes (listes, dicts, booléens), utiliser JSON
            if isinstance(value, (list, dict, bool)) or value is None:
                field.text = json.dumps(value)
            else:
                field.text = str(value)
    
    # Créer l'arbre XML
    tree = ET.ElementTree(root)
    
    # Chemins pour le fichier temporaire et final
    tmp_path = os.path.join(config.TMP_DIR, filename + ".fxml")
    path = os.path.join(config.OUTPUT_DIR, filename + ".fxml")
    
    # Écrire dans le fichier temporaire
    tree.write(tmp_path, encoding='utf-8', xml_declaration=True)
    
    # Déplacer vers le répertoire de sortie
    os.replace(tmp_path, path)
    
    return path
