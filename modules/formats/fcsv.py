import csv
import json

def convert_value(value):
    value = value.strip()

    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        pass
    return value

def load(path):    
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    for row in data:
        for k, v in row.items():
            row[k] = convert_value(v)

    return data


def save(data, path):    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
