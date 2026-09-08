# TASK — TANGRA AI GEOMETRY → CALIBRATED HQ GEOMETRY REVIEW

TASK_ID: TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908
PROJECT: TANGRA
PRIORITY: CRITICAL
STATUS: COMPLETE
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO

## OBJECTIVE
Determine whether TANGRA can recover metrically correct object geometry in the 2028x1520 HQ calibration coordinate system by mathematically inverting the deterministic transform applied to the 640x640 AI representation, without reconstructing or retaining a separate full-resolution metric image stream.

## CURRENT_STATE
COMPLETE for research/design review only. Reviewer verdict: PASS.

Architecture verdict: VIABLE_WITH_CONDITIONS. Geometry back-projection is RECOMMENDED as the minimum future design only after the actual live forward transform is VERIFIED.

Key result: for an exact invertible image-coordinate transform p_ai=A p_cal, Method A (AI geometry -> A^-1 -> original K) and Method B (AI geometry retained with K_ai=A*K) are mathematically equivalent for ray geometry and class-size range. Anisotropic scaling is safe when X/Y scales are handled independently. Coordinate inversion cannot recover cropped/clipped physical extent or pixels that were never observed.

The exact TANGRA live A remains NOT VERIFIED because active sensor mode / ScalerCrop / upstream optical mapping is still unmeasured.

## PREREQUISITES
Satisfied for mathematical review. Prior HQ geometry forensic and dual-stream architecture evidence were used; no runtime access was required.

## DEPENDENCIES
Any future implementation depends on direct Picamera2/libcamera geometry evidence establishing sensor mode, ScalerCrop, stream geometry and preprocessing transform.

## AFFECTED_COMPONENTS
Camera geometry provenance; AI preprocessing transform; bbox/keypoint mapping; range_estimator.py; target_profiles.py integration semantics; CurrentTarget geometry contract; HOROS LOS_RANGE provenance.

## PROTECTED_COMPONENTS
HQ physical calibration; Hailo model/input contract; NanoTracker; CA Kalman; CurrentTargetManager authority; HOROS estimator authority; production runtime/config; class-size profiles.

## ACCEPTANCE_CRITERIA
PASS. A-N research sections, affine/crop/resize/letterbox derivation, inverse mapping, K transform, Method-A/Method-B equivalence proof, synthetic round-trip, error budget, clipping/visibility rules, range/HOROS integration, minimum future code boundary, validation plan and dual-stream comparison are recorded in evidence and independently reviewed.

## VALIDATION_METHOD
Analytical derivation + synthetic proof case + prior WORKSHOP evidence + current libcamera ScalerCrop semantics + independent Reviewer adversarial check.

## PRE_CHANGE_CHECKPOINT
N/A — no implementation change.

## ROLLBACK_METHOD
N/A — no implementation change.

## EVIDENCE_PATHS
- evidence/TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908/RESEARCH.md
- review/TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908.md

## PROTECTED_COMPONENT_STATUS
NO VIOLATION.

## CODEX_STATUS
NOT INVOKED.

## STOP
Design review complete. No implementation authorized.