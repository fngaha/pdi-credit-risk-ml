"""Tests pour le module preprocessing."""

from __future__ import annotations

import pandas as pd

from credit_g_ml.config import TARGET_COL
from credit_g_ml.preprocessing import make_preprocessor, split_features_target
from credit_g_ml.schemas import ALL_FEATURES


def _make_dummy_dataframe() -> pd.DataFrame:
    """Crée un petit DataFrame factice avec la bonne structure."""
    data = {
        # Numériques
        "duration": [6, 24, 12],
        "credit_amount": [1000, 5000, 2500],
        "installment_commitment": [2, 3, 4],
        "residence_since": [2, 4, 3],
        "age": [25, 45, 33],
        "existing_credits": [1, 2, 1],
        "num_dependents": [1, 1, 2],
        # Catégorielles
        "checking_status": ["<0", "0<=X<200", "no checking"],
        "credit_history": [
            "no credits/all paid",
            "existing paid",
            "delayed previously",
        ],
        "purpose": ["radio/tv", "car (new)", "education"],
        "savings_status": ["<100", "500<=X<1000", "unknown"],
        "employment": ["1<=X<4", "4<=X<7", ">=7"],
        "personal_status": ["male single", "female div/dep", "male mar/wid"],
        "other_parties": ["none", "guarantor", "none"],
        "property_magnitude": ["real estate", "car", "life insurance"],
        "other_payment_plans": ["none", "bank", "stores"],
        "housing": ["own", "rent", "for free"],
        "job": ["skilled", "unskilled resident", "high qualif/self emp/mgmt"],
        "own_telephone": ["yes", "none", "yes"],
        "foreign_worker": ["yes", "yes", "no"],
        # Cible
        TARGET_COL: ["good", "bad", "good"],
    }

    df = pd.DataFrame(data)
    # Vérification rapide que les listes de features sont cohérentes
    assert set(ALL_FEATURES).issubset(df.columns)
    assert TARGET_COL in df.columns
    return df


def test_split_features_target_shapes() -> None:
    df = _make_dummy_dataframe()
    X, y = split_features_target(df)

    assert list(X.columns) == ALL_FEATURES
    assert y.name == TARGET_COL
    assert len(X) == len(y) == len(df)


def test_make_preprocessor_fit_transform() -> None:
    df = _make_dummy_dataframe()
    X, _ = split_features_target(df)

    preprocessor = make_preprocessor()
    X_processed = preprocessor.fit_transform(X)

    # On doit conserver le bon nombre de lignes
    assert X_processed.shape[0] == X.shape[0]
