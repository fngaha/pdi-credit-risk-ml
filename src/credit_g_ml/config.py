import os
from pathlib import Path

# Répertoire racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

RANDOM_STATE = 42
TARGET_COL = "class"

# Nom du modèle à charger en production
MODEL_NAME = os.getenv("MODEL_NAME", "logistic_regression")

# Seuils de décision (API + démos)
THRESHOLD_BAD = float(os.getenv("THRESHOLD_BAD", "0.50"))
THRESHOLD_ACCEPT = float(os.getenv("THRESHOLD_ACCEPT", "0.15"))
THRESHOLD_REJECT = float(os.getenv("THRESHOLD_REJECT", "0.35"))
