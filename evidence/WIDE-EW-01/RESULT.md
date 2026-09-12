# WIDE-EW-01 — Engineering Result

DATE: 2026-09-12
MODE: WORKSHOP ENGINEERING / NO RUNTIME INTEGRATION

## CUE_CONTRACT
`WideAcquisitionCue` v1 fields:
- `schema_version: 1`
- `cue_id: int` — local correlation only; never target identity
- `source: WIDE_IMX708`
- `timestamp_monotonic_s`
- `max_age_s`
- `image_x_norm` in `[0,1]`
- `image_y_norm` in `[0,1]`
- `horizontal_offset_norm` in `[-1,1]`, defined as `(image_x_norm - 0.5) * 2`
- `sector: LEFT | CENTER | RIGHT`
- `motion_area_norm` in `[0,1]`
- `quality` in `[0,1]` — deterministic motion-evidence strength only; NOT detector/class probability
- `persistence_frames`
- `provenance: WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC`

Explicitly absent: class, target ID, track ID, metric range, XYZ, bearing, velocity, FC command, navigation authority.

## CUE_GEOMETRY
Non-metric only. Cue position is normalized image-space centroid of pixels differing from the retained stable-background frame. Horizontal signed offset is image-space only. Sector uses signed normalized offset with default center half-width 0.20: offset < -0.20 LEFT; > +0.20 RIGHT; otherwise CENTER.

No degree/radian/bearing conversion exists. WIDE metric/angular geometry remains NOT_VERIFIED for this unit.

## MOTION_METHOD
Reference implementation uses deterministic stable-background grayscale differencing over an already-downscaled frame. Default engineering operating point:
- processing frame: 160x90 grayscale;
- pixel absolute-difference threshold: 20/255;
- minimum changed area: 0.005 of frame;
- no neural inference;
- no optical flow;
- no tracking;
- one retained stable-background frame only.

Background is refreshed only when the current observation is below the motion threshold. A qualifying disturbance does not immediately replace the background. This prevents a one-frame disturbance followed by return to the stable scene from being counted as two persistent observations.

The generator is deliberately downstream of capture/downscale. It does not own camera acquisition and therefore can attach later to the existing latest-frame WIDE boundary without changing capture authority.

## TEMPORAL_FILTER
Default minimum persistence: 2 consecutive frames that differ materially from the stable background. A single qualifying frame does not emit a cue. Return to stable/no-motion scene, insufficient motion, malformed input or processing failure resets persistence. State is bounded to exactly one retained downscaled background frame, one persistence counter and cue sequence state; no backlog/queue is introduced.

## FRESHNESS_RULE
Cue source time is monotonic. Default `max_age_s = 0.5`. Consumer acceptance requires:
- schema/provenance validation PASS;
- finite age;
- age >= 0;
- age <= `max_age_s`.

Future MC1/M1 ingress must evaluate freshness at consumption time; cue creation does not grant mission authority.

## MC1_INGRESS_BOUNDARY
Future integration boundary is:
`existing WIDE latest frame -> WideCueGenerator -> WideAcquisitionCue -> acquisition bridge -> MC1 authority validation -> M1 acquisition decision`.

The cue is presented only as candidate evidence to the future acquisition bridge. MC1 remains the source of mission activation/operator intent/readiness/safety gates. M1 remains the mission-decision layer. N1 is bypassed for pre-confirmation cueing. No CurrentTarget/HOROS state is created by this package.

## FAIL_CLOSED_RULES
No cue / rejected cue when:
- WIDE frame unavailable;
- frame dimensions/pixels malformed;
- timestamp non-finite;
- changed area below threshold;
- persistence below threshold;
- cue schema/source/provenance invalid;
- coordinates/quality/area non-finite or out of bounds;
- cue age negative or above expiry;
- processing exception occurs.

There is no fallback to neural inference, metric bearing, CurrentTarget, N1, M1/M2/M3 action or FC command.

## TEST_RESULTS
Deterministic synthetic validation against the hardened reference package:
- STATIC -> no persistent cue: PASS
- MOTION LEFT -> valid LEFT cue after persistence: PASS
- MOTION CENTER -> valid CENTER cue after persistence: PASS
- MOTION RIGHT -> valid RIGHT cue after persistence: PASS
- TRANSIENT NOISE -> rejected: PASS
- LARGE ONE-FRAME TRANSIENT -> rejected after return to stable scene: PASS
- STALE CUE -> accepted while fresh and rejected after max age: PASS
- malformed frame -> fail closed: PASS

Required acceptance scenarios: 6/6 PASS. Additional adversarial large-transient and malformed-input gates: PASS.

## RESOURCE_COST
Bounded reference benchmark executed on the available Workshop Python execution environment, not Pi5 and not production, after temporal-filter hardening:
- frame size: 160x90 grayscale = 14,400 samples;
- iterations: 1,000 processing calls over prebuilt synthetic frames;
- total processing time: 1.710 s;
- mean processing time: 1.710 ms/sample;
- processing-only equivalent throughput: ~584.8 samples/s.

At a proposed low acquisition sampling rate of 5 Hz this reference cost corresponds to ~8.55 ms processing time per wall-clock second on the benchmark host (~0.86% of one core if scheduling overhead and capture/downscale are excluded).

Interpretation: 160x90 at 5 Hz is a credible low-cost engineering operating point for integration testing. This is NOT Pi5 resource evidence and does not prove production CPU/RAM cost. Capture/downscale cost is excluded. A later integration unit must verify actual Pi/development-copy cost before promotion.

Memory is structurally bounded by one retained 160x90 grayscale background frame plus the current processing frame and small scalar state. Exact Python/native RSS on Pi is NOT_VERIFIED.

## FILES
- `handoffs/WIDE-EW-01/wide_acquisition_cue.py`
- `handoffs/WIDE-EW-01/test_wide_acquisition_cue.py`
- `tasks/WIDE-EW-01-WIDE-ACQUISITION-CUE-CONTRACT.md`
- this evidence file

## SCOPE PROTECTION
No changes were made to HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, M1, M2, M3, FC, command-send authority, Pi5 or production. No telemetry was removed.

## ENGINEERING_VERDICT
PASS_CANDIDATE_FOR_INDEPENDENT_REVIEW
