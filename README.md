# pdi-credit-risk-ml

![Deploy to Cloud Run](https://github.com/fngaha/pdi-credit-risk-ml/actions/workflows/deploy-cloudrun.yml/badge.svg)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://pdi-credit-risk-ml-mbn4mquhua-ew.a.run.app)

**Projet de fin de formation – Développeur orienté IA**

Scoring de risque crédit basé sur le dataset **credit-g** (OpenML), développé selon la méthodologie **CRISP-DM** et déployé en production sur **Google Cloud Run** via CI/CD GitHub Actions.

## Objectifs

- Explorer et préparer les données **(EDA)**

- Entraîner un modèle de machine learning pour prédire le risque de défaut

- Exposer le modèle via une **API Flask**

- Proposer une **interface web métier** pour le scoring client

- Mettre en œuvre des **bonnes pratiques professionnelles** :

  - formatage du code avec **black**

  - linting avec **ruff**

  - hooks **pre-commit**

  - tests automatisés avec **pytest**

  - conteneurisation **Docker**

  - déploiement **Cloud Run** (keyless via **WIF**)

## Architecture du projet

```text
src/
 ├── api/                # API Flask
 ├── credit_g_ml/        # Pipeline ML (data, preprocessing, modeling)
scripts/                 # Entraînement et téléchargement du dataset
ui/                      # Interface web (dashboard)
data/                    # Données (téléchargées au build)
models/                  # Modèle entraîné (dans l’image Docker)
reports/                 # Résultats & visualisations
tests/                   # Tests unitaires
```

## Résultats – Modèle baseline

Le modèle baseline (Logistic Regression) atteint :

- ROC AUC ≈ 0.78
- Bon rappel sur la classe "bad" (objectif métier prioritaire)

Rapports disponibles :
- `reports/baseline_logistic_regression.md`
- `reports/roc_curve_logistic_regression.png`

## API – Credit Risk Scoring

### Démarrage local

Activer l’environnement conda :

```bash
conda activate pdi-credit-risk-ml
```

Lancer l’API :

```bash
export PYTHONPATH=src
python -m api.app
```

API disponible sur :

```cpp
http://127.0.0.1:5000
```

### Endpoint de santé

```http
GET /health
```

```bash
curl http://127.0.0.1:5000/health
```

Réponse :

```json
{
  "status": "ok"
}
```

### Endpoint de prédiction

```http
POST /predict
```

Exemple de requête :

```bash
curl -X POST http://127.0.0.1:5000/predict \
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

Exemple de réponse :

```json
{
  "label": "bad",
  "probability_bad": 0.7302879499577739,
  "probability_good": 0.26971205004222615,
  "risk_level": "high"
}
```

Champs retournés :

- `label` : classe prédite (`good` ou `bad`)

- `probability_bad` : probabilité de défaut

- `probability_good` : probabilité de non défaut

- `risk_level` :

  - `low` : risque faible

  - `medium` : risque modéré

  - `high` : risque élevé

> Le modèle fournit un **score probabiliste**.<br>
> La décision finale est pilotée par **des règles métier explicites** (seuils configurables).

### Validation des entrées

Les entrées sont validées côté API :

- types des champs

- bornes numériques

- présence obligatoire de toutes les features

En cas d’erreur → réponse **HTTP 422** avec détail.

## Exécution avec Docker

### Build

```bash
docker build -t pdi-credit-risk-ml .
```

### Run

```bash
docker run --rm -p 5001:5000 -e PORT=5000 pdi-credit-risk-ml
```

Accès :

- UI: http://127.0.0.1:5001/

- Health: http://127.0.0.1:5001/health

- Demo profiles:

  - /demo/low

  - /demo/medium

  - /demo/high

## Sécurité API (minimaliste)

L’endpoint /predict est protégé par un token via variable d’environnement.

### Header requis

```http
X-API-TOKEN: your-api-token
```

Exemple :
```bash
curl -X POST https://pdi-credit-risk-ml-mbn4mquhua-ew.a.run.app/predict \
  -H "Content-Type: application/json" \
  -H "X-API-TOKEN: <your-api-token>" \
  -d '{...}'
```

L’UI reste publique, seule l’API est protégée.

## Live demo – Cloud Run

https://pdi-credit-risk-ml-mbn4mquhua-ew.a.run.app

### Script de démonstration (≈ 3 minutes)

1. Contexte

    - Cas réel de scoring crédit

    - Modèle ML + API + dashboard métier

2. Risque faible

    - /demo/full/low

    - Acceptation immédiate

3. Cas intermédiaire

    - /demo/full/medium

    - Décision dépendante du seuil métier

4. Risque élevé

    - /demo/full/high

    - Rejet automatique

    - Visualisation claire (jauge, badges)

### Message clé

> Le modèle assiste la décision,<br>
> mais **la décision finale reste métier**.

---

👤 Auteur<br>
Franck O. Ngaha<br>
Projet de développement individuel – Développeur orienté IA<br>
© 2026
