# TASK — TANGRA MULTI-RATE PIPELINE / PERFORMANCE HEADROOM RESEARCH

TASK_ID: TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Independently research and review whether TANGRA can safely use a multi-rate pipeline in which expensive modules run at the minimum useful cadence while authoritative tracking/spatial quality, freshness, and end-to-end responsiveness are preserved.
SOURCE_PLAN_OR_REQUEST: Owner request dated 2026-09-07. Source idea: TANGRA-DOCS/IDEAS/HQ_CALIBRATED_STREAM_AND_ADAPTIVE_INFERENCE_CADENCE_2026-09-07.md.
CURRENT_STATE: COMPLETE FOR RESEARCH ONLY / Reviewer PASS. Source idea remains NOT IMPLEMENTED. General multi-rate detector+tracker architecture is externally established and suitable for TANGRA experimentation, but TANGRA-specific safe detector cadence, adaptive scheduler policy, compound headroom, WIDE/HOROS cadence and production architecture remain NOT VERIFIED until benchmarked. Geometry-correctness probe remains the first gate before any HQ acquisition architecture implementation.
PREREQUISITES: Satisfied for research. Source idea and prior HQ geometry forensic evidence reviewed; current established multi-rate detector/tracker, adaptive scheduling, asynchronous inference, and bounded-latest-frame queue references included.
DEPENDENCIES: No implementation dependency. Geometry-correctness probe remains prerequisite for later HQ acquisition implementation/performance campaign.
AFFECTED_COMPONENTS: HQ acquisition, Hailo detector, NanoTracker, CA Kalman, CurrentTargetManager, range estimation, HOROS, WIDE processing, Dashboard, telemetry/radio, logging/dataset/diagnostics.
PROTECTED_COMPONENTS: NanoTracker algorithm; CA Kalman; validated authoritative chains; CurrentTarget authority; production detector/model; HQ calibration; command/actuation; runtime/config.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: PASS. A-K research output recorded; fixed/adaptive cadence reviewed; module cadence matrix and opportunity/risk ranking produced; bounded latest-frame/freshness requirements defined; benchmark and acceptance logic defined; no unverified numeric headroom claim made.
VALIDATION_METHOD: Cross-check of TANGRA source idea/prior forensic evidence against NVIDIA DeepStream tracking/inference-interval documentation, GStreamer bounded/leaky queue documentation, HailoRT async inference examples, and published adaptive detect-vs-track/frame-skipping research. Independent Reviewer PASS recorded.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907/RESEARCH.md
- review/TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907.md

## FINAL RESEARCH VERDICT
- Multi-rate architecture direction: RESEARCH-SUPPORTED / STRENGTHENED.
- Fixed N=1..6 sweep: APPROPRIATE FIRST CHARACTERIZATION TEST.
- Adaptive detector scheduling: RESEARCH-SUPPORTED FOLLOW-UP / REQUIRES TEST.
- Bounded latest-frame semantics with timestamps/freshness: REQUIRED DESIGN INVARIANT for any async experiment.
- Production-safe cadences/headroom: NOT VERIFIED.

## Hard constraints preserved
- No implementation or production changes.
- No calibration/model/NanoTracker/CA changes.
- No unbounded queues or stale-frame backlog recommendation.
- No average-FPS-only acceptance.
- No Codex or Pi5/runtime action.
