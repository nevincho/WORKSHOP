# REVIEW — TANGRA HQ DUAL-STREAM / CALIBRATION-PRESERVING METRIC PATH

TASK_ID: TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908
VERDICT: PASS
STATUS: COMPLETE

## Independent review conclusion

The design review correctly separates three concepts that must not be conflated:
1. camera optical/calibration geometry;
2. detector tensor geometry;
3. authoritative target-state geometry/identity.

The proposed architecture is acceptable only as **one camera acquisition authority with two logical geometry products**. It does not require or justify a second tracker, second CA filter, second CurrentTarget authority, or second independent Picamera2 capture loop.

## Adversarial checks

### 1. Does the metric path require a duplicate full-resolution image pipeline?
No. For the currently described class-size range and LOS projection, the minimum information is calibration-space bbox/centre geometry, K/calibration identity, source frame/timestamp and size/class provenance. Full HQ pixels are required only if a specific metric algorithm consumes pixels/landmarks/ROI. Therefore retaining/copying full 2028x1520 BGR frames for every downstream metric consumer would be unnecessary architecture expansion.

### 2. Is a Picamera2 main+lores arrangement automatically safe?
No. Picamera2/libcamera support multiple streams from one image source/request, but the exact crop/aspect/scaling relation of a candidate 2028x1520 main and 640x640 secondary stream remains NOT VERIFIED. The review correctly refuses to treat secondary-stream dimensions as geometry provenance.

### 3. Is application resize automatically preferable?
No. It is easier to audit geometrically but may impose substantial CPU/memory-copy cost. An ISP-generated secondary stream may be more efficient. The correct choice is benchmark-driven after both mappings are proven.

### 4. Can the existing tracker/CA remain authoritative?
Yes. The metric branch can be a pure coordinate/measurement projection from the authoritative AI-space bbox/state. This satisfies the protected-authority requirement and avoids architecture drift.

### 5. Is asynchronous/lower-rate Hailo already safe?
No. Prior multi-rate research supports the pattern but TANGRA-specific delayed-result semantics, detector cadence and quality envelope remain NOT VERIFIED. Frame/timestamp/source-age contracts are prerequisites.

## Performance review

The evidence correctly highlights memory bandwidth rather than RAM capacity as the primary risk of naïve full-resolution duplication. Approximate BGR888 payload at 2028x1520 is 9,247,680 bytes/frame; a single full application-level copy at 25 FPS is ~231 MB/s before stride/cache/allocator/ISP overhead. Therefore implementation must avoid gratuitous full-frame copies and stale queues.

The >25 FPS operational gate remains mandatory. A design that restores calibration geometry but causes <=25 FPS in any defined operational benchmark is not acceptable as production architecture without further redesign.

## Required future gate

Before implementation:
1. direct Picamera2/libcamera geometry probe for current and candidate configurations;
2. prove exact mapping between calibration geometry and AI geometry;
3. benchmark one-stream+application-transform versus multi-stream/ISP transform if both are valid;
4. introduce frame/timestamp/config-generation provenance before asynchronous or decimated detector operation;
5. validate range/HOROS using projected authoritative target geometry;
6. independently verify FPS/latency/tracking/range/HOROS regressions.

## Definition of Done / hygiene

- A-L requested output present: PASS.
- VERIFIED/INFERRED/NOT_VERIFIED/RECOMMENDATION classifications present: PASS.
- No implementation or runtime action: PASS.
- No calibration/refocus/model/tracker/CA/CurrentTarget/HOROS authority change: PASS.
- No second authoritative target path proposed: PASS.
- No duplicate intermediate artifacts beyond task + consolidated evidence + review: PASS.

FINAL VERDICT: **PASS / COMPLETE FOR DESIGN REVIEW ONLY.**

Architecture disposition: **VIABLE_WITH_CONDITIONS**. The next justified action is a read-only geometry/performance probe, not production implementation.
