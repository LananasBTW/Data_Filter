import os
import json
import config

def load(path):    
    with open(path, 'r') as f:
        return json.load(f)

def save(data, filename, indent=4):
    tmp_path = os.path.join(config.TMP_DIR, filename + ".json")
    path = os.path.join(config.OUTPUT_DIR, filename + ".json")

    with open(tmp_path, 'w') as f:
        json.dump(data, f, indent=indent)

    os.replace(tmp_path, path)
    return path