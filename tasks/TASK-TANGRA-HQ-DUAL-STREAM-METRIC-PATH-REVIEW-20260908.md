# TASK — TANGRA HQ DUAL-STREAM / CALIBRATION-PRESERVING METRIC PATH REVIEW

TASK_ID: TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: COMPLETE
OBJECTIVE: Independently determine whether one HQ optical acquisition should expose separate calibration-consistent metric geometry and 640x640 AI geometry without creating a second authoritative tracker/state, and define the smallest safe implementation boundary if later authorized.
SOURCE_PLAN_OR_REQUEST: Explicit owner request dated 2026-09-08, plus live/physical addendum dated 2026-09-08.
CURRENT_STATE: COMPLETE for research/design review only; Reviewer PASS. Architecture verdict remains VIABLE_WITH_CONDITIONS. VERIFIED from prior WORKSHOP evidence: active application requests Picamera2 main BGR888 640x640; Hailo input is 640x640; no explicit application ROI/letterbox/sensor-mode crop was found in the traced path; current metric focal scaling assumes 2028x1520 calibration maps directly to runtime 640x640. New live evidence confirms telemetry still reports HQ processing at 640x640, while the attempted read-only HQ snapshot route returns HTTP 404; this is an observability limitation, not camera failure. Actual selected sensor/readout/ScalerCrop geometry therefore remains NOT VERIFIED. New physical evidence also establishes that E88 has variable free-moving propeller silhouette and can be classified as FPV/Orlan-10/Talay in the same general scene, so class-prior provenance and silhouette variability must be validated separately from camera geometry. The accepted design boundary remains one camera acquisition authority, one protected detection/tracking/CurrentTarget authority, explicit calibration↔AI transform provenance, frame/timestamp identity, inverse object-geometry projection, and metric/class provenance; no second tracker/capture authority is justified.
PREREQUISITES: Satisfied for design review from prior completed HQ geometry forensic review, prior multi-rate research, current Picamera2/libcamera documentation, and owner-supplied live/physical observations.
DEPENDENCIES: No implementation dependency. Any future production work depends on direct Picamera2/libcamera geometry probe, explicit range-class provenance trace, isolated validation domains, and performance benchmark.
AFFECTED_COMPONENTS: HQ camera acquisition/configuration; image-transform provenance; Hailo preprocessing; bbox coordinate mapping; NanoTracker/CA frame provenance; CurrentTarget association; class-size range/class provenance; HOROS LOS_RANGE ingress; buffers/timestamps.
PROTECTED_COMPONENTS: HQ physical calibration; Hailo model/input contract; NanoTracker authority; CA Kalman authority; CurrentTargetManager authority; HOROS estimator authority; production runtime/config; command/actuation; production class profiles.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: PASS. A-L design review produced; VERIFIED/INFERRED/NOT_VERIFIED/RECOMMENDATION classifications provided; current pipeline, dual-stream topology, contracts, frame/timestamp identity, memory/copy analysis, range/HOROS integration, failure modes, code touchpoints, minimum plan, validation plan, risks, and verdict are recorded. Live/physical addendum is incorporated without conflating camera geometry, coordinate transform, class prior, silhouette variability, frame identity, and performance into one metric PASS/FAIL. No implementation or runtime modification occurred.
VALIDATION_METHOD: Prior WORKSHOP forensic evidence + TANGRA-DOCS context + current Picamera2/libcamera multi-stream/request documentation + owner-supplied live/physical observations + independent adversarial Reviewer PASS.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908/RESEARCH.md
- evidence/TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908/LIVE_PHYSICAL_ADDENDUM_2026-09-08.md
- review/TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908.md

## HARD CONSTRAINTS CONFIRMED
- No implementation/runtime modification.
- No calibration/refocus/model/tracker/CA/CurrentTarget/HOROS authority changes.
- No production class-profile changes.
- No second authoritative target state.
- No duplicate Picamera2 capture loop proposed as default.
- Geometry outside the AI-observable region must not be invented.
- >25 FPS remains mandatory for any future implementation validation.
