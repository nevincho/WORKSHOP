# TASK — TANGRA HQ DUAL-STREAM / CALIBRATION-PRESERVING METRIC PATH REVIEW

TASK_ID: TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: COMPLETE
OBJECTIVE: Independently determine whether one HQ optical acquisition should expose separate calibration-consistent metric geometry and 640x640 AI geometry without creating a second authoritative tracker/state, and define the smallest safe implementation boundary if later authorized.
SOURCE_PLAN_OR_REQUEST: Explicit owner request dated 2026-09-08.
CURRENT_STATE: COMPLETE for research/design review only; Reviewer PASS. Architecture verdict: VIABLE_WITH_CONDITIONS. VERIFIED from prior WORKSHOP evidence: active application requests Picamera2 main BGR888 640x640; Hailo input is 640x640; no explicit application ROI/letterbox/sensor-mode crop was found in the traced path; current metric focal scaling assumes 2028x1520 calibration maps directly to runtime 640x640. Actual selected sensor/readout/ScalerCrop geometry remains NOT VERIFIED. The accepted design boundary is one camera acquisition authority, one protected detection/tracking/CurrentTarget authority, explicit calibration↔AI transform provenance, and a metric projection adapter; no second tracker/capture authority is justified.
PREREQUISITES: Satisfied for design review from prior completed HQ geometry forensic review, prior multi-rate research, and current Picamera2/libcamera documentation.
DEPENDENCIES: No implementation dependency. Any future production work depends on direct Picamera2/libcamera geometry probe and performance benchmark.
AFFECTED_COMPONENTS: HQ camera acquisition/configuration; image-transform provenance; Hailo preprocessing; bbox coordinate mapping; NanoTracker/CA frame provenance; CurrentTarget association; class-size range; HOROS LOS_RANGE ingress; buffers/timestamps.
PROTECTED_COMPONENTS: HQ physical calibration; Hailo model/input contract; NanoTracker authority; CA Kalman authority; CurrentTargetManager authority; HOROS estimator authority; production runtime/config; command/actuation.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: PASS. A-L design review produced; VERIFIED/INFERRED/NOT_VERIFIED/RECOMMENDATION classifications provided; current pipeline, dual-stream topology, contracts, frame/timestamp identity, memory/copy analysis, range/HOROS integration, failure modes, code touchpoints, minimum plan, validation plan, risks, and verdict are recorded. No implementation or runtime action occurred.
VALIDATION_METHOD: Prior WORKSHOP forensic evidence + TANGRA-DOCS context + current Picamera2/libcamera multi-stream/request documentation + independent adversarial Reviewer PASS.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908/RESEARCH.md
- review/TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908.md

## HARD CONSTRAINTS CONFIRMED
- No implementation/runtime action.
- No calibration/refocus/model/tracker/CA/CurrentTarget/HOROS authority changes.
- No second authoritative target state.
- No duplicate Picamera2 capture loop proposed as default.
- >25 FPS remains mandatory for any future implementation validation.
