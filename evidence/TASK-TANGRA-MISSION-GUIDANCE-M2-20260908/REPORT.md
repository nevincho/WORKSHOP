# M2 Passive Guidance Decision / Translation Layer — Evidence

TASK_ID: TASK-TANGRA-MISSION-GUIDANCE-M2-20260908
STATUS: RE-REVIEW
BASE: M1 reviewed commit 88ffcf4932545304c5a82c83c65ad01b99000680; M1 COMPLETE metadata 4fc48e0a8bcb25807e84dd94d9e2c7c22ffd5cbd.
SCOPE: PASSIVE/SHADOW/non-authoritative translation only. No production integration. HOROS TASK8 untouched.

## Contract
GuidanceInput consumes the exact frozen M1 MissionDecision object plus optional NavigationEvidence and evaluated_at. Tests load the real frozen M1 implementation from its repository path. M2 validates M1_SHADOW_V1 and production_authority=False.

PassiveGuidanceDecision exposes GuidanceState {AVAILABLE, DEGRADED, SUPPRESSED}, semantic GuidanceIntent {NO_GUIDANCE,HOLD,ABORT_HOLD,MAINTAIN_OBSERVATION,REACQUIRE_TARGET,MOVE_RELATIVE,SET_ALTITUDE,SET_HEADING}, identity/time/frame, unchanged metric status, optional movement fields, reason/provenance, production_authority=False.

M2 never derives MOVE_RELATIVE/SET_ALTITUDE/SET_HEADING from target XYZ alone. Observation/track movement-coordinate fields remain null. REACQUIRE may preserve only an explicit externally supplied search_relative_vector_m when metric status is VERIFIED; no search trajectory is invented.

## M1 -> M2 mapping
NO_ACTION -> SUPPRESSED/NO_GUIDANCE.
HOLD -> AVAILABLE/HOLD.
ABORT -> AVAILABLE/ABORT_HOLD semantic only.
MISSION_COMPLETE -> AVAILABLE/HOLD.
OBSERVE_TARGET / MAINTAIN_TRACK -> geometry-gated MAINTAIN_OBSERVATION or NO_GUIDANCE; no fabricated movement.
REACQUIRE -> REACQUIRE_TARGET; without explicit search geometry remains DEGRADED semantic-only.
TARGET_LOST with non-REACQUIRE action -> SUPPRESSED.
M1 DEGRADED is always preserved as M2 DEGRADED and cannot be promoted to AVAILABLE.

## Gates
Identity/frame/timestamps must match and be fresh. LOST lifecycle suppresses navigation except semantic REACQUIRE. Metric mismatch suppresses. UNUSABLE/CONFLICT/INVALID => DEGRADED/HOLD. NOT_VERIFIED => DEGRADED without movement authority. Missing/malformed/non-finite geometry, heading, altitude or uncertainty fails closed. Missing carrier pose cannot produce world-frame movement. uncertainty >5m is a SHADOW-only degradation threshold.

## Independent review cycle 1
Candidate b19d5dd50c4593dd55a6ca474738fb1a34d98786: PASS_WITH_CONDITIONS. Finding: M1 DEGRADED + otherwise verified navigation could be promoted to M2 AVAILABLE. Bounded M2-only correction added upstream_degraded gate for observation and reacquisition paths. No M1, HOROS T8 or production paths changed.

## Validation after correction
30/30 HOST deterministic tests PASS, including two regressions proving DEGRADED OBSERVE_TARGET and DEGRADED REACQUIRE remain DEGRADED.

## Performance after correction
HOST only, n=100000: mean 0.00479664566 ms; median 0.004536 ms; p95 0.004717 ms; max 1.497449 ms. Pi5/E2E NOT_VERIFIED.

## Control side effects
NONE. No serial/socket/radio/hardware/control imports or UART, LoRa, ESP-NOW, PWM, DShot, PID, mixer, ESC, ARM, TAKEOFF, LAND, payload or actuation behavior.

## Production gates
NOT_VERIFIED: production M1 runtime integration; production M2 Guidance integration; exact production navigation inputs; Pi5 E2E; Master ESP32 transport; Flight Controller command acceptance; physical flight behavior.

## Known limitations
M2 intentionally defines no autonomous intercept/search trajectory or observation-offset policy. stale_after_s=0.5 and degrade_uncertainty_m=5.0 are SHADOW test defaults only. Future high-level command-boundary work remains separate.
