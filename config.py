# config.py

import os

# Data folder for preprocessed file
DATA_FOLDER = "data"
PREPROCESSED_FILE = os.path.join(DATA_FOLDER, "preprocessed_data.csv")

# Report CSV at root level
REPORT_FILE = "report.csv"

# Folder to save cup & handle pattern images
PATTERNS_DIR = "patterns"

# Directory for logs
LOG_DIR = os.path.join(os.getcwd(), "log_info")
os.makedirs(LOG_DIR, exist_ok=True)

# Ensure required folders exist
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(PATTERNS_DIR, exist_ok=True)
