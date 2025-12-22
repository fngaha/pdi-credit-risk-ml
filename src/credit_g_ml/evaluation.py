"""Module d'évaluation pour le projet credit_g_ml.

Fonctions d'évaluation et de visualisation des performances.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import RocCurveDisplay
from sklearn.pipeline import Pipeline


def plot_roc_curve(
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    output_path: Path | None = None,
) -> None:
    RocCurveDisplay.from_estimator(pipeline, X_test, y_test)
    plt.title("ROC Curve - Credit Risk Model")

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches="tight")

    plt.show()
