# Model v3 – Seuil métier (cost-based)

## Hypothèses de coût
- Coût FN (bad prédit good) : **5**
- Coût FP (good prédit bad) : **1**

## Résultat
- Seuil optimal : **0.15** (coût total = **114**)

## Détails au seuil optimal
- FN (bad → good) : **3**
- FP (good → bad) : **99**
- TN (bad → bad) : **57**
- TP (good → good) : **41**

## Tableau (grille de seuils)

| Seuil | Coût | FN (bad→good) | FP (good→bad) |
|---:|---:|---:|---:|
| 0.05 | 138 | 0 | 138 |
| 0.10 | 130 | 2 | 120 |
| 0.15 | 114 | 3 | 99 |
| 0.20 | 121 | 7 | 86 |
| 0.25 | 122 | 11 | 67 |
| 0.30 | 127 | 15 | 52 |
| 0.35 | 129 | 18 | 39 |
| 0.40 | 170 | 28 | 30 |
| 0.45 | 177 | 32 | 17 |
| 0.50 | 205 | 38 | 15 |
| 0.55 | 230 | 44 | 10 |
| 0.60 | 240 | 47 | 5 |
| 0.65 | 267 | 53 | 2 |
| 0.70 | 290 | 58 | 0 |
| 0.75 | 300 | 60 | 0 |
| 0.80 | 300 | 60 | 0 |
| 0.85 | 300 | 60 | 0 |
| 0.90 | 300 | 60 | 0 |
| 0.95 | 300 | 60 | 0 |
