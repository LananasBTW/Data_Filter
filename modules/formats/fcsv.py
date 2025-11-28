import csv


def load(path):    
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    # TODO: Convertir les types de données (tout est lu en str en CSV)
    
    return data


def save(data, path):    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
