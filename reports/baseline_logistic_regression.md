# Évaluation – Baseline Logistic Regression

## Contexte
- Projet : PDI – Credit Risk Scoring
- Dataset : **credit-g** (OpenML)
- Méthodologie : **CRISP-DM**
- Phase : Modeling & Evaluation
- Modèle : Logistic Regression
- Gestion du déséquilibre : `class_weight="balanced"`

---

## Configuration expérimentale

- Split train / test : **80% / 20%**
- Stratification : **oui**
- Random state : **42**
- Préprocessing :
  - Numérique : imputation médiane + standardisation
  - Catégoriel : imputation la plus fréquente + OneHotEncoding
- Pipeline scikit-learn unique (préprocessing + modèle)

---

## Métriques principales (jeu de test)

- **ROC AUC** : **0.76**

Cette valeur indique une bonne capacité de discrimination globale entre les classes *good* et *bad*, pour un modèle linéaire sans tuning avancé.

---

## Classification Report

| Classe | Precision | Recall | F1-score | Support |
|------|-----------|--------|----------|---------|
| bad  | 0.47 | 0.70 | 0.56 | 60 |
| good | 0.84 | 0.66 | 0.74 | 140 |
| **Accuracy globale** |  |  | **0.68** | 200 |

- **Recall (bad) = 0.70** :
  → 70% des mauvais payeurs sont correctement identifiés.
- **Precision (bad) = 0.47** :
  → Le modèle accepte un certain nombre de faux positifs, ce qui est cohérent dans un contexte de **gestion du risque**.

---

## Confusion Matrix

[[42 18]

[47 93]]


Interprétation :

- **True Negatives (bad correctement détectés)** : 42
- **False Positives (bons clients refusés)** : 18
- **False Negatives (mauvais clients acceptés)** : 47
- **True Positives (bons clients acceptés)** : 93

---

## Analyse métier

- Le modèle privilégie la **détection des profils à risque**, ce qui est cohérent avec un cas d’usage crédit.
- Le rappel élevé sur la classe *bad* réduit le risque d’octroi à des clients insolvables.
- Le compromis précision / rappel est acceptable pour un **baseline**, sans optimisation fine.

---

## Limites du modèle

- Modèle linéaire (relations non linéaires non capturées)
- Pas de tuning d’hyperparamètres
- Seuil de décision par défaut (0.5)
- Pas de calibration probabiliste

---

## Prochaines améliorations envisagées

- Ajustement du seuil de décision selon un objectif métier
- Modèles non linéaires (RandomForest, Gradient Boosting)
- Analyse approfondie des features importantes
- Calibration des probabilités
- Comparaison systématique des modèles

---

## Artefacts générés

- Modèle entraîné :
  `models/logistic_regression_pipeline.joblib` *(non versionné)*
- Courbe ROC :
  `reports/roc_curve_logistic_regression.png`
