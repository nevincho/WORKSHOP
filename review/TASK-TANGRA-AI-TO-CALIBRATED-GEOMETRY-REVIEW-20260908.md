# REVIEW — TANGRA AI GEOMETRY → CALIBRATED HQ GEOMETRY

TASK_ID: TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908
VERDICT: PASS
STATUS: COMPLETE

## Independent review conclusion

The research correctly separates coordinate reconstruction from image reconstruction and does not assume that the current 640x640 runtime frame has a verified full-field relationship to the 2028x1520 calibration. The exact live transform remains NOT_VERIFIED pending direct sensor/ScalerCrop/preprocess evidence.

### Mathematical checks

1. The forward crop→resize→pad transform is correctly expressed as p_ai=A p_cal with A=[[sx,0,px-sx*x0],[0,sy,py-sy*y0],[0,0,1]].
2. The inverse mapping is correct for non-zero sx/sy and recovers arbitrary points, bbox corners, centers and keypoints inside the visible domain.
3. K_ai=A K_cal is correct for the same image-coordinate transform.
4. The equivalence proof is correct: K_ai^-1 p_ai = K_cal^-1 p_cal.
5. Class-size range equivalence is correctly shown independently per axis; anisotropic scaling is not itself a metric error when fx/fy and bbox dimensions use matching sx/sy.
6. The synthetic proof case round-trips the selected 2028x1520 coordinates through a 640x640 anisotropic resize with zero analytic error.

### Adversarial constraints

- A crop/ROI can be inverted only for coordinates inside the observed crop; missing object extent cannot be reconstructed: PASS.
- Letterbox padding must be explicitly removed and boxes intersecting padding/boundaries require validity checks: PASS.
- Detector bbox semantic validity is treated separately from coordinate validity: PASS.
- No competing tracker or second CurrentTarget authority is introduced: PASS.
- NanoTracker and CA Kalman remain unchanged authoritative stages: PASS.
- target_profiles.py physical dimensions are not modified: PASS.
- No calibration parameters, correction constants or synthetic pixels are proposed: PASS.

## Architecture disposition

The geometry-only architecture is the preferred minimum future boundary for current class-size range/LOS/HOROS if the direct camera probe proves a stable deterministic transform from calibrated field to AI coordinates and the required object extent remains visible.

A separate calibration-preserving metric stream is justified only when:
- the AI path discards required calibrated FOV/physical boundaries; or
- a later metric algorithm requires calibrated pixels/ROI content rather than point/bbox geometry.

This conclusion is architectural only. It does not authorize implementation.

## Key risk

The largest risk is transform provenance, not floating-point precision. A numerically exact inverse of the wrong crop/ScalerCrop/resize mapping would produce systematically wrong metric results. Therefore camera/config generation, frame ID, SensorTimestamp and geometry transform identity must be treated as one provenance contract.

## Validation gate

Before any implementation:
1. directly observe sensor mode, ScalerCrop, stream geometry and any Hailo preprocessing;
2. derive the real forward A from evidence;
3. run Method-A vs Method-B equivalence tests;
4. run clipping/boundary rejection tests;
5. run known-distance physical validation;
6. preserve >25 FPS and measure minimum FPS/p95 latency/stale age.

## Definition of Done / hygiene

- Required A-N research sections present: PASS.
- Exact-live-transform uncertainty explicitly preserved: PASS.
- Mathematical proof and synthetic round-trip present: PASS.
- Comparison with dual-stream architecture present: PASS.
- No implementation/runtime/Pi5/Codex action: PASS.
- No production, calibration, tracker, CA, CurrentTarget, HOROS or class-profile changes: PASS.
- Repository artifacts limited to canonical task + research + final review: PASS.

FINAL VERDICT: **PASS / COMPLETE FOR DESIGN REVIEW ONLY.**

Architecture verdict: **VIABLE_WITH_CONDITIONS; geometry back-projection is RECOMMENDED as the minimum future design only after the actual forward transform is VERIFIED.**