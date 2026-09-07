# TASK — TANGRA HQ MONOCULAR RANGE / SECOND PHYSICAL OBJECT FORENSIC

TASK_ID: TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: READY
OBJECTIVE: Independently re-evaluate the HQ monocular class-size range discrepancy using a second independent physical test object and compare against the prior E88/FPV experiment.
SOURCE_PLAN_OR_REQUEST: Owner-supplied second-object forensic brief dated 2026-09-07.
CURRENT_STATE: Application-level traced path uses HQ Picamera2 BGR888 640x640 direct Hailo input; focal scaling denominators 2028 and 1520; upstream Picamera2/libcamera/sensor/ISP crop/scaling remains NOT VERIFIED. Second object measured 0.019m x 0.016m at 2.585m; RAW bbox 78.71x86.79 px; CA/range bbox 78.356897x86.656647 px; display bbox equals range bbox per trace.
PREREQUISITES: Satisfied from owner-supplied data and prior forensic evidence.
DEPENDENCIES: Prior TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907 evidence for cross-experiment comparison.
AFFECTED_COMPONENTS: Read-only geometry analysis only.
PROTECTED_COMPONENTS: HQ calibration, class-size profiles, HOROS implementation, detector/tracker/Kalman/runtime, production configuration.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: Reproduce RAW and CA calculations for both physical-axis mappings; reverse-solve required fx/fy and implied calibrated-source geometry; compare against prior ~1006.5x886 geometry; rank H1-H9 with VERIFIED/MATHEMATICALLY CONSISTENT/STRENGTHENED/WEAKENED/REFUTED/NOT VERIFIED; identify one decisive live geometry trace. No empirical correction, calibration change, runtime modification, or speculative ROI claim.
VALIDATION_METHOD: Independent arithmetic cross-check plus Reviewer adversarial consistency review against both experiments.
PRE_CHANGE_CHECKPOINT: Not applicable; read-only forensic task.
ROLLBACK_METHOD: Not applicable; no target-system modification authorized.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907/SCOUT.md ; review/TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907.md

## Hard constraints
- No code changes.
- No calibration changes.
- No correction constants.
- Do not use production full-size Shahed dimensions; class label is detector output only.
- Do not infer physical ROI merely from half-resolution-like numbers.
- Separate verified facts, mathematical implications, hypotheses, and unknowns.

## Required output sections
A. CALCULATION CHECK
B. SECOND-OBJECT RESULT
C. CROSS-EXPERIMENT COMPARISON
D. EFFECTIVE FX/FY AND IMPLIED SOURCE GEOMETRY
E. UPDATED HYPOTHESIS RANKING
F. WHAT THE NEW EVIDENCE WEAKENS OR REFUTES
G. WHAT REMAINS NOT VERIFIED
H. SINGLE DECISIVE NEXT TEST