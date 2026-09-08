# TASK — TANGRA HQ METRIC GEOMETRY ARCHITECTURE DECISION REVIEW

TASK_ID: TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: REVIEW
OBJECTIVE: Compare the already COMPLETE/Reviewer-PASS Task A and Task B results and select the first implementation architecture for HQ metric range/LOS/HOROS without reopening settled findings except where required to resolve contradictions.
SOURCE_PLAN_OR_REQUEST: Explicit owner comparative-review request dated 2026-09-08.
CURRENT_STATE: Task A `TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908` is COMPLETE/Reviewer PASS with verdict VIABLE_WITH_CONDITIONS and live/physical addendum. Task B `TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908` is COMPLETE/Reviewer PASS with verdict VIABLE_WITH_CONDITIONS. Both preserve one HQ acquisition authority and protected Hailo→NanoTracker→CA→CurrentTarget→range→HOROS authority. Exact live sensor-mode/ScalerCrop/ISP→640x640 forward transform remains NOT_VERIFIED.
PREREQUISITES: Satisfied for comparative design review from Task A, Task A physical addendum, Task B, and their independent reviews.
DEPENDENCIES: No implementation dependency. Any future implementation depends on direct verification of the live forward transform.
AFFECTED_COMPONENTS: camera geometry metadata/provenance; calibration↔AI transform; bbox projection; range/LOS/HOROS metric ingress; frame/timestamp identity; optional future calibrated pixel/ROI consumers.
PROTECTED_COMPONENTS: HQ physical calibration; Hailo model/input authority; NanoTracker; CA Kalman; CurrentTargetManager; HOROS estimator; production runtime/config; command/actuation; class profiles.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: Produce requested A-M comparative decision output; preserve six-domain validation decomposition; choose exactly one implementation recommendation and one final verdict; define shared prerequisite, fallback path and minimal future Codex handoff boundary. No implementation, no Codex prompt, no new general research.
VALIDATION_METHOD: Direct comparison of existing Task A/B canonical evidence and reviews, including Task A live/physical addendum, with independent adversarial consistency check.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908/DECISION.md
- review/TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908.md

## HARD CONSTRAINTS
- Comparative review only.
- No implementation or production/runtime changes.
- No new general research.
- Do not misrepresent Task A as second independent camera/tracker.
- Do not misrepresent Task B as image reconstruction.
- Preserve one tracking/target/HOROS authority.
- Exact live forward transform remains a hard gate.
