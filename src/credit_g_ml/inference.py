"""Module d'inférence pour le projet credit_g_ml.

Chargement du modèle et prédiction unitaire.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from .config import MODELS_DIR
from .schemas import ALL_FEATURES

DEFAULT_MODEL_PATH = MODELS_DIR / "logistic_regression_pipeline.joblib"


@dataclass(frozen=True)
class PredictionResult:
    label: str
    probability_bad: float
    probability_good: float


def load_model(model_path: Path = DEFAULT_MODEL_PATH) -> Pipeline:
    """Charge le pipeline scikit-learn sauvegardé (préprocessing + modèle)."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"Modèle introuvable: {model_path}. "
            "Lance d'abord scripts/train_model.py."
        )
    model = joblib.load(model_path)
    if not isinstance(model, Pipeline):
        raise TypeError("Le modèle chargé n'est pas un Pipeline scikit-learn.")
    return model


def _to_single_row_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
    """Convertit un payload dict en DataFrame 1 ligne, dans l'ordre des features."""
    missing = [c for c in ALL_FEATURES if c not in payload]
    if missing:
        raise ValueError(f"Features manquantes: {missing}")

    # On ne garde que les colonnes attendues (ignore champs en trop)
    row = {c: payload[c] for c in ALL_FEATURES}
    return pd.DataFrame([row], columns=ALL_FEATURES)


def predict_single(pipeline: Pipeline, payload: Dict[str, Any]) -> PredictionResult:
    """Prédit sur une observation (dict)."""
    X = _to_single_row_dataframe(payload)

    proba = pipeline.predict_proba(X)[0]  # [p(class0), p(class1)] selon sklearn
    classes = list(pipeline.named_steps["model"].classes_)

    # On veut sortir explicitement p(bad) et p(good) même si l'ordre est inversé
    proba_map = dict(zip(classes, proba, strict=False))
    p_bad = float(proba_map.get("bad", 0.0))
    p_good = float(proba_map.get("good", 0.0))

    # Décision label selon predict (seuil du modèle)
    label = str(pipeline.predict(X)[0])

    return PredictionResult(label=label, probability_bad=p_bad, probability_good=p_good)
