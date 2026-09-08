# TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908

TASK_ID: TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Prepare a standalone coordinate-only adapter mapping HQ AI-plane geometry back into a calibrated HQ image plane through an explicit invertible transform contract.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room TASK 2, 2026-09-08.
CURRENT_STATE: TASK 1 frozen COMPLETE at c7b378841979f82b037c47be3571fa72a7b70e51. Available WORKSHOP/TANGRA-DOCS search did not prove the exact live HQ preprocessing chain from calibrated 2028x1520 geometry to the 640x640 AI plane; production transform A is therefore NOT_VERIFIED.
PREREQUISITES: TASK 1 geometry-equivalent bbox/center/sparse points plus explicit transform configuration.
DEPENDENCIES: Python 3, NumPy, standard dataclasses/typing/math.
AFFECTED_COMPONENTS: Standalone TASK 2 handoff only; no runtime integration.
PROTECTED_COMPONENTS: TASK 1, HQ acquisition, primary detector, NanoTracker, CA Kalman, CurrentTargetManager, range estimator, HOROS authoritative estimator, Guidance, Dashboard, command paths.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: explicit invertible CAL->AI transform; deterministic AI->CAL inverse; crop/resize/padding fixtures; pixel convention; bbox/point/null handling; K consistency; fail-closed malformed transform; microbenchmark; no fabricated production transform.
VALIDATION_METHOD: deterministic Python unittest + coordinate-only microbenchmark.
PRE_CHANGE_CHECKPOINT: WORKSHOP main c7b378841979f82b037c47be3571fa72a7b70e51.
ROLLBACK_METHOD: revert this dedicated TASK 2 commit; no target runtime modified.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908/; handoffs/TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908/.
