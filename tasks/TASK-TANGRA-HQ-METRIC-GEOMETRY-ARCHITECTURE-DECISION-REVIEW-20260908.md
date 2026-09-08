# TASK — TANGRA HQ METRIC GEOMETRY ARCHITECTURE DECISION REVIEW

TASK_ID: TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: COMPLETE
OBJECTIVE: Compare the already COMPLETE/Reviewer-PASS Task A and Task B results and select the first implementation architecture for HQ metric range/LOS/HOROS without reopening settled findings except where required to resolve contradictions.
SOURCE_PLAN_OR_REQUEST: Explicit owner comparative-review request dated 2026-09-08.
CURRENT_STATE: COMPLETE / Reviewer PASS. Task A and Task B are not mutually exclusive. Decision: HYBRID_MINIMAL_FIRST; final verdict HYBRID_PREFERRED. First implementation boundary should use Task B's geometry-only AI→calibration projection after the live forward transform is VERIFIED, while keeping Task A-compatible camera-geometry/provenance contracts so calibrated pixels/ROI can be added later if a real consumer requires them. Exact live sensor-mode/ScalerCrop/ISP→640x640 forward transform remains NOT_VERIFIED and is a shared hard prerequisite.
PREREQUISITES: Satisfied for comparative design review from Task A, Task A physical addendum, Task B, and their independent reviews.
DEPENDENCIES: No implementation dependency. Any future implementation depends on direct verification of the live forward transform.
AFFECTED_COMPONENTS: camera geometry metadata/provenance; calibration↔AI transform; bbox projection; range/LOS/HOROS metric ingress; frame/timestamp identity; optional future calibrated pixel/ROI consumers.
PROTECTED_COMPONENTS: HQ physical calibration; Hailo model/input authority; NanoTracker; CA Kalman; CurrentTargetManager; HOROS estimator; production runtime/config; command/actuation; class profiles.
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: PASS. Requested A-M comparative decision output produced; six-domain validation decomposition preserved; exactly one implementation recommendation and one final verdict selected; shared prerequisite, fallback path and minimal future Codex handoff boundary defined. No implementation, no Codex prompt, no new general research.
VALIDATION_METHOD: Direct comparison of existing Task A/B canonical evidence and reviews, including Task A live/physical addendum, with independent adversarial Reviewer PASS.
PRE_CHANGE_CHECKPOINT: N/A — no implementation change.
ROLLBACK_METHOD: N/A — no implementation change.
EVIDENCE_PATHS:
- evidence/TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908/DECISION.md
- review/TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908.md

## DECISION
IMPLEMENTATION_RECOMMENDATION: HYBRID_MINIMAL_FIRST
FINAL_VERDICT: HYBRID_PREFERRED

## HARD CONSTRAINTS CONFIRMED
- Comparative review only.
- No implementation or production/runtime changes.
- No new general research.
- Task A not treated as second independent camera/tracker.
- Task B not treated as image reconstruction.
- One tracking/target/HOROS authority preserved.
- Exact live forward transform remains a hard gate.
