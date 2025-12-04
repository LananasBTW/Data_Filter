# Configuration file
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

TAB_PADDING = 2

DATA_DIR = os.path.join(CURRENT_PATH, "data/")
OUTPUT_DIR = os.path.join(DATA_DIR, "output/")
TMP_DIR = os.path.join(CURRENT_PATH, "tmp/")

STATS_MAX_SAMPLE_VALUES = 3
