from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ajoute src/ et api/ au path pour importer app
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))
sys.path.append(str(PROJECT_ROOT))

from api.app import app  # noqa: E402


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_predict_validation_error(client):
    resp = client.post("/predict", json={"foo": "bar"})
    assert resp.status_code == 422
    body = resp.get_json()
    assert body["error"] == "validation_error"
