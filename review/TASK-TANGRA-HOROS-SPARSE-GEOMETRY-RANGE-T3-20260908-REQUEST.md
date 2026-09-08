# TASK 3 — Independent Review Request

TASK_ID: TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908
STATUS: SUBMITTED_FOR_INDEPENDENT_REVIEW

Review only TASK 3. Frozen inputs TASK 1 `c7b378841979f82b037c47be3571fa72a7b70e51` and TASK 2 `4bd4b5d38357db501de07511aeabaa4c0ae058e1` must not be modified.

Verify:
- monocular geometry mathematics and anisotropic fx/fy handling;
- physical-span correspondence discipline / no fabricated production dimensions;
- near-top-down / mild-oblique assumptions and orientation factor treatment;
- candidate independence groups;
- outlier/disagreement handling and fail-closed behavior;
- uncertainty propagation and false-precision controls;
- TASK 1 null/validity semantics and TASK 2 calibrated geometry compatibility;
- calibration/distortion/transform validation;
- production transform/profile/calibration NOT_VERIFIED gate;
- passive comparison only against existing range source;
- protected architecture boundaries;
- complete tests and benchmark claims.

Return PASS, PASS_WITH_CONDITIONS, or FAIL. For conditions/failures, identify only concrete bounded TASK 3 defects. Do not expand into TASK 4 or production integration.
