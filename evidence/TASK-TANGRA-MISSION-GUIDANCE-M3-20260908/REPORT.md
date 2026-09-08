# M3 High-Level Command Contract — Evidence

TASK_ID: TASK-TANGRA-MISSION-GUIDANCE-M3-20260908
STATUS: RE-REVIEW
BASE_M1_REVIEWED: 88ffcf4932545304c5a82c83c65ad01b99000680
BASE_M2_REVIEWED: 75417cb4356a79e61d1196f3f859fa7cd7ba08e8
BASE_M2_METADATA: 66df7d43b5df2b9cca39143677b9c89acd0fe4bb
M2_IMPLEMENTATION_BLOB: 5616d5930c8ffca0cef7876d6c192bc7627efb2c
REVIEW_CYCLE_1: PASS_WITH_CONDITIONS — source M2 reason was not preserved as a distinct field.
CORRECTION: added source_guidance_reason and regression coverage; no M1/M2 change.

## Contract
M3 consumes the frozen M2 PassiveGuidanceDecision only. It does not consume target XYZ, carrier state, trajectory state, or hardware state. Output PassiveHighLevelCommand preserves M2 source state/intent/reason, target reference, source timestamp, frame_ref, metric status and provenance; production_authority is always False.

Command vocabulary: NO_COMMAND, HOLD, MOVE_RELATIVE, SET_ALTITUDE, SET_HEADING. ARM, DISARM, TAKEOFF and LAND are reserved compatibility enum values only and are never generated.

## Deterministic mapping
NO_GUIDANCE -> NO_COMMAND.
HOLD -> HOLD.
ABORT_HOLD -> HOLD with abort_semantic=True; no DISARM/LAND/actuation.
MAINTAIN_OBSERVATION -> NO_COMMAND; M3 never derives movement.
REACQUIRE_TARGET -> NO_COMMAND; M3 never derives search geometry.
MOVE_RELATIVE / SET_ALTITUDE / SET_HEADING -> preserve-only when M2 state=AVAILABLE, metric=VERIFIED, reference frame is explicit, and the corresponding numeric parameter already exists and is finite.

## Authority gates
M2 contract_version must be M2_SHADOW_V1 and production_authority must be False. SUPPRESSED input cannot produce a command. DEGRADED movement cannot produce movement. NOT_VERIFIED/UNUSABLE/CONFLICT/INVALID metric evidence cannot produce movement. Timestamp regression, stale guidance, target discontinuity, frame discontinuity, missing reference frame, missing parameter and non-finite values fail closed. No coordinate conversion is performed.

## Tests
29/29 deterministic HOST tests PASS, including exact reviewed M2 module import in repository test, required task matrix, source-reason preservation, wrong contract version, authoritative-M2 rejection, reserved-command non-generation and frame continuity.

## Performance
HOST-only n=100000 mean=0.00544667126 ms median=0.003906 ms p95=0.004116 ms max=37.810173 ms. Max is a host/runtime scheduling outlier. No Pi5 inference.

## Side-effect audit
No UART, serial, LoRa, ESP-NOW, socket/network, PWM, DShot, PID, mixer, ESC, motor, payload, release or weapon behavior. No hardware access or production integration.

## Production gates
NOT_VERIFIED: M1/M2/M3 runtime integration; Pi5 E2E; production movement geometry; Master ESP32 transport; ACK/heartbeat behavior; Flight Controller command acceptance; physical flight.

## Known limitations / future integration
M3 is a semantic command contract only. It does not define serialization, command IDs, ACK/retry/heartbeat, transport framing, FC acceptance semantics, units negotiation, or coordinate-frame conversion. A future transport task must consume PassiveHighLevelCommand without upgrading authority and must leave FC safety/failsafe final authority unchanged.

M1_MODIFIED: NO
M2_MODIFIED: NO
HOROS_TASK8_TOUCHED: NO
M4_STARTED: NO
