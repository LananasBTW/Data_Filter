import json


def load(path):    
    with open(path, 'r') as f:
        return json.load(f)


def save(data, path, indent=4):
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)