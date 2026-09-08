# REVIEW — TANGRA HQ DUAL-STREAM / CALIBRATION-PRESERVING METRIC PATH

TASK_ID: TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908
VERDICT: PASS
STATUS: COMPLETE

## Independent review conclusion

The original architecture verdict remains **VIABLE_WITH_CONDITIONS**. The 2026-09-08 live/physical addendum strengthens the need to keep camera geometry, coordinate transform, class-size prior, silhouette variability, frame identity, and performance as separate validation domains.

The design still correctly separates:
1. camera optical/calibration geometry;
2. detector tensor geometry;
3. authoritative target-state geometry/identity;
4. physical-size/class provenance used by range estimation.

The acceptable architecture remains **one HQ acquisition authority with one protected detection/tracking/CurrentTarget authority and an explicit calibration↔AI geometry contract**. No second tracker, second CA filter, second CurrentTarget authority, or second independent Picamera2 capture loop is justified.

## Review of new live/runtime evidence

### VERIFIED from owner-supplied live observation
- Current telemetry still reports HQ processing frame size 640x640.
- Attempted read-only HQ snapshot endpoint returned HTTP 404.
- No sufficiently recent dataset image was available under unchanged-runtime constraints.

### Reviewer interpretation
The missing snapshot is an **observability limitation**, not evidence of camera failure. It does not establish sensor mode, ScalerCrop, FOV, binning, crop, or ISP mapping. The exact live transform from calibrated optical field to 640x640 therefore remains **NOT_VERIFIED**.

## Review of physical F450 observation

- F450 did not fit fully in the HQ+50 mm view at approximately 2.58 m: accepted as VERIFIED operator physical observation.
- Lens-to-F450 distance was then measured exactly at 4.000 m; HQ focus unchanged: accepted as VERIFIED physical setup evidence.
- Full F450 visibility at 4.000 m: NOT_VERIFIED because no current HQ image was available.

The addendum correctly rejects nominal F450 model dimensions as automatic metric ground truth. A future metric test must use a directly measured rigid landmark-to-landmark span that corresponds to the measured image extent.

## Review of E88 evidence

### Classification variability
The same physical E88 was observed as FPV, Orlan-10 and Talay in the same general physical setup. This is valid robustness evidence, but not sufficient to classify detector behaviour as failure.

### Silhouette variability
The E88 free/folding propellers provide a credible physical mechanism for changing visible width/height/diagonal/rotor geometry. This makes the unconstrained full silhouette a poor metric target.

Reviewer disposition:
- E88 as unconstrained exact metric-calibration target: **WEAKENED / NOT RECOMMENDED**.
- E88 as detection/classification/robustness stimulus: **RECOMMENDED**.
- Propeller motion as sole explanation of class changes: **NOT_VERIFIED**.

## Review of class-size range provenance risk

The addendum identifies a genuine independent range-path risk: class-size ranging combines image geometry with a physical-size prior. Therefore a class change can change range even when bbox geometry is similar.

This risk exists regardless of whether the architecture uses dual logical geometry products or AI→calibration back-projection.

Required future forensic trace is accepted: determine whether `range_estimator` consumes instantaneous detector class, CurrentTarget-stabilized class, another stabilized identity, or another provenance source. No detector or class-profile modification is authorized by this review.

## Review of prior physical tests

### Printed E88 test
The supplied test-only 17 cm x 11 cm arithmetic is internally coherent, but the stimulus did not provide a trustworthy one-to-one bbox↔physical-dimension correspondence. Therefore it must not be used as proof of bad calibration. It remains valid evidence of range sensitivity to physical-size/bbox correspondence.

### Tiny Shahed model
The approximately 159.293 m result at true 2.585 m used the production full-size Shahed prior for a 1.9 cm x 1.6 cm miniature. Reviewer agrees this is a deliberate physical-size-prior mismatch, not camera-geometry evidence. Production Shahed dimensions remain protected.

## Updated validation doctrine

Before any metric promotion, the following MUST be validated separately:

1. **CAMERA GEOMETRY** — rigid known span, known pixel span, known range; establish sensor/crop/FOV mapping independently of class semantics.
2. **COORDINATE TRANSFORM** — known calibration-space points → AI transform → inverse transform → recovery error.
3. **CLASS PRIOR** — fixed image geometry with controlled alternate profiles to quantify range sensitivity and trace actual runtime class provenance.
4. **SILHOUETTE VARIABILITY** — quantify bbox/class changes from movable geometry such as E88 propellers.
5. **FRAME IDENTITY** — detector observation from frame N must use frame-N transform/metric geometry and correct CurrentTarget generation.
6. **PERFORMANCE** — complete authoritative HQ path must remain >25 FPS.

A single mixed end-to-end range PASS/FAIL is methodologically insufficient because it cannot distinguish camera geometry error from transform error, class-prior error, silhouette variability, temporal mismatch, or performance regression.

## Architecture review after addendum

The preferred topology remains:

`ONE HQ acquisition authority`
→ `explicit calibration-consistent geometry / transform provenance`
→ `deterministic AI 640x640 geometry`
→ existing `Hailo`
→ existing `NanoTracker`
→ existing `CA Kalman`
→ existing `CurrentTargetManager`
→ inverse/project authoritative object geometry into calibration coordinates
→ class-size range / LOS
→ HOROS.

Metric processing remains downstream of the protected tracking chain.

Minimum future boundary remains:
- camera geometry metadata;
- frame/timestamp/config-generation identity;
- deterministic AI transform;
- inverse object-geometry projection;
- metric/class provenance.

## Definition of Done / hygiene

- Original A-L architecture review: PASS.
- New live/physical addendum preserved as unique evidence: PASS.
- Validation domains separated explicitly: PASS.
- No implementation/runtime modification: PASS.
- No calibration/refocus/model/tracker/CA/CurrentTarget/HOROS authority change: PASS.
- No production class-profile change: PASS.
- No second authoritative target path: PASS.
- Repository evidence remains compact: task + consolidated research + unique live/physical addendum + final review: PASS.

FINAL VERDICT: **PASS / COMPLETE FOR DESIGN REVIEW ONLY.**

Architecture disposition remains **VIABLE_WITH_CONDITIONS**. The new evidence does not justify calibration changes or production implementation; it strengthens the need for direct camera-geometry observability and a separate range-class-provenance trace before metric promotion.
