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

## API – Credit Risk Scoring
### Prérequis

- Environnement conda actif :

```conda activate pdi-credit-risk-m```

- Modèle entraîné (une fois) :

```python scripts/train_model.py```

Cela génère le fichier :

```models/logistic_regression_pipeline.jobli```

### Lancer l’API localement

Depuis la racine du projet :

```
export PYTHONPATH=src
python -m api.app
```


Le serveur démarre par défaut sur :

```http://127.0.0.1:5000```

Endpoint de santé

GET ```/health```

Permet de vérifier que l’API est opérationnelle.

```curl http://127.0.0.1:5000/health```


Réponse attendue :

```json
{
  "status": "ok"
}
```

### Endpoint de prédiction

POST ```/predict```

Retourne une prédiction de risque crédit pour un client donné.

Exemple de requête

```
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

Exemple de réponse

```json
{
  "label": "bad",
  "probability_bad": 0.7302879499577739,
  "probability_good": 0.26971205004222615,
  "risk_level": "high"
}
```

Champs de la réponse

- `label` : classe prédite par le modèle (`good` ou `bad`)

- `probability_bad` : probabilité estimée d’être un mauvais payeur

- `probability_good` : probabilité estimée d’être un bon payeur

- `risk_level` :

  - `low` : risque faible

  - `medium` : risque modéré

  - `high` : risque élevé

Le niveau de risque est déterminé à partir de la probabilité `bad` selon des seuils simples, configurables dans l’API.

### Validation des entrées

Les données d’entrée sont validées côté API :

- types (numérique / chaîne),

- bornes sur les variables numériques,

- présence obligatoire de toutes les features attendues.

En cas d’erreur, l’API retourne une réponse `422` avec le détail des champs invalides.

### Notes

- Le modèle est chargé au démarrage de l’API.

- Le pipeline inclut le préprocessing et le modèle (aucune transformation manuelle requise côté client).

- Cette API constitue une base démontrable pour une intégration UI ou un déploiement ultérieur.

## Run with Docker

### Build

```bash
docker build -t pdi-credit-risk-ml .
```
### Run
```
docker run --rm -p 5001:5000 -e PORT=5000 pdi-credit-risk-ml
```
Then open:

- UI: http://127.0.0.1:5001/

- Health: http://127.0.0.1:5001/health

- Demo profiles:

  - http://127.0.0.1:5001/demo/low

  - http://127.0.0.1:5001/demo/medium

  - http://127.0.0.1:5001/demo/high
