"""Module (pipeline) de préprocessing pour le projet credit_g_ml."""

from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import RANDOM_STATE, TARGET_COL
from .schemas import ALL_FEATURES, CATEGORICAL_FEATURES, NUMERIC_FEATURES


def split_features_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Sépare le DataFrame en X (features) et y (cible).

    On sélectionne explicitement les colonnes définies dans ALL_FEATURES.
    """
    missing_cols = [col for col in ALL_FEATURES + [TARGET_COL] if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colonnes manquantes dans le DataFrame: {missing_cols}")

    X = df[ALL_FEATURES].copy()
    y = df[TARGET_COL].copy()
    return X, y


def make_preprocessor() -> ColumnTransformer:
    """Construit le ColumnTransformer pour le préprocessing.

    - Numériques: imputation médiane + standardisation
    - Catégorielles: imputation valeur la plus fréquente + OneHotEncoder
    """
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore"),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    return preprocessor


def train_test_split_credit_g(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = RANDOM_STATE,
    stratify: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Effectue un split train/test sur le dataset credit-g.

    On propose par défaut un split stratifié sur la cible.
    """
    X, y = split_features_target(df)

    stratify_param = y if stratify else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_param,
    )

    return X_train, X_test, y_train, y_test
