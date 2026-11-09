# TANGRA-FC-SA-02-01 — Scout evidence and authorization boundary

DATE: 2026-11-09
CAMPAIGN: TANGRA-FC-SOFTWARE-AUTONOMY
TASK: TANGRA-FC-SA-02-01-COMMAND-ARBITRATION
SCOUT_RESULT: NOT_VERIFIED
IMPLEMENTATION: NOT_STARTED
REVIEW: NOT_STARTED
CHECKPOINT: NOT_CREATED

## Authoritative evidence read
- WORKSHOP canonical task and Scout assignment from main.
- WORKSHOP state index, profile and handoff.
- TANGRA-DOCS PR #13 open at head 1ce87e6a76822c757029be67ee9bccb342774d0a (verified 2026-11-09).
- TANGRA-DOCS ARCHITECTURE/TANGRA_FLIGHT_CONTROL_ARCHITECTURE.md at PR #13.
- TANGRA-DOCS REPORTS/TANGRA_FC_COM13_PASSIVE_VALIDATION_20261108.md at PR #13.

## Observed existing architecture and qualification
- USB/MAVLink directly connects Pi5 and the custom ESP32 FC; Master ESP32 is not an FC hop.
- Mission Lifecycle v1 is documented as implemented and host-tested with states INIT/READY/ACTIVE/HOLD/ABORT/COMPLETE/FAULT.
- Current documented hardware candidate is TANGRA-FC-HW-DIAG-MPU-SCHED-02 / 0.9.1-hw-diag-candidate, with hardware read-back, bounded roll/pitch, MPU ~250 Hz, fresh BMP280, SCH_OVR=0, SENS_ERR=0, zero captured MAVLink CRC errors, and lifecycle telemetry retained.
- Documentation reports corrected gravity-inclusive accelerometer offset handling and UART diagnostic TX blocking.
- Physical actuator outputs and arming remain OFF.

## Missing authoritative inspection
The exact current Windows-local FC source tree under D:\RaspberryPi5\TANGRA\WORKSPACE\TANGRA_FC_ESP32 was NOT INSPECTED in this execution environment.
Therefore the present implementation of source-tagged arbitration, priority/preemption, ownership, stale-input rejection and Safety Supervisor integration is NOT VERIFIED. Exact source files, modification boundaries and existing tests are NOT VERIFIED.
Do not treat this as proof that arbitration is absent or incomplete.

## Engineering gate
Planner and Worker must not invent a missing implementation, file list, diff or PASS.
The current evidence is sufficient for coordination and a bounded passive safety review, not for a verified implementation change.
Allowed immediate non-actuating follow-up: examine existing diagnostics and fail-safe/safety-off telemetry or review supplied source/test evidence, without implementing autonomous guidance, navigation, waypoint execution or command-to-actuation capability.

## Classification
- SOURCE_EVIDENCE: NOT_VERIFIED
- DUPLICATE_IMPLEMENTATION_RISK: UNKNOWN
- IMPLEMENTATION_READY: NO
- NEXT_ROUTE: CONTROL_ROOM_RECONCILE
- CHAIN: STOP before Planner/Worker implementation; no STEP_3 unlock.

This record is a Scout evidence record only; it is not an independent Reviewer verdict or validated software checkpoint.
