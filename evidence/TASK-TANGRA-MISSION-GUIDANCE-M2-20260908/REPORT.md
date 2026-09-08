# M2 Passive Guidance Decision / Translation Layer — Evidence

TASK_ID: TASK-TANGRA-MISSION-GUIDANCE-M2-20260908
STATUS: REVIEW
BASE: M1 reviewed commit 88ffcf4932545304c5a82c83c65ad01b99000680; M1 COMPLETE metadata 4fc48e0a8bcb25807e84dd94d9e2c7c22ffd5cbd.
SCOPE: PASSIVE/SHADOW/non-authoritative translation only. No production integration. HOROS TASK8 untouched.

## Exact M1 input
Tests load the exact frozen M1 implementation file from its repository path and instantiate its real MissionDecision contract. M2 validates M1 version M1_SHADOW_V1 and production_authority=False.

## M2 input contract
GuidanceInput = exact M1 MissionDecision + optional NavigationEvidence + evaluated_at. NavigationEvidence carries only externally supplied target/carrier geometry, lifecycle, metric status, freshness, uncertainty and provenance. Missing geometry is never fabricated.

## M2 output contract
PassiveGuidanceDecision: GuidanceState {AVAILABLE, DEGRADED, SUPPRESSED}; GuidanceIntent {NO_GUIDANCE,HOLD,ABORT_HOLD,MAINTAIN_OBSERVATION,REACQUIRE_TARGET,MOVE_RELATIVE,SET_ALTITUDE,SET_HEADING}; target/time/frame; unchanged metric status; optional relative_vector/altitude/heading; reason/provenance; production_authority=False.

M2 does not infer MOVE_RELATIVE/SET_ALTITUDE/SET_HEADING from target XYZ alone. Those fields remain null in observation/track decisions. For REACQUIRE, an explicit externally supplied search_relative_vector_m may be preserved as evidence only when metric status is VERIFIED; M2 does not create a search trajectory.

## Deterministic M1->M2 mapping
NO_ACTION -> SUPPRESSED/NO_GUIDANCE.
HOLD -> AVAILABLE/HOLD.
ABORT -> AVAILABLE/ABORT_HOLD (passive semantic only).
MISSION_COMPLETE -> AVAILABLE/HOLD.
OBSERVE_TARGET -> MAINTAIN_OBSERVATION only with usable fresh evidence; missing target geometry -> DEGRADED/NO_GUIDANCE; missing carrier pose -> DEGRADED/MAINTAIN_OBSERVATION without movement coordinates.
MAINTAIN_TRACK -> same geometry gates; no fabricated movement.
REACQUIRE -> REACQUIRE_TARGET; without explicit search geometry remains DEGRADED semantic-only.
TARGET_LOST with non-REACQUIRE action -> SUPPRESSED.

## Geometry/authority gates
- M1 and NavigationEvidence target/frame must match.
- M1 timestamp and navigation timestamp must be finite/fresh; regressions/discontinuities suppress.
- lifecycle LOST suppresses navigation except semantic REACQUIRE.
- metric mismatch suppresses.
- UNUSABLE/CONFLICT/INVALID => DEGRADED/HOLD.
- NOT_VERIFIED => DEGRADED, no navigation movement coordinates and no authority promotion.
- malformed/non-finite target/carrier/search vectors, heading, altitude or uncertainty suppress.
- uncertainty >5 m => DEGRADED SHADOW policy only; not production threshold.

## Tests
HOST deterministic suite: 28/28 PASS.
Required coverage includes NO_ACTION, HOLD, ABORT, MISSION_COMPLETE, OBSERVE valid/missing geometry, MAINTAIN_TRACK valid, degraded and NOT_VERIFIED metric, REACQUIRE with/without search geometry, missing carrier pose, stale input, malformed target/carrier state, identity discontinuity, timestamp regression, LOST lifecycle, determinism, uncertainty degradation, forbidden side-effect audit, no fabricated movement-coordinate audit, metric/frame mismatch, stale navigation evidence, malformed heading/uncertainty, and rejection of authoritative M1 input.

## Performance
HOST only, n=100000: mean 0.00491857134 ms; median 0.004517 ms; p95 0.004717 ms; max 0.877862 ms. Pi5/E2E NOT_VERIFIED.

## Control-side-effect audit
No serial/socket/radio/hardware/control imports. No UART, LoRa, ESP-NOW, PWM, DShot, PID, mixer, ESC, ARM, TAKEOFF, LAND, payload or actuation behavior. No command transmission.

## Production gates
NOT_VERIFIED: production M1 runtime integration; production M2 Guidance integration; exact production navigation inputs; Pi5 E2E; Master ESP32 transport; Flight Controller command acceptance; physical flight behavior.

## Known limitations
M2 is intentionally conservative and does not define autonomous intercept/search trajectories or observation-offset policy. stale_after_s=0.5 and degrade_uncertainty_m=5.0 are SHADOW test defaults, not production-authoritative thresholds. Future high-level command-boundary work must independently define transport schema and FC acceptance without changing M2 authority.
