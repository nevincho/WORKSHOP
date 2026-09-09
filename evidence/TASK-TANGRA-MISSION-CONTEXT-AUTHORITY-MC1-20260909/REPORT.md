# Mission Context Authority — Evidence

TASK_ID: TASK-TANGRA-MISSION-CONTEXT-AUTHORITY-MC1-20260909
STATUS: READY_FOR_INDEPENDENT_REREVIEW
BASE_M1_REVIEWED: 88ffcf4932545304c5a82c83c65ad01b99000680
BASE_M2_COMPLETE: 66df7d43b5df2b9cca39143677b9c89acd0fe4bb
PRIOR_CANDIDATE: e46b73f598b6bc2a404bddafa6cbb1523153c451
PRIOR_REVIEW_RESULT: FAIL
SCOPE: bounded authority-boundary repair only.

## Reviewed defect
The prior `map_to_m1_context()` trusted arbitrary directly-constructed `MissionContext` objects and only tested whether values/stamps were present. This bypassed `MissionContextStore` owner/source/revision validation.

## Bounded repair
`map_to_m1_context()` now independently validates every public input field at the mapping boundary:
- mission_active: exact bool + matching MISSION_ACTIVATION authority stamp
- operator_intent: exact OperatorIntent + matching OPERATOR_INTENT authority stamp
- system_ready: exact bool + matching SYSTEM_READINESS authority stamp
- safety_available: exact bool + matching SAFETY_AVAILABILITY authority stamp
- each stamp must be AuthorityStamp with explicit non-whitespace source_ref and non-negative integer revision
- exact AuthorityStamp, AuthorityOwner, OperatorIntent and MissionContext public types are enforced at the trust boundary

The mapper does not trust construction through `MissionContextStore`.
Non-MissionContext inputs fail closed without propagating an exception.

## Fail-closed behavior
If any field/value/stamp validation fails:
- authoritative=False
- mission_active=False
- system_ready=False
- safety_available=False
- operator_intent=NONE

Exception: HOLD or ABORT is preserved only when its own OperatorIntent value and authority stamp independently validate. TRACK/OBSERVE/COMPLETE are never preserved through incomplete/forged context.

## Store behavior
Existing dedicated setter semantics remain:
- exact owner per field
- explicit source_ref
- non-negative integer revision
- strictly monotonic revision for same source
- source replacement requires explicit reset_authorities()
- reset drops all authority

## M1 compatibility
No frozen M1 or M2 file changed. Mapping remains exactly:
mission_active -> frozen M1 MissionInput.mission_active
operator_intent.value -> frozen M1 OperatorIntent(value)
system_ready -> frozen M1 MissionInput.system_ready
safety_available -> frozen M1 MissionInput.safety_available

## Validation
40/40 deterministic local unit tests PASS after second bounded repair.
The original 19 tests are retained. Direct-boundary adversarial coverage includes wrong owners, one wrong owner, empty/whitespace source, malformed revision, wrong value types, mixed valid/forged stamps, missing stamps, fully valid direct context, exact prior forged TRACK reproduction, authoritative HOLD/ABORT, forged HOLD rejection, non-context input, repeated determinism, raw string-typed AuthorityOwner rejection, MissionContext subclass rejection, and AuthorityStamp subclass rejection.

## Independent review history
REREVIEW_CYCLE_1: FAIL at 83e00fac2dd5f5003577bc2459cf25b01d0f5a5b — raw string AuthorityOwner values could satisfy str-Enum equality.
SECOND_BOUNDED_REPAIR: exact public boundary types are now required for MissionContext, AuthorityStamp, AuthorityOwner and OperatorIntent.
INDEPENDENT_REREVIEW_CYCLE_2: PENDING

## Side-effect audit
No control/transport/hardware behavior added. No ARM/TAKEOFF/LAND/PWM/DShot/PID/mixer/ESC. Pi remains mission-level only; Flight Controller remains final stabilization/safety/motor authority.

PRODUCTION_INTEGRATION: NO
PRODUCTION_AUTHORITY: FALSE
FROZEN_M1_MODIFIED: NO
FROZEN_M2_MODIFIED: NO
