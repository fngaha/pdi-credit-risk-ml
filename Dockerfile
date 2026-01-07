FROM python:3.11-slim

# Bonnes pratiques
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances (cache docker optimisé)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et des assets
COPY src /app/src
COPY ui /app/ui
COPY models /app/models
COPY data /app/data
COPY reports /app/reports
COPY README.md /app/README.md

# Très important : permettre "python -m api.app" avec src layout
ENV PYTHONPATH=/app/src
ENV MODEL_PATH=/app/models/logistic_regression_pipeline.joblib

EXPOSE 5000

CMD ["python", "-m", "api.app"]
