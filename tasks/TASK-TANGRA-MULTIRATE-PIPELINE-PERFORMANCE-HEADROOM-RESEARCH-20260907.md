# TASK — TANGRA MULTI-RATE PIPELINE / PERFORMANCE HEADROOM RESEARCH

TASK_ID: TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Independently research and review whether TANGRA can safely use a multi-rate pipeline in which expensive modules run at the minimum useful cadence while authoritative tracking/spatial quality, freshness, and end-to-end responsiveness are preserved.
SOURCE_PLAN_OR_REQUEST: Owner request dated 2026-09-07. Source idea: TANGRA-DOCS/IDEAS/HQ_CALIBRATED_STREAM_AND_ADAPTIVE_INFERENCE_CADENCE_2026-09-07.md.
CURRENT_STATE: Source idea is explicitly IDEA / FUTURE VALIDATION / NOT IMPLEMENTED. It proposes separating calibration-consistent HQ acquisition geometry from 640x640 Hailo inference geometry and evaluating Hailo inference cadence N=1..6. Prior forensic work indicates camera geometry must be proven before any production change. TANGRA runtime remains OFFLINE_HOLD; this task is repository/web research only.
PREREQUISITES: Source idea available; prior HQ geometry forensic evidence available; current established multi-rate detector/tracker, adaptive scheduling, asynchronous inference, and bounded-latest-frame queue references available.
DEPENDENCIES: No implementation dependency. Geometry-correctness probe remains a prerequisite for any later HQ acquisition architecture implementation.
AFFECTED_COMPONENTS: HQ acquisition, Hailo detector, NanoTracker, CA Kalman, CurrentTargetManager, range estimation, HOROS, WIDE processing, Dashboard, telemetry/radio, logging/dataset/diagnostics.
PROTECTED_COMPONENTS: NanoTracker algorithm; CA Kalman; validated authoritative chains; CurrentTarget authority; production detector/model; HQ calibration; command/actuation; runtime/config.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: Produce A-K research output; critically test fixed/adaptive detector cadence; classify module cadences; rank opportunities by expected gain/risk/validation cost; define queue/freshness rules, failure modes, benchmark plan, acceptance logic, compound-headroom reasoning, and experiment order. No implementation or production changes.
VALIDATION_METHOD: Cross-check TANGRA source idea and prior forensic evidence against established industry documentation and published detector/tracker scheduling research. Reviewer must separate evidence-backed principles from TANGRA-specific hypotheses requiring benchmark validation.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907/RESEARCH.md
- review/TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907.md

## Hard constraints
- RESEARCH + FORENSIC DESIGN REVIEW only.
- No implementation, production, calibration, model, tracker, or CA changes.
- No unbounded queues; stale-frame backlog is failure.
- Average FPS alone is insufficient.
- Lower detector Hz is not assumed safe.
- Fixed N is benchmarked before any adaptive policy is considered.
