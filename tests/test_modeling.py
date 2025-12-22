"""Tests pour le module modeling."""

from credit_g_ml.modeling import build_logistic_regression_pipeline


def test_build_logistic_pipeline() -> None:
    pipeline = build_logistic_regression_pipeline()
    assert "preprocessor" in pipeline.named_steps
    assert "model" in pipeline.named_steps
