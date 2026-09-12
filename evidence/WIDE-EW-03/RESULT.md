# WIDE-EW-03 — Engineering Result

DATE: 2026-09-12
MODE: WORKSHOP ENGINEERING / NO RUNTIME INTEGRATION

## M1_OUTPUT
Accepted upstream semantic from WIDE-EW-02:
`ACQUIRE / ORIENT_REQUEST_PENDING` carrying only cue correlation, source/provenance, monotonic source time/expiry, normalized image x/y, signed normalized horizontal offset, LEFT/CENTER/RIGHT sector, bounded quality/persistence and mission-authority validity.

## M2_INPUT
Minimal passive adapter input is `M1OrientationRequest`. It contains no target identity, track identity, range, XYZ, bearing, yaw, heading, navigation evidence or command fields.

## M2_CONTRACT_STATUS
`BOUNDED_EXTENSION_REQUIRED`.

Current repository evidence documents frozen M2 Passive Guidance as consuming M1 mission decisions plus optional N1 NavigationEvidence for TRACK semantics and producing states such as `AVAILABLE/MAINTAIN_OBSERVATION`, `DEGRADED/REACQUIRE_TARGET`, or `SUPPRESSED/NO_GUIDANCE`. No existing frozen `ORIENT_OBSERVATION_AXIS` semantic is documented. Therefore reuse-as-is would require overloading unrelated TRACK/navigation semantics. This package adds only the minimal passive orientation semantic and does not redesign M2.

## ORIENT_OBSERVATION_AXIS_SEMANTICS
`ORIENT_OBSERVATION_AXIS` means only:
"An accepted M1 WIDE acquisition requests that the authoritative observation axis be oriented toward the supplied non-metric image-space direction."

It does not define how motion occurs and carries no actuator/carrier command semantics.

Reference M2 output:
- `status = AVAILABLE`
- `guidance_type = ORIENT_OBSERVATION_AXIS`
- cue correlation ID
- source/provenance
- expiry
- normalized image x/y
- signed normalized horizontal offset
- LEFT/CENTER/RIGHT sector
- reason/provenance status

## GEOMETRY_SEMANTICS
Image-space only:
- x/y normalized to `[0,1]`;
- signed horizontal offset in `[-1,1]` and consistent with `(image_x_norm - 0.5) * 2`;
- sector derived from the frozen WIDE center-half-width 0.20 rule.

No degree/radian bearing, yaw, heading, range, XYZ or carrier-relative metric frame is created.

## HQ_PREEMPTION
HQ authority is deterministic and dominant. If an authoritative HQ target is active, M2 WIDE orientation guidance is immediately suppressed as `NO_GUIDANCE / HQ_AUTHORITY_ACTIVE`. No WIDE override or secondary-attention exception is introduced.

## TIMEOUT_CANCEL_RULE
Guidance exists only while M1 remains `ACQUIRE / ORIENT_REQUEST_PENDING` and the acquisition remains within its inherited expiry window. Expired/future acquisition -> `SUPPRESSED / NO_GUIDANCE / STALE_ACQUISITION`. Cancelled/non-pending M1 state -> `SUPPRESSED / NO_GUIDANCE / ACQUISITION_NOT_PENDING`. No stale guidance is retained or renewed.

## FAIL_CLOSED_RULES
Suppress guidance on:
- invalid evaluation time;
- missing acquisition;
- M1 state/action not exactly `ACQUIRE / ORIENT_REQUEST_PENDING`;
- mission authority lost;
- active HQ authoritative target;
- source/provenance mismatch;
- non-finite/out-of-range normalized geometry;
- inconsistent x/offset/sector semantics;
- stale/future acquisition;
- malformed input/processing exception.

No failure path creates N1, HOROS, CurrentTarget, M3 or FC output.

## TEST_RESULTS
Deterministic offline Workshop reference validation: 11/11 PASS.
Required matrix:
- VALID_LEFT_ORIENT: PASS
- VALID_CENTER_ORIENT: PASS
- VALID_RIGHT_ORIENT: PASS
- STALE_ACQUISITION: PASS
- MALFORMED_DIRECTION: PASS
- INVALID_PROVENANCE: PASS
- MISSION_AUTHORITY_LOST: PASS
- HQ_AUTHORITY_PREEMPTS: PASS
- ACQUISITION_CANCELLED: PASS
- TIMEOUT_CLEARS_GUIDANCE: PASS
Additional scope invariant:
- no M3/command/yaw/heading/bearing/range/XYZ/target/track fields in output: PASS

Execution result: `Ran 11 tests ... OK`; 0 failures, 0 errors. Offline repository engineering validation only; no Pi5/runtime claim.

## M3_OUTPUT
NONE.

This package exposes no M3 adapter, command contract, FC transport or actuator output. M3 receives nothing in WIDE-EW-03.

## FILES
- `tasks/WIDE-EW-03-M1-TO-M2-PASSIVE-ORIENTATION-GUIDANCE.md`
- `handoffs/WIDE-EW-03/m2_orientation_guidance.py`
- `handoffs/WIDE-EW-03/test_m2_orientation_guidance.py`
- `evidence/WIDE-EW-03/RESULT.md`

## SCOPE_PROTECTION
No modification to WideAcquisitionCue v1 semantics, HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, M3, FC/carrier adapter, command-send authority, Pi5 or production. No legacy WIDE cleanup performed.

## ENGINEERING_VERDICT
PASS_CANDIDATE_FOR_INDEPENDENT_REVIEW
