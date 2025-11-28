import os
import csv
import json
import config

def convert_strToValue(value):
    value = value.strip()
    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        pass
    return value

def convert_valueToStr(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    return str(value)

def load(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    for row in data:
        for k, v in row.items():
            row[k] = convert_strToValue(v)

    return data

def save(data, filename):
    tmp_data = data.copy()
    for row in tmp_data:
        for k, v in row.items():
            row[k] = convert_valueToStr(v)
        
    tmp_path = os.path.join(config.TMP_DIR, filename + ".csv")
    path = os.path.join(config.OUTPUT_DIR, filename + ".csv")

    with open(tmp_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=tmp_data[0].keys())
        writer.writeheader()
        writer.writerows(tmp_data)
        
    os.replace(tmp_path, path)
    return path