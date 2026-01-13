from __future__ import annotations

from api.demo_profiles import DEMO_PROFILES
from credit_g_ml.config import THRESHOLD_ACCEPT, THRESHOLD_REJECT
from credit_g_ml.inference import load_model, predict_single


def decision(p_bad: float) -> str:
    if p_bad >= THRESHOLD_REJECT:
        return "reject"
    if p_bad >= THRESHOLD_ACCEPT:
        return "review"
    return "accept"


def main() -> None:
    pipeline = load_model()
    print(
        f"Seuils: accept={THRESHOLD_ACCEPT:.2f} | " f"reject={THRESHOLD_REJECT:.2f}\n"
    )

    for name, payload in DEMO_PROFILES.items():
        r = predict_single(pipeline, payload)

        if r.probability_bad < 0.4:
            risk = "low"
        elif r.probability_bad < 0.7:
            risk = "medium"
        else:
            risk = "high"

        print(
            f"{name.upper():6}  "
            f"P(bad)={r.probability_bad:.3f}  "
            f"risk={risk:6}  "
            f"decision={decision(r.probability_bad)}"
        )


if __name__ == "__main__":
    main()
