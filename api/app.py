from __future__ import annotations

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from pydantic import ValidationError

# Pour importer src/credit_g_ml
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from schemas import CreditRiskRequest, CreditRiskResponse  # noqa: E402

from credit_g_ml.inference import load_model, predict_single  # noqa: E402

UI_DIR = PROJECT_ROOT / "ui"
app = Flask(
    __name__,
    template_folder=UI_DIR / "templates",
    static_folder=UI_DIR / "static",
)

# Charger le modèle au démarrage (simple et efficace pour un PDI)
MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        str(PROJECT_ROOT / "models" / "logistic_regression_pipeline.joblib"),
    )
)
pipeline = load_model(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict():
    try:
        payload = request.get_json(force=True)
        req = CreditRiskRequest(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 422
    except Exception:
        return jsonify({"error": "invalid_json"}), 400

    result = predict_single(pipeline, req.model_dump())

    # Risk level simple (tu pourras le rendre configurable ensuite)
    if result.probability_bad >= 0.7:
        risk_level = "high"
    elif result.probability_bad >= 0.4:
        risk_level = "medium"
    else:
        risk_level = "low"

    resp = CreditRiskResponse(
        label=result.label,
        probability_bad=result.probability_bad,
        probability_good=result.probability_good,
        risk_level=risk_level,
    )

    return jsonify(resp.model_dump())


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/ui/predict")
def ui_predict():
    try:
        form_payload = request.form.to_dict()

        # Conversion types numériques (les champs HTML arrivent en string)
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
            ),
            422,
        )
    except Exception as e:
        return (
            render_template(
                "index.html",
                error=f"Invalid form data: {e}",
                form=form_payload,
            ),
            400,
        )

    result = predict_single(pipeline, req.model_dump())

    if result.probability_bad >= 0.7:
        risk_level = "high"
    elif result.probability_bad >= 0.4:
        risk_level = "medium"
    else:
        risk_level = "low"

    return render_template(
        "index.html",
        result={
            "label": result.label,
            "probability_bad": result.probability_bad,
            "probability_good": result.probability_good,
            "risk_level": risk_level,
        },
        form=req.model_dump(),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
