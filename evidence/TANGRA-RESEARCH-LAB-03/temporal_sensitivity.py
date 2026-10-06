#!/usr/bin/env python3
"""Deterministic temporal-sensitivity calculations for TANGRA Research Lab JOB-03.

This is an evidence classification and unit-conversion artifact. It does not
model the target population, estimate probability, or validate physical error.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


EVIDENCED = {
    "current_fps": {
        "no_target_average": 41.28,
        "tracking_average": 36.016,
        "tracking_minimum_sample": 28.368,
        "tracking_maximum_sample": 39.059,
        "static_recent_five_sample_mean": 41.10,
        "static_recent_five_sample_minimum": 36.96,
        "static_recent_five_sample_maximum": 43.58,
    },
    "static_pair_delta_ms": [4.807, 44.751, 50.691],
    "historical_2026_07_27_frame_period_ms": {
        "live_mean": 62.687,
        "live_median": 54.756,
        "live_p95": 79.528,
        "replay_mean": 67.097,
        "replay_median": 60.073,
        "replay_p95": 84.119,
    },
    "wide_stale_threshold_ms": 500.0,
}

SYNTHETIC = {
    "velocity_mps": [1.0, 5.0, 10.0, 25.0],
    "age_ms": [0.0, 25.0, 50.0, 100.0, 250.0, 500.0],
    "jitter_ms": [1.0, 5.0, 10.0, 25.0, 50.0],
    "missed_frame_count": [1, 2, 3, 5, 10],
}


def period_ms(fps: float) -> float:
    return 1000.0 / fps


def displacement_m(velocity_mps: float, duration_ms: float) -> float:
    return velocity_mps * duration_ms / 1000.0


def rounded(value: float) -> float:
    return round(value, 9)


def build() -> dict:
    current_periods = {
        name: rounded(period_ms(value))
        for name, value in EVIDENCED["current_fps"].items()
    }

    synthetic_age = []
    for velocity in SYNTHETIC["velocity_mps"]:
        for age in SYNTHETIC["age_ms"]:
            synthetic_age.append(
                {
                    "velocity_mps": velocity,
                    "age_ms": age,
                    "uncompensated_displacement_m": rounded(
                        displacement_m(velocity, age)
                    ),
                }
            )

    synthetic_jitter = []
    for velocity in SYNTHETIC["velocity_mps"]:
        for jitter in SYNTHETIC["jitter_ms"]:
            synthetic_jitter.append(
                {
                    "velocity_mps": velocity,
                    "jitter_ms": jitter,
                    "incremental_displacement_m": rounded(
                        displacement_m(velocity, jitter)
                    ),
                }
            )

    # A missed-frame count is converted to elapsed time only. The calculation
    # intentionally assumes neither a tracker policy nor successful recovery.
    synthetic_dropout = []
    for cadence_name in ("no_target_average", "tracking_average"):
        frame_period = current_periods[cadence_name]
        for missed in SYNTHETIC["missed_frame_count"]:
            elapsed = missed * frame_period
            for velocity in SYNTHETIC["velocity_mps"]:
                synthetic_dropout.append(
                    {
                        "cadence_basis": cadence_name,
                        "frame_period_ms": frame_period,
                        "missed_frames": missed,
                        "elapsed_ms": rounded(elapsed),
                        "velocity_mps": velocity,
                        "unobserved_motion_distance_m": rounded(
                            displacement_m(velocity, elapsed)
                        ),
                    }
                )

    evidenced_coefficients = {
        "static_pair_delta_displacement_mm_per_1_mps": [
            rounded(value) for value in EVIDENCED["static_pair_delta_ms"]
        ],
        "current_period_ms_derived_from_reciprocal_fps": current_periods,
        "wide_threshold_displacement_m_per_1_mps": rounded(
            displacement_m(1.0, EVIDENCED["wide_stale_threshold_ms"])
        ),
    }

    return {
        "schema": "tangra-temporal-sensitivity-v1",
        "claim_boundary": (
            "Deterministic elapsed-time/displacement sensitivity only; not a "
            "physical-error, probability, tracker-policy, or runtime-validation result."
        ),
        "evidenced_inputs": EVIDENCED,
        "synthetic_inputs": SYNTHETIC,
        "derived_from_evidenced_inputs": evidenced_coefficients,
        "synthetic_age_sensitivity": synthetic_age,
        "synthetic_jitter_sensitivity": synthetic_jitter,
        "synthetic_dropout_sensitivity": synthetic_dropout,
    }


def main() -> None:
    output = Path(__file__).with_suffix(".json")
    payload = json.dumps(build(), indent=2, sort_keys=True) + "\n"
    output.write_text(payload, encoding="utf-8")
    print(hashlib.sha256(payload.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
