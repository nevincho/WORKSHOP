# TASK — TANGRA AI GEOMETRY → CALIBRATED HQ GEOMETRY REVIEW

TASK_ID: TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: REVIEW
OBJECTIVE: Independently determine whether TANGRA can recover metrically correct object geometry in the 2028x1520 HQ calibration coordinate system by mathematically inverting the deterministic transform applied to the 640x640 AI representation, without reconstructing or retaining a separate full-resolution metric image stream.
SOURCE_PLAN_OR_REQUEST: Explicit owner request dated 2026-09-08.
CURRENT_STATE: VERIFIED from prior WORKSHOP evidence: HQ calibration space is 2028x1520 with fx=15756.86, fy=15848.54, cx=1014, cy=760, D=[0,0,0,0,0]; runtime AI geometry is 640x640; protected authority remains HQ->Hailo->NanoTracker->CA Kalman->CurrentTargetManager->range evidence->HOROS. Prior forensic trace shows application requests Picamera2 main 640x640 and Hailo input 640x640, but actual sensor mode / ScalerCrop / upstream optical transform remains NOT VERIFIED. Therefore the general mathematics can be reviewed, but the exact live forward matrix cannot yet be claimed VERIFIED.
PREREQUISITES: Prior completed HQ 640x640 geometry forensic review; prior dual-stream metric-path architecture review; current libcamera ScalerCrop semantics; owner-supplied calibration values.
DEPENDENCIES: Future implementation requires direct capture-geometry probe establishing the exact forward transform from calibrated optical field to AI frame.
AFFECTED_COMPONENTS: camera geometry provenance; AI preprocessing transform; bbox/keypoint mapping; range_estimator.py; target_profiles.py; CurrentTargetManager integration contract; HOROS LOS_RANGE ingress.
PROTECTED_COMPONENTS: HQ physical calibration; Hailo model/input contract; NanoTracker authority; CA Kalman authority; CurrentTargetManager authority; HOROS estimator authority; production runtime/config; class-size profiles.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: Produce A-N design review; derive affine/projective coordinate mappings for resize/crop/letterbox cases; prove equivalence of back-projecting geometry to calibrated coordinates with original K versus retaining AI geometry with transformed K; define validity limits, clipping rules, error budget, range/HOROS integration, minimum code boundary, validation plan, and comparison against separate metric stream. Explicit VERIFIED/INFERRED/NOT_VERIFIED/RECOMMENDATION classifications. No implementation.
VALIDATION_METHOD: Analytical derivation, synthetic round-trip proof case, cross-check against prior WORKSHOP evidence and current libcamera geometry semantics, independent reviewer adversarial check.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908/RESEARCH.md
- review/TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908.md

## HARD CONSTRAINTS
- RESEARCH + FORENSIC DESIGN REVIEW ONLY.
- No implementation or production/runtime action.
- No calibration change, refocus, correction factor, class-size modification, tracker/CA/CurrentTarget/HOROS authority change.
- Do not invent geometry outside the AI-visible region.
- Coordinate reconstruction is permitted conceptually; pixel/image reconstruction is not required.
- Exact live transform remains NOT VERIFIED until sensor/crop/resize metadata is captured.