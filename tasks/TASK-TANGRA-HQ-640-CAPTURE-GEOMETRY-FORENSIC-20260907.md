# TASK — TANGRA HQ 640x640 CAPTURE GEOMETRY FORENSIC REVIEW

TASK_ID: TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: REVIEW
OBJECTIVE: Determine, read-only, whether TANGRA may be incorrectly treating 640x640 detector geometry as camera acquisition geometry, invalidating the current scaling of HQ calibration intrinsics and contributing to the observed ~2.1x monocular under-range.
SOURCE_PLAN_OR_REQUEST: Explicit owner request dated 2026-09-07; owner authorization is limited to repository-safe forensic analysis. TANGRA runtime/Pi5 remains OFFLINE_HOLD and is not to be probed in this task.
CURRENT_STATE: VERIFIED owner-supplied code trace: FRAME_WIDTH/HEIGHT=640; CAMERA_RESOLUTION=(FRAME_WIDTH,FRAME_HEIGHT); HAILO_INPUT_SIZE=(640,640); CameraStream requests Picamera2 BGR888 main size 640x640; Hailo cv2.resize to 640x640; no explicit sensor mode/ScalerCrop/crop/binning configured in the traced application path. HQ calibration is 2028x1520 with fx=15756.86, fy=15848.54; current runtime uses fx640=fx*640/2028 and fy640=fy*640/1520. Physical evidence includes E88 ~46% under-range and second object ~1.20-1.23m at true 2.585m.
PREREQUISITES: Owner-supplied code trace; prior completed forensic tasks TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907 and TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907; current official Picamera2/libcamera documentation for sensor configuration and ScalerCrop semantics.
DEPENDENCIES: Prior forensic evidence only; no runtime access required.
AFFECTED_COMPONENTS: HQ Picamera2 capture geometry assumptions; sensor-mode/crop/scaler interpretation; Hailo input geometry; monocular range intrinsics provenance.
PROTECTED_COMPONENTS: HQ calibration values; detector input size; class-size profiles; NanoTracker/CA Kalman; HOROS; production runtime/config; Pi5 runtime.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: Adversarially try to refute the hypothesis; classify code evidence and quantitative compatibility; rank alternatives; identify what is and is not verified; specify one decisive Picamera2/libcamera probe with exact fields. No correction factor, recalibration, detector-size change, class-size change, or runtime modification.
VALIDATION_METHOD: Repository-safe forensic reasoning against owner-supplied implementation trace, prior WORKSHOP evidence, exact range arithmetic, and current official Raspberry Pi/libcamera documentation. No physical/runtime validation is claimed.
PRE_CHANGE_CHECKPOINT: N/A — no target implementation change.
ROLLBACK_METHOD: N/A — no target implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907/SCOUT.md
- review/TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907.md

## REQUIRED OUTPUT
HYPOTHESIS_VERDICT
CODE_EVIDENCE
QUANTITATIVE_COMPATIBILITY
ALTERNATIVES_RANKED
MISSING_EVIDENCE
DECISIVE_PROBE
STOP

## HARD CONSTRAINTS
- READ-ONLY.
- No runtime/Pi5 probe in this task.
- No code changes.
- No calibration changes.
- No empirical correction constants.
- Do not recommend changing 640x640 detector input.
- Do not infer sensor crop/ROI until metadata proves it.
- Use VERIFIED / MATHEMATICALLY CONSISTENT / STRENGTHENED / WEAKENED / REFUTED / NOT VERIFIED explicitly.