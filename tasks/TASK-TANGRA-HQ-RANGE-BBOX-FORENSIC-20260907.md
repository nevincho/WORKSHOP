# TASK — TANGRA HQ MONOCULAR RANGE / BBOX GEOMETRY FORENSIC

TASK_ID: TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: COMPLETE
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO

## OBJECTIVE
Bounded read-only forensic of the ~46% HQ monocular class-size under-range discrepancy, testing whether an unaccounted crop/ROI or equivalent image transform can explain the supplied detector-space bbox and range numbers.

## SOURCE_PLAN_OR_REQUEST
Owner request dated 2026-09-07. Original full forensic specification and supplied numerical inputs are preserved in Git history before completion compaction.

## CURRENT_STATE
COMPLETE for mathematical forensic only. Physical/runtime root cause remains NOT VERIFIED.

Reviewer verdict: PASS.

Key result: an unaccounted image-scale transform is MATHEMATICALLY CONSISTENT and is the leading hypothesis. The exact proposed 1014x760 ROI is an excellent X-axis fit but is not jointly consistent with Y. If transform mismatch alone explains both axes with the supplied physical extents, the equivalent pre-resize geometry is approximately 1006.55x886.01 -> 640x640.

## PREREQUISITES
Satisfied for read-only mathematics. No runtime/Pi access, Codex, implementation, or wider TANGRA discovery was required.

## DEPENDENCIES
NONE.

## AFFECTED_COMPONENTS
HQ image geometry; detector preprocessing geometry; bbox coordinate transforms; monocular class-size range geometry; display-vs-ranging bbox provenance.

## PROTECTED_COMPONENTS
HOROS; production detector/Hailo; NanoTracker; CA Kalman; Fusion; CURRENT_TARGET; command/actuation; production runtime/config; class-size profiles; calibration values.

## ACCEPTANCE_CRITERIA
PASS. Independent recomputation, transform equations, root-cause ranking, required one-frame variables, decisive test, expected TRUE/FALSE outcomes, and do-not-change constraints are recorded in final evidence/review.

## VALIDATION_METHOD
Independent mathematical recomputation and consistency analysis only. No physical/runtime validation claimed.

## PRE_CHANGE_CHECKPOINT
N/A — no target implementation change.

## ROLLBACK_METHOD
N/A — no target implementation/runtime change.

## EVIDENCE_PATHS
- evidence/TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907/SCOUT.md
- review/TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907.md

## PROTECTED_COMPONENT_STATUS
NO VIOLATION.

## CODEX_STATUS
NOT INVOKED.