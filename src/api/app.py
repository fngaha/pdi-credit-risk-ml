from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request
from pydantic import ValidationError

from api.demo_profiles import DEMO_PROFILES
from api.schemas import CreditRiskRequest, CreditRiskResponse
from credit_g_ml.config import THRESHOLD_ACCEPT, THRESHOLD_REJECT
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
    "threshold": THRESHOLD_ACCEPT,
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


def compute_decision(p_bad: float) -> str:
    """Décision métier en 3 états selon P(bad)."""
    if p_bad >= THRESHOLD_REJECT:
        return "reject"
    if p_bad >= THRESHOLD_ACCEPT:
        return "review"
    return "accept"


def compute_risk_level(p_bad: float) -> str:
    """Niveau de risque aligné sur les seuils métier."""
    if p_bad >= THRESHOLD_REJECT:
        return "high"
    if p_bad >= THRESHOLD_ACCEPT:
        return "medium"
    return "low"


def compute_risk_level_with_thresholds(
    p_bad: float, accept: float, reject: float
) -> str:
    """Niveau de risque basé sur des seuils (utile pour le slider)."""
    if p_bad >= reject:
        return "high"
    if p_bad >= accept:
        return "medium"
    return "low"


def compute_decision_with_thresholds(p_bad: float, accept: float, reject: float) -> str:
    """Décision métier basée sur des seuils (utile pour le slider)."""
    if p_bad >= reject:
        return "reject"
    if p_bad >= accept:
        return "review"
    return "accept"


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
    p_bad = result.probability_bad
    risk_level = compute_risk_level(p_bad)
    decision = compute_decision(p_bad)

    resp = CreditRiskResponse(
        label=result.label,
        probability_bad=result.probability_bad,
        probability_good=result.probability_good,
        risk_level=risk_level,
        threshold_accept=THRESHOLD_ACCEPT,
        threshold_reject=THRESHOLD_REJECT,
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
    threshold_str = form_payload.get("threshold", str(THRESHOLD_ACCEPT))
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

    threshold_accept = threshold  # slider
    threshold_reject = THRESHOLD_REJECT
    threshold_accept = min(threshold_accept, threshold_reject - 1e-6)

    pipeline = get_pipeline()
    result = predict_single(pipeline, req.model_dump())
    p_bad = result.probability_bad
    risk_level = compute_risk_level_with_thresholds(
        p_bad, threshold_accept, threshold_reject
    )
    business_decision = compute_decision_with_thresholds(
        p_bad, threshold_accept, threshold_reject
    )

    return render_template(
        "index.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
            "threshold_accept": threshold_accept,
            "threshold_reject": threshold_reject,
            "business_decision": business_decision,
        },
        form=req.model_dump() | {"threshold": threshold_accept},
        categorical_options=get_categorical_values(),
    )


@app.get("/demo/<level>")
def demo(level: str):
    if level not in DEMO_PROFILES:
        return "Unknown demo profile", 404

    payload = DEMO_PROFILES[level]

    pipeline = get_pipeline()

    req = CreditRiskRequest(**payload)
    result = predict_single(pipeline, req.model_dump())
    p_bad = result.probability_bad
    risk_level = compute_risk_level(p_bad)
    business_decision = compute_decision(p_bad)
    categorical_options = get_categorical_values()

    return render_template(
        "index.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
            "threshold_accept": THRESHOLD_ACCEPT,
            "threshold_reject": THRESHOLD_REJECT,
            "business_decision": business_decision,
        },
        form=req.model_dump() | {"threshold": THRESHOLD_ACCEPT},
        categorical_options=categorical_options,
    )


@app.get("/demo/full/<level>")
def demo_full(level: str):
    if level not in DEMO_PROFILES:
        return "Unknown demo profile", 404

    payload = DEMO_PROFILES[level]

    pipeline = get_pipeline()

    req = CreditRiskRequest(**payload)
    result = predict_single(pipeline, req.model_dump())
    p_bad = result.probability_bad
    risk_level = compute_risk_level(p_bad)
    business_decision = compute_decision(p_bad)

    return render_template(
        "demo_full.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
            "threshold_accept": THRESHOLD_ACCEPT,
            "threshold_reject": THRESHOLD_REJECT,
            "business_decision": business_decision,
        },
        current_level=level,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
