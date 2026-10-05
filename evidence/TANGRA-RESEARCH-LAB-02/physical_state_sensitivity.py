#!/usr/bin/env python3
"""Deterministic, distribution-free sensitivity calculations for JOB-02.

This does not model production.  Evidenced constants and explicitly synthetic
perturbation grids are separated in the JSON output.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


EVIDENCED = {
    "hq_calibration": {
        "width_px": 2028,
        "height_px": 1520,
        "fx_px": 15756.86,
        "fy_px": 15848.54,
        "cx_px": 1014.0,
        "cy_px": 760.0,
        "reprojection_rms_px": 1.239,
        "status": "PROVISIONAL_PASS",
    },
    "physical_point": {
        "truth_m": 4.36,
        "estimate_m": 4.366,
        "reported_uncertainty_m": 1.774,
        "focus_m": 4.0,
        "scope": "single near-field point",
    },
    "fpv_profiles_m": [
        [0.20, 0.25],
        [0.30, 0.30],
        [0.40, 0.40],
        [0.50, 0.50],
        [0.60, 0.60],
    ],
    "paired_sensor_delta_ms": [4.807, 44.751, 50.691],
    "camera_baseline_m": 0.0356,
}

SYNTHETIC = {
    "relative_perturbation_pct": [-10, -5, -2, -1, 0, 1, 2, 5, 10],
    "calibration_plane_pixel_offsets": [1, 2, 5, 10],
    "motion_normalization_mps": 1.0,
    "note": "Sensitivity probes only; not TANGRA uncertainty distributions.",
}


def rounded(value: float, digits: int = 9) -> float:
    return round(value, digits)


def main() -> None:
    point = EVIDENCED["physical_point"]
    truth = point["truth_m"]
    estimate = point["estimate_m"]

    one_factor = []
    for pct in SYNTHETIC["relative_perturbation_pct"]:
        q = pct / 100.0
        one_factor.append(
            {
                "perturbation_pct": pct,
                "focal_or_size_range_ratio": rounded(1.0 + q),
                "bbox_range_ratio": rounded(1.0 / (1.0 + q)),
                "focal_or_size_delta_at_4_366_m": rounded(estimate * q),
                "bbox_delta_at_4_366_m": rounded(estimate / (1.0 + q) - estimate),
            }
        )

    profile_scales = [math.sqrt(w * h) for w, h in EVIDENCED["fpv_profiles_m"]]
    mean_scale = sum(profile_scales) / len(profile_scales)
    profile_ratios = [x / mean_scale for x in profile_scales]
    profile_ranges = [estimate * x for x in profile_ratios]

    fx = EVIDENCED["hq_calibration"]["fx_px"]
    fy = EVIDENCED["hq_calibration"]["fy_px"]
    los = []
    for px in SYNTHETIC["calibration_plane_pixel_offsets"]:
        ax = math.atan(px / fx)
        ay = math.atan(px / fy)
        los.append(
            {
                "offset_px": px,
                "horizontal_angle_mrad": rounded(ax * 1000),
                "vertical_angle_mrad": rounded(ay * 1000),
                "horizontal_cross_range_mm_at_4_366_m": rounded(estimate * math.tan(ax) * 1000),
                "vertical_cross_range_mm_at_4_366_m": rounded(estimate * math.tan(ay) * 1000),
            }
        )

    motion = []
    for delta_ms in EVIDENCED["paired_sensor_delta_ms"]:
        motion.append(
            {
                "sensor_delta_ms": delta_ms,
                "displacement_mm_per_1_mps": rounded(delta_ms),
            }
        )

    output = {
        "schema": "TANGRA_RESEARCH_LAB_02_PHYSICAL_SENSITIVITY_V1",
        "method": "deterministic algebraic sweep; no probability distributions; no Monte Carlo",
        "evidenced_inputs": EVIDENCED,
        "synthetic_sensitivity_inputs": SYNTHETIC,
        "single_point": {
            "absolute_residual_m": rounded(abs(estimate - truth)),
            "relative_residual_pct": rounded(abs(estimate - truth) / truth * 100),
            "reported_uncertainty_relative_pct": rounded(point["reported_uncertainty_m"] / estimate * 100),
            "residual_over_reported_uncertainty": rounded(abs(estimate - truth) / point["reported_uncertainty_m"]),
        },
        "monocular_model": {
            "axis_equations": ["Rw=fx*W/bbox_w", "Rh=fy*H/bbox_h"],
            "combined_equation": "R=sqrt(Rw*Rh)",
            "first_order_relative": "dR/R=0.5*(dfx/fx+dfy/fy+dW/W+dH/H-dpw/pw-dph/ph)",
            "one_factor_sweep": one_factor,
        },
        "fpv_profile_only_sensitivity": {
            "geometric_size_scales_m": [rounded(x) for x in profile_scales],
            "equal_weight_mean_scale_m": rounded(mean_scale),
            "range_ratios_to_equal_weight_mean": [rounded(x) for x in profile_ratios],
            "ranges_if_equal_weight_mean_is_4_366_m": [rounded(x) for x in profile_ranges],
            "min_relative_deviation_pct": rounded((min(profile_ratios) - 1) * 100),
            "max_relative_deviation_pct": rounded((max(profile_ratios) - 1) * 100),
            "limitation": "Isolates documented profile hypotheses at fixed bbox/calibration; not a population distribution.",
        },
        "los_pixel_sensitivity": los,
        "pair_timing_motion_coefficient": motion,
        "unbounded_terms": [
            "actual calibration-to-AI forward transform",
            "detector/tracker/range bbox semantic and transform uncertainty",
            "target physical-size truth/distribution and pose/foreshortening",
            "HQ-to-WIDE rotation and translation extrinsics",
            "carrier attitude/position uncertainty and LOCAL_ENU transform",
            "source timestamp, processing latency, measurement age and correlation",
        ],
    }

    path = Path(__file__).with_name("physical_state_sensitivity.json")
    payload = json.dumps(output, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8")
    print(hashlib.sha256(payload.encode("utf-8")).hexdigest(), path.name)


if __name__ == "__main__":
    main()
