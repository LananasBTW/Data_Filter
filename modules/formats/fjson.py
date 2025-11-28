import json


def load(path):
    if not path:
        raise ValueError("Path cannot be empty")
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    with open(path, 'r') as f:
        return json.load(f)


def save(data, path, indent=4):
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)