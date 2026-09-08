# TASK 7 ARCHITECTURE DECISION / EVIDENCE

## Existing boundary reused
Repository architecture states: Raspberry Pi owns AI, tracking, mission logic and guidance generation; Master ESP32 owns communications/routing/bridge; Flight Controller ESP32 owns stabilization, safety, control loops and ESC output and always has final flight authority. HOROS master plan forbids HOROS guidance/actuation authority. TASK7 therefore creates no competing Guidance subsystem: it is an isolated adapter/contract feeding the existing future Mission Logic/Guidance Layer boundary.

GUIDANCE_RUNTIME_STATUS=NOT_VERIFIED. Inspected repository documentation proves the architecture boundary but not a current executable production Guidance Layer. No production integration is performed.

## Input contract
HorosGuidanceInput preserves target_ref, timestamp, frame_ref, lifecycle, metric_state/usability, optional authoritative HOROS XYZ/Vxyz/covariance/prediction reference/range state, confidence, optional externally supplied carrier pose, TASK6 envelope evidence and provenance. Missing state is never fabricated.

## Output contract
PassiveGuidanceAdvisory is advisory/state evidence only: AVAILABLE/DEGRADED/SUPPRESSED plus OBSERVE, MAINTAIN_OBSERVATION_GEOMETRY, TRACK_STATE_UNUSABLE or NO_GUIDANCE_AVAILABLE. Contract contains no transport, actuator, flight-mode or motor command field and production_authority is always false.

## Deterministic policy
- valid metric state + RELIABLE envelope + XYZ => AVAILABLE/OBSERVE.
- degraded metric/lifecycle or DEGRADED/UNKNOWN envelope => DEGRADED; degradation preserved.
- UNUSABLE envelope, INVALID/CONFLICT metric state, UNUSABLE metric usability, LOST, COASTING, stale, malformed or missing XYZ => SUPPRESSED.
- NOT_VERIFIED propagates unchanged and never promotes.
- carrier pose absent => target-relative advisory may remain, but world_navigation_available=false.
- valid externally supplied carrier pose => world_navigation_available may be true for non-suppressed advisory; TASK7 computes no trajectory.
- TASK6 envelope is consumed verbatim; no angle/scale/orientation recomputation.

## Freshness
Production freshness threshold is NOT_VERIFIED. Focused tests use explicit SHADOW_TEST FreshnessConfig(stale_after_s=0.5). Source timestamp and evaluated-at time are preserved; negative age is timestamp_discontinuity; age above configured shadow threshold fails closed.

## Tests / fail closed
20/20 PASS locally: reliable, degraded, unusable, invalid, conflict, LOST, COASTING, stale, missing/valid pose, NOT_VERIFIED propagation, target identity change, timestamp discontinuity, malformed input, repeatability, no production authority, no control/transport fields, missing XYZ, degraded metric, TASK6 envelope pass-through.

## Performance
HOST-only CPython benchmark, 100000 evaluations: mean 0.00386388029 ms; median 0.003715 ms; p95 0.003855 ms; max 0.858007 ms. No Pi5 or end-to-end claim.

## Production gates
AI→CAL transform NOT_VERIFIED; physical point↔span correspondence NOT_VERIFIED; physical metric accuracy NOT_VERIFIED; Pi5 E2E NOT_VERIFIED; Guidance runtime integration NOT_VERIFIED. No promotion.
