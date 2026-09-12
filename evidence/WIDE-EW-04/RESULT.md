# WIDE-EW-04 — Engineering Result

DATE: 2026-09-12
MODE: WORKSHOP ENGINEERING / NO RUNTIME INTEGRATION

## M2_OUTPUT
Accepted upstream semantic is passive M2 `ORIENT_OBSERVATION_AXIS`, carrying only cue correlation/provenance, expiry, normalized image x/y, signed normalized horizontal offset and LEFT/CENTER/RIGHT sector.

## M3_INPUT
Reference `M2OrientationGuidance` fields consumed by M3:
- `status`
- `guidance_type`
- `cue_id`
- `source`
- `provenance`
- `timestamp_monotonic_s`
- `expires_at_s`
- `image_x_norm`
- `image_y_norm`
- `horizontal_offset_norm`
- `sector`
- `mission_authority_valid`

No target identity, track identity, bearing, yaw, heading, range, XYZ or actuator field is consumed.

## M3_CONTRACT_STATUS
`BOUNDED_EXTENSION_REQUIRED`.

Current authoritative checkpoint establishes frozen M3 as passive representation-only high-level command contract with no transport/FC/hardware authority. Current repository evidence does not establish an existing frozen M3 `ORIENT_OBSERVATION_AXIS` representation. Therefore the existing M3 authority boundary is reused, while one bounded passive orientation-intent semantic is added in this engineering package. M3 is not redesigned.

## M3_ORIENTATION_INTENT
`M3PassiveOrientationIntent` represents only:
"An accepted high-level request exists to orient the authoritative observation axis toward this validated non-metric image-space direction."

Valid representation:
- `status = VALID`
- `intent_type = ORIENT_OBSERVATION_AXIS`
- cue correlation/source/provenance
- expiry
- normalized image x/y
- signed normalized horizontal offset
- LEFT/CENTER/RIGHT sector

Suppressed representation contains `NO_INTENT` and clears all cue/direction fields.

M3 does not decide carrier motion or create transport/command authority.

## GEOMETRY_SEMANTICS
Strictly non-metric image-space semantics. M3 validates consistency:
`horizontal_offset_norm = (image_x_norm - 0.5) * 2`
and sector must match the frozen LEFT/CENTER/RIGHT split with center half-width 0.20.

No conversion to degrees/radians/bearing/yaw/heading/range/XYZ exists.

## CARRIER_BOUNDARY
M3 terminates at a passive semantic boundary:
`M2 ORIENT_OBSERVATION_AXIS -> M3 passive orientation intent -> [future carrier adapter, NOT IMPLEMENTED]`.

Future carrier adapter responsibility is only architectural interpretation: determine whether/how the specific carrier can safely realize the request. Quadrotor yaw, gimbal pan/tilt, turret pan or fixed-wing heading/turn remain future carrier-specific realizations and are absent from this package.

## HQ_PREEMPTION
If authoritative HQ target is active, M3 immediately returns `SUPPRESSED / NO_INTENT / HQ_AUTHORITY_ACTIVE`. No WIDE intent competes with HQ authority and no previous intent is retained.

## TIMEOUT_CANCEL_RULE
- future/stale/expired M2 guidance -> `NO_INTENT / STALE_GUIDANCE`;
- M2 status not AVAILABLE, including cancellation/suppression -> `NO_INTENT / GUIDANCE_SUPPRESSED_OR_CANCELLED`;
- no latching or stale-intent retention exists; every call derives a fresh representation from current validated M2 input.

## FAIL_CLOSED_RULES
Suppress/clear intent on:
- invalid/non-finite evaluation time;
- HQ authoritative target active;
- missing M2 guidance;
- mission authority lost;
- M2 guidance suppressed/cancelled;
- unsupported semantic type;
- source/provenance mismatch;
- malformed/non-finite/out-of-range geometry;
- expiry earlier than source timestamp;
- inconsistent normalized x / signed offset / sector;
- future/stale/expired guidance;
- processing/attribute error.

No failure path creates carrier/FC output or physical command.

## TEST_RESULTS
Deterministic Workshop engineering execution:
- VALID_LEFT_INTENT: PASS
- VALID_CENTER_INTENT: PASS
- VALID_RIGHT_INTENT: PASS
- STALE_GUIDANCE: PASS
- MALFORMED_DIRECTION: PASS
- INVALID_PROVENANCE: PASS
- MISSION_AUTHORITY_LOST: PASS
- HQ_AUTHORITY_PREEMPTS: PASS
- ACQUISITION_CANCELLED: PASS
- UNSUPPORTED_SEMANTIC: PASS
- NO_STALE_INTENT_RETENTION: PASS

Required acceptance scenarios: 11/11 PASS.

Additional invariant check: PASS — finalized M3 intent object contains none of the forbidden physical/control fields: yaw/yaw_deg/yaw_rate, heading/heading_deg, bearing/bearing_deg, range/range_m, xyz, target_id, track_id, motor, servo, pwm, actuator, fc_command, carrier_command, command_send.

Validation is repository/offline engineering evidence only; no Pi5/runtime/production claim is made.

## FC_OUTPUT
NONE.

## CARRIER_ADAPTER_OUTPUT
NONE.

## YAW_COMMAND
NONE.

## HEADING_COMMAND
NONE.

## ACTUATOR_COMMAND
NONE.

## COMMAND_AUTHORITY
`COMMAND_SEND = UNTOUCHED / NOT ENABLED BY THIS PACKAGE`.
No transport, FC adapter, command packet or actuator path is present.

## FILES
- `tasks/WIDE-EW-04-M2-TO-M3-PASSIVE-ORIENTATION-INTENT.md`
- `handoffs/WIDE-EW-04/m3_orientation_intent.py`
- `handoffs/WIDE-EW-04/test_m3_orientation_intent.py`
- this evidence file

## SCOPE_PROTECTION
No modification to WideAcquisitionCue v1, MC1, M1, N1, HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, FC/carrier implementation, command-send authority, Pi5 or production. No legacy WIDE cleanup performed.

## ENGINEERING_VERDICT
PASS_CANDIDATE_FOR_INDEPENDENT_REVIEW
