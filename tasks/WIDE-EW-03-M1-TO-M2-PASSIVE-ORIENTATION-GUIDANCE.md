# WIDE-EW-03 — M1 Acquisition State → M2 Passive Orientation Guidance

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: COMPLETE
TYPE: ENGINEERING / PASSIVE M2 CONTRACT EXTENSION + DETERMINISTIC TESTS
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Create and independently validate the minimum passive transformation from accepted M1 `ACQUIRE / ORIENT_REQUEST_PENDING` into carrier-independent M2 `ORIENT_OBSERVATION_AXIS` guidance.

## Upstream
`WideAcquisitionCue v1 -> MC1 validation -> AcquisitionInput -> M1 ACQUIRE / ORIENT_REQUEST_PENDING`.
N1 remains excluded pre-confirmation.

## Scope
- inspect only current M1 acquisition output and current documented M2 Passive Guidance semantics;
- determine `REUSE_AS_IS` versus `BOUNDED_EXTENSION_REQUIRED`;
- define the minimum M1→M2 non-metric contract;
- implement passive `ORIENT_OBSERVATION_AXIS` reference transformation;
- fail closed on stale/cancelled/inconsistent/unauthorized input and HQ authority preemption;
- deterministic tests for LEFT/CENTER/RIGHT, stale, malformed, invalid provenance, mission authority loss, HQ preemption, cancellation and timeout clearing.

## Protected
No modification to WideAcquisitionCue v1, HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, M3, FC/carrier adapter, command-send authority, Pi5 or production. No metric bearing/yaw/heading/range/XYZ semantics.

## Acceptance result
Independent review: PASS.
M2 contract status: `BOUNDED_EXTENSION_REQUIRED`.
Deterministic tests: 11/11 PASS.
Evidence: `evidence/WIDE-EW-03/RESULT.md`.
Review: `review/WIDE-EW-03.md`.
M3 output: NONE.

## STOP
WIDE-EW-03 complete. Do not start WIDE-EW-04 in this cycle.