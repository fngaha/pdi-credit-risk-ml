"""Métadonnées du dataset credit-g (valeurs catégorielles autorisées)."""

from __future__ import annotations

from typing import Dict, List

from .data_loading import load_local_credit_g
from .schemas import CATEGORICAL_FEATURES


def get_categorical_values() -> Dict[str, List[str]]:
    """Retourne les valeurs uniques par feature catégorielle.

    Utilisé pour alimenter les listes déroulantes de l'UI.
    """
    df = load_local_credit_g()

    values: Dict[str, List[str]] = {}
    for col in CATEGORICAL_FEATURES:
        values[col] = sorted(df[col].dropna().unique().tolist())

    return values
