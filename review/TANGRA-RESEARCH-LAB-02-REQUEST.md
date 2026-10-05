# TANGRA-RESEARCH-LAB-02 — Independent Review Request

TASK_ID: TANGRA-RESEARCH-LAB-02

FROM_ROLE: WORKER

TO_ROLE: INDEPENDENT REVIEWER

STATUS: REVIEW_REQUESTED

WORKER_EVIDENCE: `evidence/TANGRA-RESEARCH-LAB-02/WORKER.md`

CALCULATION_ARTIFACTS:
- `evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.py`
- `evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.json`

## Required independent checks

1. Verify every evidenced number against exact qualified source/ref/path and every synthetic perturbation is clearly separated.
2. Re-run the calculation twice; verify deterministic JSON and SHA-256.
3. Independently recompute the 4.36/4.366 residual, FPV profile-only ratios, sample one-factor bbox/focal sensitivities, LOS pixel sensitivity and timestamp displacement coefficients.
4. Challenge the ground-truth audit for circular/self-comparison and incompatible-domain use.
5. Confirm no range-only result is promoted to camera/world/LOCAL_ENU validation.
6. Confirm transform, bbox semantics, target size/pose, extrinsics, carrier pose and time/age gaps remain visible/unbounded.
7. Confirm experiments are minimal, measurable and include falsification/pass-fail conditions.
8. Verify TANGRA repositories/runtime were not modified/accessed for mutation and WORKSHOP hygiene passes.

## Worker hashes

- Python: `11facaeefa8f19f932a05958b0ee5d41b208cfb686308277c99427380c71e4ee`
- JSON: `bd4920496dcd236b6ceb20cfacbf4cfe4500a505204436ac5799e187da4a0546`

## Requested verdict

`PASS`, `REWORK`, `BLOCKED`, or `NOT VERIFIED` with the smallest evidence-based correction if needed. Worker makes no PASS claim.
