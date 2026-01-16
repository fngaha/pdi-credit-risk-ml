# Credit Risk Scoring — Business Decision Thresholds (PDI)

![Deploy to Cloud Run](https://github.com/fngaha/pdi-credit-risk-ml/actions/workflows/deploy-cloudrun.yml/badge.svg)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://pdi-credit-risk-ml-mbn4mquhua-ew.a.run.app)

---

## TL;DR

- **But** : prédire **P(bad)** (risque de défaut) et convertir ce score en décision **ACCEPT / REVIEW / REJECT** via seuils métier.
- **Stack** : Python • scikit-learn • **Flask API** + **UI** • Docker • Cloud Run • CI/CD GitHub Actions (WIF).
- **Démarrage rapide** : `make run` puis ouvre `http://127.0.0.1:5001`
- **Test** : `make smoke`
- **Démo** : `/demo/full/low` → ACCEPT • `/demo/full/medium` → REVIEW • `/demo/full/high` → REJECT

---
**FR / EN** — Projet de fin de formation (Développeur orienté IA)

Dataset : **credit-g** (OpenML) • Méthodo : **CRISP-DM** • Déploiement : **Google Cloud Run** (CI/CD GitHub Actions, keyless via **WIF**)

## 🇫🇷 Résumé (FR)

Ce projet met en œuvre un système de **scoring de risque crédit** : un modèle ML prédit **P(bad)**, puis une couche métier transforme cette probabilité en **décision exploitable (ACCEPT / REVIEW / REJECT)** via des **seuils configurables**.

> **Message clé** : le modèle assiste la décision, mais la décision finale reste métier.

## 🇬🇧 Summary (EN)

This project implements a **credit risk scoring** system: an ML model outputs **P(bad)** and a business layer converts it into an actionable decision **(ACCEPT / REVIEW / REJECT)** using configurable thresholds.

> **Key message**: the model supports decision-making, but the final decision remains business-driven.

## Objectifs / Goals

- EDA + préparation des données (**credit-g**, OpenML)
- Entraîner et évaluer des modèles (baseline + comparaison)
- Exposer le scoring via une **API Flask**
- Proposer une **UI web** orientée métier (dashboard de décision)
- Bonnes pratiques : **black, ruff, pre-commit, pytest, Docker, Cloud Run** (WIF)

## Architecture

```text
src/
 ├── api/                # API Flask (UI + endpoints)
 ├── credit_g_ml/        # Pipeline ML (data, preprocessing, modeling)
scripts/                 # Download / training / threshold tuning
ui/                      # Templates & static assets
data/                    # Dataset (downloaded at build time)
models/                  # Trained artifact (inside Docker image)
reports/                 # Metrics & visualizations
tests/                   # Unit tests
```

## Résultats (baseline)

Baseline : **Logistic Regression** (modèle interprétable, stable, adapté au scoring crédit)
- ROC AUC ≈ **0.78**
- Rappel "bad" correct (priorité métier : éviter les faux négatifs)

Rapports :
- `reports/baseline_logistic_regression.md`
- `reports/roc_curve_logistic_regression.png`

## Business Decision Thresholds (Model v3)

Le modèle sous-jacent reste identique (Logistic Regression) ; seule la couche de décision évolue.

### Pourquoi ?

Une simple probabilité **P(bad)** est difficile à exploiter telle quelle.
En crédit, on a souvent besoin de :

- **refus automatique** pour les dossiers très risqués
- **acceptation automatique** pour les dossiers très sûrs
- **zone grise** → revue humaine

### Règle (3 états)

Deux seuils :
- `A` : seuil d’acceptation
- `R` : seuil de rejet

Décision :
- **ACCEPT** si P(bad) < A
- **REVIEW** si A ≤ P(bad) < R
- **REJECT** si P(bad) ≥ R

Exemple :

| **Seuil** | **Valeur** |
| --------- | ---------- |
| `A`       | 0.15       |
| `R`       | 0.35       |

### Seuil optimal (analyse coût)

Une analyse coût simple (pondération FN / FP, côté métier) a conduit au seuil optimal suivant :

```text
Seuil optimal ≈ 0.15
Coût total = 114
FN = 3
FP = 99
```

Ce seuil sert naturellement de A. Le seuil R est volontairement plus conservateur que A afin de limiter les faux positifs critiques.

### UI

L’interface met en évidence :
- `P(bad)` (score modèle)
- seuils `A` (accept) et `R` (reject)
- **décision finale** (ACCEPT / REVIEW / REJECT)
- séparation claire : **risque (informatif)** vs **règle métier (décision)**

## Feature Importance (interprétabilité)

Pour améliorer la compréhension du modèle (Logistic Regression), on analyse les **coefficients** :
- |coef| = proxy d’importance
- signe du coef : influence positive (↑ risque) ou négative (↓ risque)

Indicatif (dépend du prétraitement et des corrélations), ce n’est pas une règle métier.
Ces informations sont destinées à l’analyse et à la communication, pas à l’automatisation de décisions.

### Top 20 :
![Feature importance – Logistic Regression](reports/feature_importance_logreg_top20.png)

### Détails :
- `reports/feature_importance_logreg_top20.csv`

## Quickstart (Makefile)

Le projet inclut un Makefile pour standardiser les commandes (local / Docker / CI).

| **Commande**        | **Description** |
|-----------------|-------------|
| `make help`     | Liste les commandes |
| `make install`  | Installe les dépendances |
| `make lint`     | Lint (ruff) |
| `make format`   | Format (black) |
| `make test`     | Tests (pytest) |
| `make run`      | Run local (Flask) |
| `make docker-build` | Build image Docker |
| `make docker-run`   | Run via Docker |
| `make smoke`    | Test santé API |

## Exécution en local

Recommandé :
```bash
make run
```

Alternative :
```bash
export PYTHONPATH=src
python -m api.app
```

Accès :
- UI : http://127.0.0.1:5001/
- Health : http://127.0.0.1:5001/health

Smoke test :
```bash
make smoke
```

## API – Scoring & Decision

### Health
```
GET /health
curl http://127.0.0.1:5001/health
```

### Predict
```
POST /predict
```

Exemple :
```bash
curl http://127.0.0.1:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 24,
    "credit_amount": 5000,
    "installment_commitment": 3,
    "residence_since": 4,
    "age": 45,
    "existing_credits": 2,
    "num_dependents": 1,
    "checking_status": "0<=X<200",
    "credit_history": "existing paid",
    "purpose": "new car",
    "savings_status": "500<=X<1000",
    "employment": "4<=X<7",
    "personal_status": "female div/dep/mar",
    "other_parties": "guarantor",
    "property_magnitude": "car",
    "other_payment_plans": "bank",
    "housing": "rent",
    "job": "unskilled resident",
    "own_telephone": "none",
    "foreign_worker": "yes"
  }'
```

Réponse (exemple) :

```json
{
  "label": "bad",
  "probability_bad": 0.73,
  "probability_good": 0.27,
  "risk_level": "high"
}
```

## Docker

### Via Makefile

```bash
make docker-build
make docker-run
```

### Commandes brutes

```bash
docker build -t pdi-credit-risk-ml
docker run --rm -p 5001:5000 -e PORT=5000 pdi-credit-risk-ml
```

Accès :

- UI: `http://127.0.0.1:5001`
- Démos : `/demo/low`, `/demo/medium`, `/demo/high`
- Fullscreen : `/demo/full/<level>`

## Sécurité API (minimaliste)

L’UI est publique. L’API /predict est protégée via un token. Cette protection est volontairement simple et illustrative (hors OAuth / IAM).

### Header requis

```http
X-API-TOKEN: your-api-token
```

## Live Demo (Cloud Run)

App : https://pdi-credit-risk-ml-mbn4mquhua-ew.a.run.app

### Script de démo (~3 min) :
1. Contexte + score P(bad)
2. /demo/full/low → ACCEPT
3. /demo/full/medium → REVIEW
4. /demo/full/high → REJECT

---

## 👤 Auteur
Franck Ngaha — PDI (Développeur orienté IA) — © 2026
