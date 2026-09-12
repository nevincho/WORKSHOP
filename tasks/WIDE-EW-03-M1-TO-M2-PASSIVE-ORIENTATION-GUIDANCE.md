# WIDE-EW-03 — M1 Acquisition State → M2 Passive Orientation Guidance

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: IN_PROGRESS
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

## Acceptance
PASS only if exact M1→M2 contract, `ORIENT_OBSERVATION_AXIS` semantics, contract-status classification, non-metric preservation, HQ preemption, expiry/cancellation, fail-closed behavior, bounded tests and independent review are present, and M3 receives nothing.

## STOP
After independent review, STOP. Do not start WIDE-EW-04.