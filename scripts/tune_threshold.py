"""Recherche d'un seuil de décision optimisé selon un coût métier.

Objectif :
- Minimiser un coût simple basé sur la matrice de confusion
- FN (bad prédit good) est plus coûteux que FP (good prédit bad)

Par défaut (Option 1) :
- coût_FN = 5
- coût_FP = 1
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix

# Ajout de src au PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from credit_g_ml.data_loading import load_local_credit_g  # noqa: E402
from credit_g_ml.modeling import (  # noqa: E402
    build_hist_gradient_boosting_calibrated_pipeline,
)
from credit_g_ml.preprocessing import train_test_split_credit_g  # noqa: E402


def predict_proba_bad(pipeline, X_test) -> np.ndarray:
    """Retourne P(bad) sur le jeu de test."""
    proba = pipeline.predict_proba(X_test)
    # On récupère l'index de la classe "bad"
    classes = list(pipeline.named_steps["model"].classes_)
    bad_idx = classes.index("bad")
    return proba[:, bad_idx]


def compute_cost(y_true, y_pred, cost_fn: int, cost_fp: int) -> dict:
    """Calcule le coût et renvoie FN/FP/TN/TP pour un reporting."""
    # Ordre des labels : ["bad", "good"]
    cm = confusion_matrix(y_true, y_pred, labels=["bad", "good"])
    tn = int(cm[0, 0])  # bad -> bad (bien détecté) = "vrai bad"
    fp = int(cm[0, 1])  # bad -> good (erreur) = FN au sens "bad raté"
    fn = int(cm[1, 0])  # good -> bad (erreur) = FP au sens "bon client rejeté"
    tp = int(cm[1, 1])  # good -> good

    # Attention : confusion_matrix avec labels ["bad","good"] :
    # ligne = vrai, colonne = prédit
    # - vrai bad prédit good = FN métier
    fn_business = fp
    # - vrai good prédit bad = FP métier
    fp_business = fn

    cost = cost_fn * fn_business + cost_fp * fp_business
    return {
        "tn_bad": tn,
        "tp_good": tp,
        "fn_bad_pred_good": fn_business,
        "fp_good_pred_bad": fp_business,
        "cost": int(cost),
    }


def main() -> None:
    # Coûts métier (Option 1)
    cost_fn = 5  # bad prédit good (grave)
    cost_fp = 1  # good prédit bad (moins grave)

    # Choix du modèle candidat pour v3 : calibré ou non calibré
    # Recommandation : calibré (probabilités plus fiables)
    pipeline = build_hist_gradient_boosting_calibrated_pipeline()

    df = load_local_credit_g()
    X_train, X_test, y_train, y_test = train_test_split_credit_g(df)

    pipeline.fit(X_train, y_train)
    proba_bad = predict_proba_bad(pipeline, X_test)

    thresholds = np.linspace(0.05, 0.95, 19)
    rows = []

    for t in thresholds:
        y_pred = np.where(proba_bad >= t, "bad", "good")
        stats = compute_cost(y_test, y_pred, cost_fn=cost_fn, cost_fp=cost_fp)
        rows.append({"threshold": float(t), **stats})

    best = min(rows, key=lambda r: r["cost"])

    # Écriture d'un mini rapport
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out = reports_dir / "model_v3_threshold.md"

    lines = []
    lines.append("# Model v3 – Seuil métier (cost-based)\n\n")
    lines.append("## Hypothèses de coût\n")
    lines.append(f"- Coût FN (bad prédit good) : **{cost_fn}**\n")
    lines.append(f"- Coût FP (good prédit bad) : **{cost_fp}**\n\n")
    lines.append("## Résultat\n")
    lines.append(
        f'- Seuil optimal : **{best["threshold"]:.2f}** '
        f'(coût total = **{best["cost"]}**)\n\n'
    )
    lines.append("## Détails au seuil optimal\n")
    lines.append(f'- FN (bad → good) : **{best["fn_bad_pred_good"]}**\n')
    lines.append(f'- FP (good → bad) : **{best["fp_good_pred_bad"]}**\n')
    lines.append(f'- TN (bad → bad) : **{best["tn_bad"]}**\n')
    lines.append(f'- TP (good → good) : **{best["tp_good"]}**\n\n')

    lines.append("## Tableau (grille de seuils)\n\n")
    lines.append("| Seuil | Coût | FN (bad→good) | FP (good→bad) |\n")
    lines.append("|---:|---:|---:|---:|\n")
    for r in rows:
        line = (
            f"| {r['threshold']:.2f} "
            f"| {r['cost']} "
            f"| {r['fn_bad_pred_good']} "
            f"| {r['fp_good_pred_bad']} |\n"
        )
        lines.append(line)

    out.write_text("".join(lines), encoding="utf-8")
    print(f"Rapport écrit dans : {out}")
    print(f"Seuil optimal: {best['threshold']:.2f} | coût={best['cost']}")


if __name__ == "__main__":
    main()
