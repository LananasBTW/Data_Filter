import os
import csv
import json
import config

def load(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    for row in data:
        for k, v in row.items():
            try:
                row[k] = json.loads(v.strip())
            except json.JSONDecodeError:
                row[k] = v.strip()

    return data

def save(data, filename):
    tmp_data = []
    for row in data:
        new_row = {}
        for k, v in row.items():
            # Les strings simples restent telles quelles, le reste en JSON
            if isinstance(v, str):
                new_row[k] = v
            else:
                new_row[k] = json.dumps(v)
        tmp_data.append(new_row)
        
    tmp_path = os.path.join(config.TMP_DIR, filename + ".csv")
    path = os.path.join(config.OUTPUT_DIR, filename + ".csv")

    with open(tmp_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=tmp_data[0].keys())
        writer.writeheader()
        writer.writerows(tmp_data)
        
    os.replace(tmp_path, path)
    return path