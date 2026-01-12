"""Entraîner et comparer les candidats modèles (Modèle v2)."""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score

# Ajouter src/ à PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

from credit_g_ml.data_loading import load_local_credit_g  # noqa: E402
from credit_g_ml.modeling import (  # noqa: E402
    build_hist_gradient_boosting_pipeline,
    build_logistic_regression_pipeline,
    build_random_forest_pipeline,
)
from credit_g_ml.preprocessing import train_test_split_credit_g  # noqa: E402


def evaluate_binary_bad(y_true, proba_bad) -> dict:
    """Calcule les métriques clés pour la classe 'bad'."""
    roc_auc = roc_auc_score((y_true == "bad").astype(int), proba_bad)

    y_pred = ["bad" if p >= 0.5 else "good" for p in proba_bad]
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=["bad"], average=None, zero_division=0
    )
    return {
        "roc_auc": float(roc_auc),
        "precision_bad": float(precision[0]),
        "recall_bad": float(recall[0]),
        "f1_bad": float(f1[0]),
    }


def save_model(pipeline, name: str) -> Path:
    path = MODELS_DIR / f"{name}_pipeline.joblib"
    joblib.dump(pipeline, path)
    return path


def main() -> None:
    df = load_local_credit_g()
    X_train, X_test, y_train, y_test = train_test_split_credit_g(df)

    candidates = [
        ("logistic_regression", build_logistic_regression_pipeline()),
        ("random_forest", build_random_forest_pipeline()),
        ("hist_gradient_boosting", build_hist_gradient_boosting_pipeline()),
    ]

    results = []
    for name, pipeline in candidates:
        pipeline.fit(X_train, y_train)

        # Probabilité de"bad"
        proba = pipeline.predict_proba(X_test)
        classes = list(pipeline.named_steps["model"].classes_)
        bad_idx = classes.index("bad")
        proba_bad = proba[:, bad_idx]

        metrics = evaluate_binary_bad(y_test, proba_bad)
        model_path = save_model(pipeline, name)

        results.append(
            {
                "model": name,
                **metrics,
                "artifact": str(model_path),
            }
        )

        print(f"[{name}] {metrics} -> {model_path}")

    # Générer le rapport Markdown
    out = REPORTS_DIR / "model_v2_comparison.md"
    lines = []
    lines.append("# Model v2 – Comparison\n\n")
    lines.append("Same split, same features, same preprocessing.\n\n")
    lines.append(
        "| Model | ROC AUC | Precision (bad) | Recall (bad) | F1 (bad) | Artifact |\n"
    )
    lines.append("|---|---:|---:|---:|---:|---|\n")

    results_sorted = sorted(results, key=lambda r: r["roc_auc"], reverse=True)
    for r in results_sorted:
        line = (
            f"| {r['model']} "
            f"| {r['roc_auc']:.3f} "
            f"| {r['precision_bad']:.3f} "
            f"| {r['recall_bad']:.3f} "
            f"| {r['f1_bad']:.3f} "
            f"| `{r['artifact']}` |\n"
        )
        lines.append(line)

    out.write_text("".join(lines), encoding="utf-8")
    print(f"Report written to: {out}")


if __name__ == "__main__":
    main()
