"""Module de chargement des données pour le projet credit_g_ml.

Ce module fournit une fonction pour charger le dataset credit-g via OpenML.
"""

from pathlib import Path

import openml
import pandas as pd

from .config import RAW_DATA_DIR, TARGET_COL

DATASET_NAME = "credit-g"
DATASET_ID = 31  # pour info, mais on utilise surtout le nom


def fetch_credit_g_dataframe() -> pd.DataFrame:
    """Télécharge le dataset credit-g depuis OpenML et retourne un DataFrame complet.

    On fusionne X et y dans un seul DataFrame, avec la colonne cible TARGET_COL.
    """
    dataset = openml.datasets.get_dataset(DATASET_NAME)
    X, y, _, _ = dataset.get_data(
        dataset_format="dataframe",
        target=dataset.default_target_attribute,
    )

    df = X.copy()
    df[TARGET_COL] = y

    return df


def save_raw_credit_g(filename: str = "credit_g_raw.csv") -> Path:
    """Télécharge le dataset credit-g et le sauvegarde dans data/raw/ en CSV.

    Retourne le chemin du fichier sauvegardé.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = fetch_credit_g_dataframe()
    output_path = RAW_DATA_DIR / filename
    df.to_csv(output_path, index=False)

    return output_path


def load_local_credit_g(filename: str = "credit_g_raw.csv") -> pd.DataFrame:
    """Charge le dataset credit-g sauvegardé en local dans data/raw/."""
    csv_path = RAW_DATA_DIR / filename
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Le fichier {csv_path} n'existe pas. "
            "Lance d'abord save_raw_credit_g() pour le télécharger."
        )
    return pd.read_csv(csv_path)


if __name__ == "__main__":
    path = save_raw_credit_g()
    print(f"Dataset credit-g sauvegardé dans : {path}")
