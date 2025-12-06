import os
import json
from .. import config

def load(path):    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(data, filename, indent=4):
    base_name = os.path.basename(filename)
    if not base_name.endswith('.json'): base_name += '.json'
    
    path = os.path.join(config.OUTPUT_DIR, base_name)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)

    return path