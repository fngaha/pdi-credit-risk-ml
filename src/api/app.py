from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request
from pydantic import ValidationError

from api.demo_profiles import DEMO_PROFILES
from api.schemas import CreditRiskRequest, CreditRiskResponse
from credit_g_ml.config import THRESHOLD_BAD
from credit_g_ml.inference import load_model, predict_single
from credit_g_ml.metadata import get_categorical_values

API_TOKEN = os.getenv("API_TOKEN")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
UI_DIR = PROJECT_ROOT / "ui"

app = Flask(
    __name__,
    template_folder=str(UI_DIR / "templates"),
    static_folder=str(UI_DIR / "static"),
)

MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        str(PROJECT_ROOT / "models" / "logistic_regression_pipeline.joblib"),
    )
)

_pipeline: Any | None = None


DEFAULT_FORM = {
    "threshold": THRESHOLD_BAD,
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
    "foreign_worker": "yes",
}


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = load_model(MODEL_PATH)
    return _pipeline


def compute_risk_level(p_bad: float) -> str:
    # Niveau de risque "informatif" (indépendant du seuil métier)
    if p_bad >= 0.7:
        return "high"
    if p_bad >= 0.4:
        return "medium"
    return "low"


def compute_decision(p_bad: float, threshold: float) -> str:
    return "reject" if p_bad >= threshold else "accept"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict():
    # Sécurité minimale par token
    if API_TOKEN:
        client_token = request.headers.get("X-API-TOKEN")
        if not client_token or client_token != API_TOKEN:
            return jsonify({"error": "unauthorized"}), 401
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "invalid_json"}), 400
        req = CreditRiskRequest(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 422
    except Exception:
        return jsonify({"error": "invalid_json"}), 400

    pipeline = get_pipeline()

    result = predict_single(pipeline, req.model_dump())
    risk_level = compute_risk_level(result.probability_bad)
    decision = compute_decision(result.probability_bad, THRESHOLD_BAD)

    resp = CreditRiskResponse(
        label=result.label,
        probability_bad=result.probability_bad,
        probability_good=result.probability_good,
        risk_level=risk_level,
        threshold_bad=THRESHOLD_BAD,
        decision=decision,
    )
    return jsonify(resp.model_dump())


@app.get("/")
def home():
    categorical_options = get_categorical_values()
    return render_template(
        "index.html",
        api_token=os.getenv("API_TOKEN", ""),
        categorical_options=categorical_options,
        form=DEFAULT_FORM,
    )


@app.post("/ui/predict")
def ui_predict():
    form_payload = request.form.to_dict()
    threshold_str = form_payload.get("threshold", str(THRESHOLD_BAD))
    threshold = float(threshold_str)
    threshold = max(0.0, min(1.0, threshold))  # clamp sécurité

    try:
        for k in [
            "duration",
            "credit_amount",
            "installment_commitment",
            "residence_since",
            "age",
            "existing_credits",
            "num_dependents",
        ]:
            if k == "credit_amount":
                form_payload[k] = float(form_payload[k])
            else:
                form_payload[k] = int(form_payload[k])

        req = CreditRiskRequest(**form_payload)
    except ValidationError as e:
        return (
            render_template(
                "index.html",
                error="Validation error",
                details=e.errors(),
                form=form_payload,
                categorical_options=get_categorical_values(),
            ),
            422,
        )
    except Exception as e:
        return (
            render_template(
                "index.html",
                error=f"Invalid form data: {e}",
                form=form_payload,
                categorical_options=get_categorical_values(),
            ),
            400,
        )

    pipeline = get_pipeline()

    result = predict_single(pipeline, req.model_dump())
    business_decision = "reject" if result.probability_bad >= threshold else "accept"
    risk_level = compute_risk_level(result.probability_bad)

    return render_template(
        "index.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
            "threshold": threshold,
            "business_decision": business_decision,
        },
        form=req.model_dump() | {"threshold": threshold},
        categorical_options=get_categorical_values(),
    )


@app.get("/demo/<level>")
def demo(level: str):
    if level not in DEMO_PROFILES:
        return "Unknown demo profile", 404

    threshold = THRESHOLD_BAD
    payload = DEMO_PROFILES[level]

    pipeline = get_pipeline()

    req = CreditRiskRequest(**payload)
    result = predict_single(pipeline, req.model_dump())

    business_decision = "reject" if result.probability_bad >= threshold else "accept"
    risk_level = compute_risk_level(result.probability_bad)
    categorical_options = get_categorical_values()

    return render_template(
        "index.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
            "threshold": threshold,
            "business_decision": business_decision,
        },
        form=req.model_dump() | {"threshold": threshold},
        categorical_options=categorical_options,
    )


@app.get("/demo/full/<level>")
def demo_full(level: str):
    if level not in DEMO_PROFILES:
        return "Unknown demo profile", 404

    threshold = THRESHOLD_BAD
    payload = DEMO_PROFILES[level]

    pipeline = get_pipeline()

    req = CreditRiskRequest(**payload)
    result = predict_single(pipeline, req.model_dump())

    business_decision = "reject" if result.probability_bad >= threshold else "accept"
    risk_level = compute_risk_level(result.probability_bad)

    return render_template(
        "demo_full.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
            "threshold": threshold,
            "business_decision": business_decision,
        },
        current_level=level,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
