# TASK — TANGRA HQ 640x640 CAPTURE GEOMETRY FORENSIC REVIEW

TASK_ID: TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: COMPLETE
OBJECTIVE: Determine, read-only, whether TANGRA may be incorrectly treating 640x640 detector geometry as camera acquisition geometry, invalidating the current scaling of HQ calibration intrinsics and contributing to the observed ~2.1x monocular under-range.
SOURCE_PLAN_OR_REQUEST: Explicit owner request dated 2026-09-07; owner authorization is limited to repository-safe forensic analysis. TANGRA runtime/Pi5 remains OFFLINE_HOLD and was not probed.
CURRENT_STATE: REVIEWER PASS. The hypothesis is STRENGTHENED / MATHEMATICALLY CONSISTENT / NOT VERIFIED. VERIFIED code evidence shows 640x640 is both Picamera2 main-stream request and Hailo canonical input, but current evidence does not establish the actual sensor/readout/ScalerCrop/ISP field feeding that stream. Official Picamera2/libcamera behavior confirms stream size and sensor/crop geometry are distinct. Object2 requires ~2.10-2.15x effective focal/image scale relative to current K scaling, quantitatively compatible with a materially narrower upstream field but not proof of any specific crop. One read-only metadata probe is required to resolve the leading hypotheses.
PREREQUISITES: Satisfied for repository-safe forensic analysis from owner-supplied code trace, prior completed forensic tasks, exact arithmetic, and current official Picamera2/libcamera documentation.
DEPENDENCIES: Prior TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907 and TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907 evidence.
AFFECTED_COMPONENTS: HQ Picamera2 capture geometry assumptions; sensor-mode/crop/scaler interpretation; Hailo input geometry; monocular range intrinsics provenance.
PROTECTED_COMPONENTS: HQ calibration values; detector input size; class-size profiles; NanoTracker/CA Kalman; HOROS; production runtime/config; Pi5 runtime.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: PASS. Adversarial refutation attempted; code evidence and quantitative compatibility classified; alternatives ranked; missing evidence explicit; one decisive Picamera2/libcamera probe specified. No correction factor, recalibration, detector-size change, class-size change, or runtime modification.
VALIDATION_METHOD: Repository-safe forensic reasoning against owner-supplied implementation trace, prior WORKSHOP evidence, exact range arithmetic, and current official Raspberry Pi/libcamera documentation. No physical/runtime validation claimed.
PRE_CHANGE_CHECKPOINT: N/A — no target implementation change.
ROLLBACK_METHOD: N/A — no target implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907/SCOUT.md
- review/TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907.md

## REVIEWER VERDICT
PASS.

## PROTECTED COMPONENT STATUS
NO VIOLATION.

## CODEX STATUS
NOT INVOKED.

## RUNTIME STATUS
NOT VERIFIED / NOT PROBED.