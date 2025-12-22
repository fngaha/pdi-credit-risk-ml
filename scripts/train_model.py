"""Script d'entraînement du modèle credit risk."""

import sys
from pathlib import Path

import joblib

# Ajout de src au PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

REPORTS_DIR = PROJECT_ROOT / "reports"
roc_path = REPORTS_DIR / "roc_curve_logistic_regression.png"

from credit_g_ml.config import MODELS_DIR  # noqa: E402
from credit_g_ml.data_loading import load_local_credit_g  # noqa: E402
from credit_g_ml.evaluation import plot_roc_curve  # noqa: E402
from credit_g_ml.modeling import (  # noqa: E402
    build_logistic_regression_pipeline,
    train_and_evaluate,
)
from credit_g_ml.preprocessing import train_test_split_credit_g  # noqa: E402


def main() -> None:
    df = load_local_credit_g()

    X_train, X_test, y_train, y_test = train_test_split_credit_g(df)

    pipeline = build_logistic_regression_pipeline()
    metrics = train_and_evaluate(
        pipeline,
        X_train,
        y_train,
        X_test,
        y_test,
    )

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / "logistic_regression_pipeline.joblib"
    joblib.dump(pipeline, model_path)

    print(f"Modèle sauvegardé dans : {model_path}")
    print(f"Métriques finales : {metrics}")

    plot_roc_curve(pipeline, X_test, y_test, output_path=roc_path)


if __name__ == "__main__":
    main()
