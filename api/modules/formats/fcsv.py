import os
import csv
import json

from .. import config 

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    for row in data:
        for k, v in row.items():
            try:
                if v: row[k] = json.loads(v.strip())
            except (json.JSONDecodeError, TypeError):
                row[k] = v.strip() if v else ""
    return data

def save(data, filename):
    all_fields = set()
    for row in data: all_fields.update(row.keys())
    all_fields = sorted(all_fields)
    
    tmp_data = []
    for row in data:
        new_row = {}
        for field in all_fields:
            v = row.get(field)
            if isinstance(v, str): new_row[field] = v
            else: new_row[field] = json.dumps(v)
        tmp_data.append(new_row)
        
    # Utilisation des chemins depuis config
    # Attention: filename peut être un chemin complet ou juste un nom
    # on s'assure d'avoir juste le nom pour le fichier final
    base_name = os.path.basename(filename)
    if not base_name.endswith('.csv'): base_name += '.csv'

    path = os.path.join(config.OUTPUT_DIR, base_name)
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(tmp_data)
        
    return path