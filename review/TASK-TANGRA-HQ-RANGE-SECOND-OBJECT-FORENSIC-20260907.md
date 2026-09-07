# REVIEW — TANGRA HQ MONOCULAR RANGE / SECOND PHYSICAL OBJECT

TASK_ID: TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907
VERDICT: PASS
STATUS: COMPLETE

## Review findings

The arithmetic in the Scout evidence was independently checked against the owner-supplied intrinsics, RAW bbox, CA/range bbox, physical dimensions, and 2.585 m ground truth.

### Verified numerical results
Orientation A (W=0.019 m, H=0.016 m):
- RAW Rw = 1.200343 m
- RAW Rh = 1.230201 m
- CA/range Rw = 1.205752 m
- CA/range Rh = 1.232094 m
- RAW required fx = 10708.703 px
- RAW required fy = 14022.009 px
- RAW implied calibrated-source geometry = 941.700 x 723.367 px
- CA/range required fx = 10660.662 px
- CA/range required fy = 14000.465 px
- CA/range implied calibrated-source geometry = 945.944 x 724.481 px

Orientation B (W=0.016 m, H=0.019 m):
- RAW Rw = 1.010815 m
- RAW Rh = 1.460863 m
- CA/range Rw = 1.015370 m
- CA/range Rh = 1.463111 m

The supplied conclusion that CA modification is far too small to explain the ~2x discrepancy is VERIFIED.

## Adversarial cross-experiment conclusion

The second object materially strengthens the existence of a common scale/effective-focal problem because a normal ~79x87 px bbox independently produces ~1.20–1.23 m at a true 2.585 m distance with close X/Y agreement.

However, the second-object reverse-solved geometry (~942x723 RAW, ~946x724 CA) does NOT match the earlier E88 reverse-solved ~1006.5x886 geometry. Therefore an exact single fixed crop/ROI rectangle is NOT supported by both experiments.

The strongest current interpretation is:
- a common geometry/effective-scale mismatch is STRENGTHENED;
- an additional E88-specific clipping/semantic/measurement effect is also STRENGTHENED;
- exact physical ROI dimensions remain NOT VERIFIED.

## Hypothesis disposition

H1 application focal denominator bug: WEAKENED strongly; traced 2028/1520 denominators are correct for the application code path.
H2 sensor-mode crop: STRENGTHENED as a plausible common upstream mechanism; NOT VERIFIED.
H3 ScalerCrop/ISP crop/digital zoom: STRENGTHENED as a plausible common upstream mechanism; NOT VERIFIED.
H4 detector preprocessing transform absent from range intrinsics: STRENGTHENED / MATHEMATICALLY CONSISTENT.
H5 bbox coordinate transform error: MATHEMATICALLY CONSISTENT but WEAKENED as a simple RAW→CA/display issue.
H6 bbox semantic mismatch/padding: WEAKENED as sole root cause; remains plausible contributor, especially for E88.
H7 E88-specific issue + separate common geometry error: STRENGTHENED and ranked #1.
H8 physical orientation/dimension correspondence error: swapped orientation WEAKENED; exact projected silhouette remains NOT VERIFIED.
H9 calibration wrong: NOT VERIFIED; no evidence justifies changing calibration.

## Decisive next test

PASS recommendation: capture one exact same-frame geometry ledger including actual Picamera2/libcamera sensor mode, raw/full sensor dimensions, current ScalerCrop/crop rectangle, output stream geometry, ISP scaling relation, detector input geometry, RAW bbox, range bbox, display bbox, and actual fx/fy used.

This is the highest-information next test because the current monocular equation cannot algebraically distinguish focal error, image-scale error, uniform bbox-scale error, or sensor/ISP crop from one frame without observing the transform metadata directly.

## Protection review

- No code changes: PASS
- No calibration changes: PASS
- No correction constants: PASS
- No class-size profile changes: PASS
- No Codex: PASS
- No production/runtime modification: PASS
- No physical ROI claimed as verified: PASS