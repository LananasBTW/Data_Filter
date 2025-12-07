import os

# On récupère le chemin du dossier actuel (api/modules)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# On remonte d'un niveau pour atteindre le dossier 'data' qui est dans 'api/data'
# Structure : api/modules/../data
DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "data")
DATA_DIR = os.path.normpath(DATA_DIR) # Nettoie le chemin (enlève le ..)

OUTPUT_DIR = os.path.join(DATA_DIR, "output")
TMP_DIR = os.path.join(DATA_DIR, "tmp")

# Crée les dossiers s'ils n'existent pas
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

TAB_PADDING = 2
STATS_MAX_SAMPLE_VALUES = 3