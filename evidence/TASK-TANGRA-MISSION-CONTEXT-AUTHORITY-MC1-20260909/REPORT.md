# Mission Context Authority — Evidence

TASK_ID: TASK-TANGRA-MISSION-CONTEXT-AUTHORITY-MC1-20260909
STATUS: READY_FOR_INDEPENDENT_REVIEW
BASE_M1_REVIEWED: 88ffcf4932545304c5a82c83c65ad01b99000680
BASE_M2_COMPLETE: 66df7d43b5df2b9cca39143677b9c89acd0fe4bb
SCOPE: isolated passive/non-production mission-context authority contract only.

## Purpose
Provide exactly the four explicit runtime inputs required by frozen M1 without inferring mission authority from perception, HOROS, T7, connectivity, dashboard labels, generic ACTIVE state, or generated telemetry.

## Field semantics and owners
- mission_active: explicit mission-session activation/deactivation. Owner: MISSION_ACTIVATION_AUTHORITY.
- operator_intent: explicit operator mission-level intent NONE/OBSERVE/TRACK/HOLD/COMPLETE/ABORT. Owner: OPERATOR_INTENT_AUTHORITY.
- system_ready: explicit Pi mission-runtime readiness statement from a future designated readiness authority. It is not detector state, HOROS validity, generic runtime ACTIVE, or connectivity. Owner: SYSTEM_READINESS_AUTHORITY.
- safety_available: explicit availability statement from a future designated safety authority, ultimately subordinate to Flight Controller safety/final flight authority. It is not connectivity or permission to actuate. Owner: SAFETY_AVAILABILITY_AUTHORITY.

## Update contract
Each field may be updated only through its dedicated setter with an AuthorityStamp(owner, source_ref, revision).
Owner must match the field. source_ref must be non-empty. revision must be a non-negative integer and strictly increase for the same source. A source change requires explicit reset_authorities() before acceptance. No perception-derived or telemetry-derived setters exist.

## Fail-closed mapping
A context is fully authoritative only when all four values and all four authority stamps are present.
If any authority is unavailable:
- mission_active -> False
- system_ready -> False
- safety_available -> False
- operator_intent -> NONE, except an explicitly authoritative ABORT or HOLD is preserved because it is safety-conservative.
- authoritative -> False with explicit missing-authority reasons.
No TRACK/OBSERVE/COMPLETE intent is promoted through an incomplete authority context.

## M1 mapping
When fully authoritative, map values 1:1 into frozen M1:
mission_active -> MissionInput.mission_active
operator_intent.value -> frozen M1 OperatorIntent(value)
system_ready -> MissionInput.system_ready
safety_available -> MissionInput.safety_available
The package does not alter any other M1 field or M1 decision semantics.

## Authority boundaries
Pi remains mission-level decision layer only.
Master ESP32 transport/communications is outside scope.
Flight Controller remains final stabilization/safety/motor authority.
No motor, actuator, ARM, TAKEOFF, LAND, UART, LoRa, ESP-NOW, PWM, DShot, PID, mixer, ESC, socket, or hardware behavior is implemented.

## Protected architecture
P-HQ, P-DET, P-NANO, P-CA, P-CT, P-HOROS, P-PROD unchanged.
Frozen M1 and M2 unchanged.

## Validation
19/19 deterministic local unit tests PASS.
Coverage includes all-unavailable fail closed, exact four-authority mapping, non-inference, owner mismatch, missing source, monotonic revision, source takeover rejection, reset, explicit false, malformed types, no production authority, no control/transport side effects, forbidden perception/HOROS context inputs, determinism, and partial-context conservative intent handling.

PRODUCTION_INTEGRATION: NO
PRODUCTION_AUTHORITY: FALSE
INDEPENDENT_REVIEW: PENDING
