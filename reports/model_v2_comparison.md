# Model v2 – Comparison

Same split, same features, same preprocessing.

| Model | ROC AUC | Precision (bad) | Recall (bad) | F1 (bad) | Artifact |
|---|---:|---:|---:|---:|---|
| random_forest | 0.786 | 0.538 | 0.350 | 0.424 | `/Users/franckngaha/Library/CloudStorage/GoogleDrive-franck.o.ngaha@gmail.com/Mon Drive/Menage/1_Membres_du_menage/1_Franck_Ngaha/3_Emploi_et_carriere/2025-Formations/Technofuture TIC/Formation développeur orienté IA/PDI/pdi-credit-risk-ml/models/random_forest_pipeline.joblib` |
| logistic_regression | 0.760 | 0.472 | 0.700 | 0.564 | `/Users/franckngaha/Library/CloudStorage/GoogleDrive-franck.o.ngaha@gmail.com/Mon Drive/Menage/1_Membres_du_menage/1_Franck_Ngaha/3_Emploi_et_carriere/2025-Formations/Technofuture TIC/Formation développeur orienté IA/PDI/pdi-credit-risk-ml/models/logistic_regression_pipeline.joblib` |
| hist_gradient_boosting | 0.760 | 0.604 | 0.533 | 0.566 | `/Users/franckngaha/Library/CloudStorage/GoogleDrive-franck.o.ngaha@gmail.com/Mon Drive/Menage/1_Membres_du_menage/1_Franck_Ngaha/3_Emploi_et_carriere/2025-Formations/Technofuture TIC/Formation développeur orienté IA/PDI/pdi-credit-risk-ml/models/hist_gradient_boosting_pipeline.joblib` |
