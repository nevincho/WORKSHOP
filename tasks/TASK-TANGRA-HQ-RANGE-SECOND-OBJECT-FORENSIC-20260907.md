# TASK — TANGRA HQ MONOCULAR RANGE / SECOND PHYSICAL OBJECT FORENSIC

TASK_ID: TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Independently re-evaluate the HQ monocular class-size range discrepancy using a second independent physical test object and compare against the prior E88/FPV experiment.
SOURCE_PLAN_OR_REQUEST: Owner-supplied second-object forensic brief dated 2026-09-07.
CURRENT_STATE: COMPLETE / Reviewer PASS. Application-level traced path uses HQ Picamera2 BGR888 640x640 direct Hailo input; focal scaling denominators 2028 and 1520. Second object independently reproduces ~2.10–2.15 under-range scale on both axes for the stated 0.019m x 0.016m orientation. Upstream Picamera2/libcamera/sensor/ISP crop/scaling remains NOT VERIFIED.
PREREQUISITES: Satisfied.
DEPENDENCIES: Prior TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907 evidence used for cross-experiment comparison.
AFFECTED_COMPONENTS: Read-only geometry analysis only.
PROTECTED_COMPONENTS: HQ calibration, class-size profiles, HOROS implementation, detector/tracker/Kalman/runtime, production configuration.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: PASS — calculations reproduced for RAW/CA and both axis mappings; required fx/fy and implied source geometry reverse-solved; prior E88 compared; H1-H9 disposition reviewed; one decisive live geometry trace specified.
VALIDATION_METHOD: Independent arithmetic cross-check plus Reviewer adversarial consistency review against both experiments.
PRE_CHANGE_CHECKPOINT: Not applicable; read-only forensic task.
ROLLBACK_METHOD: Not applicable; no target-system modification occurred.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907/SCOUT.md ; review/TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907.md

## Final classification
- Common image-geometry/effective-scale mismatch: STRENGTHENED.
- Exact single fixed ROI/crop geometry explaining both experiments: WEAKENED / not supported by current reverse solutions.
- E88-specific clipping/semantic/measurement issue plus separate common geometry error: STRENGTHENED / leading composite hypothesis.
- Physical sensor/ISP crop: NOT VERIFIED.
- Calibration root cause: NOT VERIFIED.

## Hard constraints preserved
- No code changes.
- No calibration changes.
- No correction constants.
- No class-size profile changes.
- No Codex.
- No runtime/production modification.