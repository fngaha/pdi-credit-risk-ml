from __future__ import annotations

import pandas as pd

from credit_g_ml.config import RAW_DATA_DIR, THRESHOLD_ACCEPT, THRESHOLD_REJECT
from credit_g_ml.inference import load_model, predict_single
from credit_g_ml.schemas import ALL_FEATURES

TARGETS = {
    "low": THRESHOLD_ACCEPT * 0.6,  # bien en dessous
    "medium": (THRESHOLD_ACCEPT + THRESHOLD_REJECT) / 2,  # au milieu
    "high": min(0.95, THRESHOLD_REJECT + 0.25),  # bien au dessus
}


def main() -> None:
    csv_path = RAW_DATA_DIR / "credit_g_raw.csv"
    df = pd.read_csv(csv_path)
    pipeline = load_model()

    best = {k: (999.0, None) for k in TARGETS}  # (distance, row_payload)

    for _, row in df.iterrows():
        payload = {c: row[c] for c in ALL_FEATURES}
        r = predict_single(pipeline, payload)
        p = r.probability_bad

        for name, target in TARGETS.items():
            d = abs(p - target)
            if d < best[name][0]:
                best[name] = (d, payload | {"_p_bad": p})

    for name, (_, payload) in best.items():
        print(f"\n=== {name.upper()} candidate (target={TARGETS[name]:.3f}) ===")
        print(f"P(bad)={payload['_p_bad']:.3f}")
        payload.pop("_p_bad")
        print(payload)


if __name__ == "__main__":
    main()
