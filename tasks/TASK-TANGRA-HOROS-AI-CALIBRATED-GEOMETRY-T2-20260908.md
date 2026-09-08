# TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908

TASK_ID: TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Prepare a standalone coordinate-only adapter mapping HQ AI-plane geometry back into a calibrated HQ image plane through an explicit invertible transform contract.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room TASK 2, 2026-09-08.
CURRENT_STATE: COMPLETE after independent review cycle. Final reviewed implementation commit: 4bd4b5d38357db501de07511aeabaa4c0ae058e1. Production HQ CAL->AI transform remains NOT_VERIFIED and must not be fabricated during future integration.
PREREQUISITES: TASK 1 geometry-equivalent bbox/center/sparse points plus explicit transform configuration.
DEPENDENCIES: Python 3, NumPy, standard dataclasses/typing/math.
AFFECTED_COMPONENTS: Standalone TASK 2 handoff only; no runtime integration.
PROTECTED_COMPONENTS: TASK 1, HQ acquisition, primary detector, NanoTracker, CA Kalman, CurrentTargetManager, range estimator, HOROS authoritative estimator, Guidance, Dashboard, command paths.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: PASS — explicit invertible CAL->AI transform; deterministic AI->CAL inverse; crop/resize/padding fixtures; explicit pixel-center convention; bbox/point/null handling; K consistency; fail-closed malformed transform; bounded microbenchmark; no fabricated production transform.
VALIDATION_METHOD: deterministic Python unittest + coordinate-only microbenchmark; 12/12 PASS after correction cycle 1.
PRE_CHANGE_CHECKPOINT: WORKSHOP main c7b378841979f82b037c47be3571fa72a7b70e51.
ROLLBACK_METHOD: revert TASK 2 implementation/review commits; no target runtime modified.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908/; handoffs/TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908/; review/TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908.md.
FROZEN_REVIEWED_COMMIT: 4bd4b5d38357db501de07511aeabaa4c0ae058e1
