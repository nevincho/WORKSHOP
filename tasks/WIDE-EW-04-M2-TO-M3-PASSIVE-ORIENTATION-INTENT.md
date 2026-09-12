# WIDE-EW-04 — M2 ORIENT_OBSERVATION_AXIS → M3 Passive High-Level Orientation Intent

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: COMPLETE
TYPE: ENGINEERING / PASSIVE M3 CONTRACT EXTENSION + DETERMINISTIC TESTS
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Create and independently validate the minimum passive M3 representation for accepted M2 `ORIENT_OBSERVATION_AXIS` guidance, stopping at M3.

## Upstream
`WideAcquisitionCue v1 -> MC1 -> M1 ACQUIRE / ORIENT_REQUEST_PENDING -> M2 ORIENT_OBSERVATION_AXIS`.
N1 remains excluded pre-confirmation.

## Scope
- inspect current/frozen documented M3 boundary and WIDE-EW-03 M2 handoff;
- classify M3 as REUSE_AS_IS or BOUNDED_EXTENSION_REQUIRED;
- define carrier-independent, non-metric M2→M3 representation;
- preserve deterministic HQ preemption, expiry/cancellation and fail-closed semantics;
- deterministic tests for valid LEFT/CENTER/RIGHT plus stale, malformed, invalid provenance, mission authority loss, HQ preemption, cancellation, unsupported semantic and no stale retention;
- prove no carrier adapter, FC, yaw, heading, actuator or command-send output.

## Protected
No modification to WideAcquisitionCue v1, MC1, M1, N1, HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, FC/carrier implementation, command-send authority, Pi5 or production. No legacy WIDE cleanup.

## Acceptance
PASS only if exact M2→M3 contract, schema-status classification, passive carrier-independent semantics, non-metric geometry, HQ preemption, expiry/cancellation, fail-closed behavior, bounded tests and independent review are present, with zero carrier/FC/physical command output.

## Completion
Independent review verdict: PASS.
Evidence: `evidence/WIDE-EW-04/RESULT.md`.
Review: `review/WIDE-EW-04.md`.

## STOP
WIDE-EW-04 is complete. Do not start another engineering unit in this cycle.