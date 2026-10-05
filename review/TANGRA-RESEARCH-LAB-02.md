# TANGRA-RESEARCH-LAB-02 — Independent Review

TASK_ID: TANGRA-RESEARCH-LAB-02

DATE: 2026-10-05

ROLE: INDEPENDENT REVIEWER

WORKER_COMMIT_REVIEWED: `b2f9d0f`

VERDICT: PASS

CURRENT_STATUS: COMPLETE / INDEPENDENT_REVIEW_PASS

TANGRA_CHANGED: NO

PI_OR_RUNTIME_ACCESSED: NO

CODEX_USED: NO

## Review method

The Reviewer independently inspected the canonical task, Worker diff and retained source evidence; re-ran the deterministic calculation artifact; verified its output hash and a separate set of arithmetic assertions; sampled provenance, processing-domain and frame claims against the cited exact-ref/retained evidence; challenged ground-truth independence, uncertainty logic and claim scope; and inspected repository hygiene and the protected read-only boundary.

The exact qualified documentation ref remains `nevincho/TANGRA-DOCS@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba`. The Worker records exact source paths plus blob identities for the two principal target reports. Fresh production source/runtime was not accessed and remains `NOT VERIFIED`.

## Independent calculation checks

Command re-run:

`python3 evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.py`

Observed output hash: `bd4920496dcd236b6ceb20cfacbf4cfe4500a505204436ac5799e187da4a0546`.

Artifact hashes independently confirmed:

- script: `11facaeefa8f19f932a05958b0ee5d41b208cfb686308277c99427380c71e4ee`;
- JSON: `bd4920496dcd236b6ceb20cfacbf4cfe4500a505204436ac5799e187da4a0546`.

Independent assertions recomputed the 0.006 m residual, 0.137614679% truth-relative residual, 40.632157581% reported-uncertainty ratio, every profile scale/ratio, every one-factor inverse-bbox ratio and all timing coefficients. All matched the JSON within rounding tolerance.

The first-order equation is correct for the stated model:

`R = sqrt((fx W / pw)(fy H / ph))`

therefore

`dR/R = 0.5(dfx/fx + dfy/fy + dW/W + dH/H - dpw/pw - dph/ph)`.

The LOS probe correctly uses the provisional 2028×1520 calibration-plane focal lengths. The report explicitly prevents those pixel sensitivities from being transferred to the 640×640 AI plane until the composed calibration-to-AI transform is evidenced.

## Evidence and methodology findings

| Review question | Independent result |
|---|---|
| Numerical provenance | PASS. Evidenced constants, derived quantities and synthetic perturbation grids are separated. No probability distribution is invented. |
| Bbox domains | PASS. The invalid 2028×1520-manual-bbox/640×640-live-estimator crossing is identified, excluded and not used for qualification. The actual forward transform remains `NOT VERIFIED`. |
| Coordinate frames | PASS. Range-only, calibration-plane LOS, camera-frame, cross-camera and world/LOCAL_ENU claims remain distinct. |
| Ground-truth independence | PASS with explicit limitation. The 4.36 m physical measurement is methodologically independent of the estimator, but its instrument/procedure uncertainty is absent. The 4.366 m estimate, 1.774 m estimator uncertainty and downstream HOROS reuse are not treated as independent truth. |
| Uncertainty logic | PASS. The output is a deterministic sensitivity budget, not covariance or confidence coverage. Missing correlations, transform, pose, time, semantic extent and measurement-truth uncertainty stay visible and unbounded. |
| Claim scope | PASS. One near-field point is not promoted to a range curve, live LOS, stereo accuracy or world-position validation. |
| Experiments | PASS. The minimum experiment set targets the actual missing prerequisites and includes measurable falsification criteria without prescribing production changes. |
| Protected boundary | PASS. The reviewed commit changes only WORKSHOP task/evidence/review-request artifacts. No target repository, Pi/runtime, firmware, model, service or configuration mutation occurred. |
| Hygiene | PASS. One canonical Worker report, one reproducible script, one generated JSON result and one review request are justified; no disposable duplicate or temporary artifact was found. |

## Important interpretation boundary

This PASS validates the evidence classification, deterministic sensitivity calculations and proposed closure experiments. It does **not** establish:

- current production/runtime identity;
- an operational range-error curve;
- calibrated estimator uncertainty coverage;
- the live calibration-to-AI transform;
- final HQ-to-WIDE extrinsics;
- moving-target temporal alignment;
- carrier pose or LOCAL_ENU/world-position accuracy.

The reported 0.006 m residual therefore remains a single recorded near-field observation. Its small magnitude cannot falsify the much larger unresolved systematic terms. Conversely, absence of the missing evidence is not evidence that the corresponding components fail.

## Acceptance decision

All ten canonical acceptance criteria pass. No rework is required. The next campaign unit may proceed only after this review checkpoint is recorded and Control Room recomputes dependencies.

FINAL_VERDICT: PASS

REWORK_LOOPS: 0

TANGRA_MODIFIED: NO
