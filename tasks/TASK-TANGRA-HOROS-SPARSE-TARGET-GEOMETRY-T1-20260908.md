# TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908

TASK_ID: TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Prepare and validate a standalone passive ROI-only sparse target geometry candidate producing 5 semantic image-space points without range, calibrated mapping, tracking authority, or production integration.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room initialization, 2026-09-08.
CURRENT_STATE: VERIFIED documentation inventory identifies production `main.py`, `tracker_numpy.KalmanTracker`, `CurrentTargetManager`, `horos_shadow_runtime.py`; exact current local source bodies and insertion point are NOT VERIFIED from GitHub because implementation authority is local.
PREREQUISITES: Existing HQ frame + authoritative detector bbox/class/confidence; NumPy; OpenCV. No metric transform required for TASK 1.
DEPENDENCIES: numpy, opencv-python/cv2, Python dataclasses/enum/time.
AFFECTED_COMPONENTS: Standalone candidate only; future integration adapter NOT IMPLEMENTED.
PROTECTED_COMPONENTS: HQ acquisition, primary detector, NanoTracker, tracker_numpy CA Kalman, CurrentTargetManager, range_estimator, HOROS authoritative state, guidance, dashboard, command paths.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: deterministic ROI-only 5-point typed observation; ambiguity handling; bounded synthetic tests; actual per-target benchmark; no upstream mutation; no range/calibration/guidance/production changes.
VALIDATION_METHOD: Python unittest synthetic fixtures + direct microbenchmark of candidate extractor. No physical or Pi5 claims.
PRE_CHANGE_CHECKPOINT: WORKSHOP main faa6822db8395c5e6364c565e281d9b3ade8e277. Target local implementation unchanged.
ROLLBACK_METHOD: Revert this dedicated WORKSHOP package commit; no target runtime/source changed.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908/REPORT.md; evidence/.../benchmark.json; handoffs/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908/.
