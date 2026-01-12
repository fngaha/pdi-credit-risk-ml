"""Module de modélisation pour le projet credit_g_ml."""

from __future__ import annotations

from typing import Dict

import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

from .config import RANDOM_STATE
from .preprocessing import make_preprocessor


def build_logistic_regression_pipeline() -> Pipeline:
    """Construit un pipeline complet preprocessing + LogisticRegression."""
    preprocessor = make_preprocessor()

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",  # important pour credit-g (classes déséquilibrées)
        random_state=RANDOM_STATE,
        n_jobs=None,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    return pipeline


def build_random_forest_pipeline() -> Pipeline:
    """Construit un pipeline preprocessing + RandomForestClassifier."""
    preprocessor = make_preprocessor()

    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    return pipeline


def build_hist_gradient_boosting_pipeline() -> Pipeline:
    """Construit un pipeline preprocessing + HistGradientBoostingClassifier."""
    preprocessor = make_preprocessor()

    model = HistGradientBoostingClassifier(
        learning_rate=0.05,
        max_iter=400,
        max_depth=None,
        random_state=RANDOM_STATE,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    return pipeline


def build_hist_gradient_boosting_calibrated_pipeline() -> Pipeline:
    """Pipeline HGB + calibration pour obtenir des probabilités plus fiables."""
    preprocessor = make_preprocessor()

    base_model = HistGradientBoostingClassifier(
        learning_rate=0.05,
        max_iter=400,
        max_depth=None,
        random_state=RANDOM_STATE,
    )

    # Calibration sigmoid = généralement plus robuste sur petits datasets
    calibrated = CalibratedClassifierCV(
        estimator=base_model,
        method="sigmoid",
        cv=5,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", calibrated),
        ]
    )


def train_and_evaluate(
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Dict[str, float]:
    """Entraîne le pipeline et retourne les métriques principales."""
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    print("=== Classification report ===")
    print(classification_report(y_test, y_pred))

    print("=== Confusion matrix ===")
    print(confusion_matrix(y_test, y_pred))

    print("=== ROC AUC ===")
    print(metrics["roc_auc"])

    return metrics
