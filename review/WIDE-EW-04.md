# WIDE-EW-04 — Independent Review

DATE: 2026-09-12
REVIEW_SCOPE: M2 ORIENT_OBSERVATION_AXIS -> passive M3 orientation intent
VERDICT: PASS

## Acceptance review

### Exact M2 -> M3 contract
PASS. Input/output are explicit and limited to current passive WIDE acquisition semantics.

### M3 schema status
PASS. Classification is `BOUNDED_EXTENSION_REQUIRED`. Existing frozen M3 authority boundary is preserved; repository evidence does not establish a frozen `ORIENT_OBSERVATION_AXIS` M3 semantic, so one bounded passive representation is added without redesign.

### Passive carrier-independent semantics
PASS. M3 represents only that the authoritative observation axis should be oriented toward the validated non-metric image-space direction. It does not decide how a carrier moves.

### Non-metric preservation
PASS. Only normalized x/y, signed normalized horizontal offset and LEFT/CENTER/RIGHT sector are represented. No bearing/yaw/heading/range/XYZ conversion exists.

### HQ preemption
PASS. HQ authority deterministically suppresses M3 WIDE intent and clears cue/direction fields.

### Expiry/cancellation
PASS. Stale/future/expired or suppressed/cancelled M2 guidance produces `NO_INTENT`; no stale M3 state is retained.

### Fail-closed behavior
PASS. Missing guidance, invalid time, mission authority loss, unsupported semantic, invalid provenance, malformed/inconsistent geometry and HQ preemption all suppress output.

### Deterministic tests
PASS.
- VALID_LEFT_INTENT
- VALID_CENTER_INTENT
- VALID_RIGHT_INTENT
- STALE_GUIDANCE
- MALFORMED_DIRECTION
- INVALID_PROVENANCE
- MISSION_AUTHORITY_LOST
- HQ_AUTHORITY_PREEMPTS
- ACQUISITION_CANCELLED
- UNSUPPORTED_SEMANTIC
- NO_STALE_INTENT_RETENTION

11/11 required scenarios PASS. Additional forbidden-field invariant PASS.

### Physical/control authority absence
PASS.
- FC_OUTPUT = NONE
- CARRIER_ADAPTER_OUTPUT = NONE
- YAW_COMMAND = NONE
- HEADING_COMMAND = NONE
- ACTUATOR_COMMAND = NONE
- COMMAND_SEND = UNTOUCHED / NOT ENABLED

### Protected scope
PASS. No modification to WideAcquisitionCue v1, MC1, M1, N1, HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, FC/carrier implementation, command-send authority, Pi5 or production.

## Review conclusion
WIDE-EW-04 satisfies the bounded engineering acceptance criteria as an independently reviewable passive M3 representation package. It introduces no carrier, FC, transport or physical command authority.

No Codex or production promotion is authorized by this PASS.
