# TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908 — Independent Review

## Cycle 1
REVIEW_RESULT: PASS_WITH_CONDITIONS
COMMIT_REVIEWED: 1cd2e641f4387aa190071839d763bb2b9732dc1f
DEFECT_1: candidate evidence exposed normalized calibrated span but not explicit calibrated pixel span required for candidate-level evidence.
REQUIRED_CORRECTION_1: add `calibrated_length_px` without changing range mathematics.
DEFECT_2: candidate provenance did not directly carry source geometry/calibration/transform identity.
REQUIRED_CORRECTION_2: carry `source_geometry_ref`, `calibration_id`, `transform_id`, and `transform_version` at candidate level.

## Cycle 2 / Final
REVIEW_RESULT: PASS
COMMIT_REVIEWED: c121ce25dbba84520c6f8e644281a7cb2bf3ee73

### Verification
- Monocular span mathematics is consistent with anisotropic calibrated focal geometry: `q=sqrt((du/fx)^2+(dv/fy)^2)`, with `Z=S*r/q` only for explicit physical correspondence and explicit orientation projection factor.
- Candidate evidence now preserves both calibrated pixel length and normalized calibrated span.
- Physical spans require explicit correspondence verification, uncertainty, provenance, and independence group; no production dimensions are fabricated.
- Near-top-down / mild-oblique limitation is explicit; orientation projection is supplied evidence and is not inferred as general 6DoF pose.
- Independence groups prevent correlated candidates multiplying fusion evidence.
- Invalid/non-finite/near-zero candidates are rejected; >=3-group outliers are bounded by robust residual; two-group excessive disagreement fails closed; insufficient independent evidence fails closed.
- Uncertainty includes endpoint/span, physical dimension, orientation, calibration and transform relative-scale terms plus a floor against false precision.
- TASK 1 invalid/null NOSE/TAIL semantics remain unusable and propagate fail-closed.
- TASK 2 transform validity is required; production metric verification additionally requires transform, profile and calibration production-verification gates.
- Nonzero distortion fails closed unless calibrated points are declared undistorted.
- Existing MONOCULAR_CLASS_SIZE comparison remains passive/external and does not modify or replace the production estimator; no superiority claim.
- Exact validated implementation/test blobs match the reviewed commit artifacts. Complete corrected suite: 18/18 PASS.
- Corrected host-only benchmark: n=50,000; mean 0.06209089742 ms; median 0.053601 ms; p95 0.090216 ms; max 22.973591 ms. Max is a single host scheduling/outlier observation; Pi5/end-to-end performance NOT_VERIFIED.
- Diff from pre-TASK3 checkpoint contains only TASK 3 task/handoff/evidence/review files. TASK 1, TASK 2 and all protected runtime authorities remain unchanged.

DECISION: PASS
TASK3_COMPLETE: YES
FROZEN_REVIEWED_COMMIT: c121ce25dbba84520c6f8e644281a7cb2bf3ee73
PRODUCTION_METRIC_STATUS: NOT_VERIFIED
BLOCKER: NONE for standalone TASK 3 completion. Production use remains gated on verified live TASK 2 transform, verified physical target-span correspondence/profile, and physical metric validation.
