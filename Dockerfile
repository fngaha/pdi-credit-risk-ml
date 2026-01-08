FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier code + ressources nécessaires au build du modèle
COPY src /app/src
COPY scripts /app/scripts
COPY ui /app/ui
COPY reports /app/reports
COPY README.md /app/README.md

# Important pour layout src/ (api et credit_g_ml)
ENV PYTHONPATH=/app/src

# Assurer que reports/ existe (le script y écrit la ROC)
RUN mkdir -p /app/reports /app/data/raw

# Entraîner le modèle au build (crée /app/models/...)
RUN python /app/scripts/download_credit_g.py
RUN python /app/scripts/train_model.py

# Chemin modèle utilisé par l'API
ENV MODEL_PATH=/app/models/logistic_regression_pipeline.joblib

EXPOSE 5000

CMD ["python", "-m", "api.app"]
