"""Script utilitaire pour télécharger et sauvegarder le dataset credit-g."""

import sys
from pathlib import Path

# Ajoute le dossier src au PYTHONPATH pour pouvoir importer credit_g_ml
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from credit_g_ml.data_loading import save_raw_credit_g  # type: ignore  # noqa: E402


def main() -> None:
    path = save_raw_credit_g()
    print(f"Dataset credit-g téléchargé et sauvegardé dans: {path}")


if __name__ == "__main__":
    main()
