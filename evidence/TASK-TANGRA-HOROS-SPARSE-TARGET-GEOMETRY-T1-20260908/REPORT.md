# TASK 1 Evidence Report — Sparse Target Geometry

RESULT: PASS_FOR_STANDALONE_CANDIDATE / REVIEW_REQUIRED
DATE: 2026-09-08

## What was actually tested
A standalone deterministic ROI-only candidate, not production integration. Tests used SYNTHETIC top-down/mild-rotation fixtures and directly exercised point ordering, confidence response, axial ambiguity, boundary clipping, repeatability, blank ROI invalidation and source-input immutability.

## Test result
9/9 unittest cases PASS: near top-down silhouette; mild oblique/top-down proxy; point ordering/repeatability; geometry-confidence response; ambiguous nose/tail handling; ROI/frame boundary clipping; unchanged-input repeatability; no mutation of frame/metadata; blank ROI invalidation.

The mild-oblique test is a synthetic 23-degree in-plane proxy and is not physical perspective/3D-obliquity validation.

## Performance
Environment: x86_64 Workshop container, OpenCV 4.13.0, NumPy 2.3.5. Microbenchmark only; 900 targets, 300 per size.
- ROI 64x64; target span ~49x33 px: mean 0.564 ms, median 0.582 ms, p95 0.690 ms, max 1.536 ms.
- ROI 128x96 (reported HxW 96x128); target span ~97x50 px: mean 0.649 ms, median 0.630 ms, p95 0.818 ms, max 2.703 ms.
- ROI 192x144 (reported HxW 144x192); target span ~146x75 px: mean 0.865 ms, median 0.819 ms, p95 1.000 ms, max 5.452 ms.
Overall: mean 0.693 ms, median 0.646 ms, p95 0.907 ms, max 5.452 ms.
No end-to-end FPS effect is inferred.

## Dependency / copy behavior
Dependencies: Python 3, NumPy, OpenCV. Source target ROI is a NumPy view, not an explicit source ROI copy. Grayscale, threshold, component mask, morphology and contour/PCA data are ROI-sized temporary allocations. No full-frame copy or persisted contour.

## Protected state
No target repository/runtime was modified. Candidate has no write path into detector, NanoTracker, CA Kalman, CurrentTargetManager, range estimator, HOROS authoritative state, flight guidance, dashboard or command paths.

## Validation classification
Standalone algorithm objective: VERIFIED in the stated synthetic harness.
Physical silhouette quality: NOT VERIFIED.
True mild-oblique perspective behavior: NOT VERIFIED.
Pi5 latency/end-to-end FPS: NOT VERIFIED.
Current local production source compatibility/insertion point: NOT VERIFIED.
Metric coordinates/range: OUT OF SCOPE / NOT IMPLEMENTED.
