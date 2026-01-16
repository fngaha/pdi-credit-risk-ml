SHELL := /bin/bash

# -----------------------
# Configuration générale
# -----------------------
PY ?= python
HOST ?= 127.0.0.1
PORT ?= 5001

IMAGE ?= pdi-credit-risk-ml
TAG ?= latest

# Cloud Run
SERVICE ?= pdi-credit-risk-ml
REGION ?= europe-west1

.DEFAULT_GOAL := help

# -----------------------
# Aide
# -----------------------
.PHONY: help
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Développement"
	@echo "  run              Lancer l'app Flask en local"
	@echo "  demo             Afficher les URLs de démo"
	@echo ""
	@echo "Data / ML"
	@echo "  data             Télécharger le dataset credit-g"
	@echo "  train            Entraîner le modèle"
	@echo "  eval             Évaluer le modèle"
	@echo ""
	@echo "Qualité"
	@echo "  fmt              Formatage (black)"
	@echo "  lint             Lint (ruff)"
	@echo "  test             Tests (pytest)"
	@echo "  check            Lint + tests"
	@echo ""
	@echo "Docker"
	@echo "  docker-build     Build de l'image Docker"
	@echo "  docker-run       Lancer le conteneur Docker"
	@echo ""
	@echo "Cloud Run"
	@echo "  deploy           Déployer sur Cloud Run"
	@echo "  logs             Voir les logs Cloud Run"
	@echo ""

# -----------------------
# Développement local
# -----------------------
.PHONY: run
run:
	@echo "App disponible sur http://$(HOST):$(PORT)"
	PYTHONPATH=src PORT=$(PORT) $(PY) src/api/app.py

.PHONY: demo
demo:
	@echo "Démo URLs :"
	@echo "  http://$(HOST):$(PORT)/demo/low"
	@echo "  http://$(HOST):$(PORT)/demo/medium"
	@echo "  http://$(HOST):$(PORT)/demo/high"
	@echo "  http://$(HOST):$(PORT)/demo/full/medium"

# -----------------------
# Data / ML
# -----------------------
.PHONY: data
data:
	$(PY) scripts/download_credit_g.py

.PHONY: train
train:
	$(PY) scripts/train_model.py

.PHONY: eval
eval:
	$(PY) scripts/evaluate_model.py

# -----------------------
# Qualité
# -----------------------
.PHONY: fmt
fmt:
	black .

.PHONY: lint
lint:
	ruff check .

.PHONY: test
test:
	PYTHONPATH=src pytest -q

.PHONY: check
check: lint test

# -----------------------
# Smoke test API
# -----------------------
BASE_URL ?= http://127.0.0.1:$(PORT)
API_TOKEN ?=

.PHONY: smoke
smoke:
	@echo "== Smoke test: $(BASE_URL) =="
	@echo ""
	@echo "[1/2] GET /health"
	@curl -sS $(BASE_URL)/health | python -m json.tool
	@echo ""
	@echo "[2/2] POST /predict"
	@curl -sS -X POST $(BASE_URL)/predict \
		-H "Content-Type: application/json" \
		$(if $(API_TOKEN),-H "X-API-TOKEN: $(API_TOKEN)",) \
		-d '{"duration":24,"credit_amount":5000,"installment_commitment":3,"residence_since":4,"age":45,"existing_credits":2,"num_dependents":1,"checking_status":"0<=X<200","credit_history":"existing paid","purpose":"new car","savings_status":"500<=X<1000","employment":"4<=X<7","personal_status":"female div/dep/mar","other_parties":"guarantor","property_magnitude":"car","other_payment_plans":"bank","housing":"rent","job":"unskilled resident","own_telephone":"none","foreign_worker":"yes"}' \
		| python -m json.tool

# -----------------------
# Docker
# -----------------------
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE):$(TAG) .

.PHONY: docker-run
docker-run:
	@echo "App Docker disponible sur http://localhost:5001"
	docker run --rm \
		-p 5001:5000 \
		-e PORT=5000 \
		$(IMAGE):$(TAG)

# -----------------------
# Cloud Run
# -----------------------
.PHONY: deploy
deploy:
	gcloud run deploy $(SERVICE) \
		--source . \
		--region $(REGION) \
		--allow-unauthenticated

.PHONY: logs
logs:
	gcloud run services logs tail $(SERVICE) --region $(REGION)
