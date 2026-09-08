# TASK 2 Evidence Report

RESULT: PASS_FOR_STANDALONE_CANDIDATE / REVIEW_REQUIRED
DATE: 2026-09-08

## Evidence gate
Repository/configuration search across available WORKSHOP and TANGRA-DOCS did not prove the exact live HQ CAL->AI preprocessing transform. No concrete production A is claimed. Production transform: NOT_VERIFIED.

## Implementation
Standalone NumPy affine-coordinate adapter with explicit PlaneSpec, GeometryTransform, TASK1-equivalent input, calibrated output, fail-closed validation, bbox corner mapping, point/null preservation, and intrinsics transform helper.

## Tests
12/12 PASS: identity; anisotropic full-frame resize; crop+resize; letterbox/padding inverse; bidirectional round-trip; bbox mapping; TASK 1 sparse-point mapping; invalid/null preservation; boundary/corner coordinates; non-invertible fail-closed; malformed/non-affine fail-closed; K/coordinate consistency.

Floating-point assertions use absolute tolerances of 1e-8 to 1e-9 for deterministic affine cases.

## Performance
Environment: x86_64 container; Python/NumPy coordinate-only microbenchmark; NOT Pi5/end-to-end.
Sample count: 20,000.
Mean: 0.315403 ms
Median: 0.292583 ms
p95: 0.383131 ms
Maximum: 21.285867 ms
No Pi5 or end-to-end FPS claim.

## Dependencies
Python 3, NumPy; standard dataclasses/typing/math.

## Protected state
TASK 1 frozen source not modified. No HQ acquisition, detector, tracker, CA Kalman, CurrentTargetManager, range estimator, HOROS estimator, Guidance, Dashboard, command path, production runtime, second frame/detector/tracker, or full-resolution image reconstruction touched.

STATUS: READY_FOR_INDEPENDENT_REVIEW
