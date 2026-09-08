# TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908

TASK_ID: TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Standalone passive SHADOW monocular metric-range source from TASK 1 sparse geometry after TASK 2 calibrated-plane mapping, with explicit physical-span correspondences, robust multi-span fusion, uncertainty and provenance.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room TASK 3, 2026-09-08.
CURRENT_STATE: Implementation/tests/evidence complete; submitted for bounded review. Production metric usability remains NOT_VERIFIED because production TASK 2 transform A remains NOT_VERIFIED and no production sparse-point physical-span correspondence was proven from repository evidence.
PREREQUISITES: TASK 1 frozen commit c7b378841979f82b037c47be3571fa72a7b70e51; TASK 2 frozen commit 4bd4b5d38357db501de07511aeabaa4c0ae058e1.
DEPENDENCIES: Python 3, NumPy, standard dataclasses/enum/statistics/math/time/typing.
AFFECTED_COMPONENTS: Standalone TASK 3 handoff/evidence/review artifacts only.
PROTECTED_COMPONENTS: TASK 1, TASK 2, HQ acquisition, primary detector, NanoTracker, CA Kalman, CurrentTargetManager, existing range estimator, HOROS authoritative estimator, Guidance, Dashboard, command paths.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: explicit physical-span contract; no fabricated production dimensions/correspondence; calibrated anisotropic geometry; orientation gate; candidate evidence; robust group-aware outlier rejection; insufficient/disagreement fail-closed; uncertainty propagation; TASK 1/2 compatibility; production NOT_VERIFIED gate; shadow existing-range comparison; deterministic tests; host microbenchmark.
VALIDATION_METHOD: deterministic Python unittest + standalone coordinate/range benchmark. All physical ground-truth evidence is explicitly SYNTHETIC.
PRE_CHANGE_CHECKPOINT: WORKSHOP main 51faa24190deaf53d22d5253912c38cfd155384e.
ROLLBACK_METHOD: revert TASK 3 implementation/review commits; no production runtime modified.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/; handoffs/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/; review/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908.md.
