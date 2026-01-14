"""
Génère un graphique d'importance des variables (coefficients)
pour une Logistic Regression.

Hypothèses :
- Le modèle est un Pipeline scikit-learn avec les steps :
  ("preprocessor", ...) puis ("model", LogisticRegression).
- Le preprocessor est un ColumnTransformer utilisant un
  OneHotEncoder et éventuellement un StandardScaler.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "logistic_regression_pipeline.joblib"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUT_PNG = REPORTS_DIR / "feature_importance_logreg_top20.png"
OUT_CSV = REPORTS_DIR / "feature_importance_logreg_top20.csv"


def _get_feature_names_from_preprocessor(preprocessor) -> list[str]:
    """Récupère les noms de features après transformation (incluant one-hot)."""
    # scikit-learn >= 1.0 fournit get_feature_names_out() sur ColumnTransformer
    try:
        names = preprocessor.get_feature_names_out()
        return [str(n) for n in names]
    except Exception:
        pass

    # Fallback : tentative de reconstruction manuelle (moins robuste)
    feature_names: list[str] = []
    for name, transformer, cols in getattr(preprocessor, "transformers_", []):
        if name == "remainder" and transformer == "drop":
            continue

        if hasattr(transformer, "get_feature_names_out"):
            try:
                # OneHotEncoder retourne des noms enrichis
                fn = transformer.get_feature_names_out(cols)
                feature_names.extend([str(x) for x in fn])
                continue
            except Exception:
                pass

        # Sinon : on retombe sur les colonnes brutes
        if isinstance(cols, (list, tuple, np.ndarray)):
            feature_names.extend([str(c) for c in cols])
        else:
            feature_names.append(str(cols))

    return feature_names


def main(top_n: int = 20) -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modèle introuvable: {MODEL_PATH}. Lance d'abord scripts/train_model.py."
        )

    pipeline = joblib.load(MODEL_PATH)

    if "preprocessor" not in pipeline.named_steps:
        raise KeyError("Step 'preprocessor' introuvable dans le pipeline.")
    if "model" not in pipeline.named_steps:
        raise KeyError("Step 'model' introuvable dans le pipeline.")

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    if not hasattr(model, "coef_"):
        raise TypeError("Le modèle ne fournit pas coef_ (attendu: LogisticRegression).")

    feature_names = _get_feature_names_from_preprocessor(preprocessor)
    coefs = model.coef_

    # Cas binaire => shape (1, n_features)
    if coefs.ndim == 2 and coefs.shape[0] == 1:
        coefs = coefs[0]

    if len(feature_names) != len(coefs):
        raise ValueError(
            f"Incohérence: {len(feature_names)=} vs {len(coefs)=}. "
            "Vérifie le preprocessor et/ou la version scikit-learn."
        )

    df = pd.DataFrame(
        {
            "feature": feature_names,
            "coef": coefs,
            "importance_abs": np.abs(coefs),
            "direction": np.where(coefs >= 0, "↑ risque (bad)", "↓ risque (bad)"),
        }
    ).sort_values("importance_abs", ascending=False)

    df_top = df.head(top_n).copy()

    # Export CSV
    df_top.to_csv(OUT_CSV, index=False)

    # Graphique
    plt.figure(figsize=(10, 6))
    y = np.arange(len(df_top))[::-1]
    plt.barh(y, df_top["importance_abs"][::-1])
    plt.yticks(y, df_top["feature"][::-1])
    plt.xlabel("Importance (|coefficient|)")
    plt.title(f"Logistic Regression – Top {top_n} Feature Importance (|coef|)")
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200)
    plt.close()

    print(f" CSV: {OUT_CSV}")
    print(f" PNG: {OUT_PNG}")


if __name__ == "__main__":
    main(top_n=20)
