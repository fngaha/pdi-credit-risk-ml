# pdi-credit-risk-ml

Projet de fin de formation – Développeur orienté IA
Score de risque crédit basé sur le dataset **credit-g** (OpenML), développé selon la méthodologie **CRISP-DM**.

## Objectifs

- Explorer et préparer les données (EDA).
- Entraîner un modèle de machine learning pour prédire le risque de défaut.
- Exposer le modèle via une **API Flask**.
- Proposer une **interface web simple** pour scorer un client.
- Mettre en place des bonnes pratiques :
  - formatage avec **black**,
  - linting avec **ruff**,
  - hooks **pre-commit**,
  - tests automatisés avec **pytest**.

## Structure du projet

(à compléter au fur et à mesure)

## Résultats – Baseline

Le modèle baseline (Logistic Regression) atteint :

- ROC AUC ≈ 0.78
- Bon rappel sur la classe "bad" (objectif métier)

Voir :
- `reports/baseline_logistic_regression.md`
- `reports/roc_curve_logistic_regression.png`
