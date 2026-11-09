# TANGRA FC Software Autonomy Campaign

CAMPAIGN: TANGRA-FC-SOFTWARE-AUTONOMY
PROJECT: TANGRA
STATUS: ACTIVE
CREATED: 2026-11-09
AUTHORIZATION: EXPLICIT_HUMAN_AUTHORIZATION
COORDINATION_AUTHORITY: WORKSHOP
IMPLEMENTATION_AUTHORITY: authoritative TANGRA repository/runtime evidence

## Scope

Authorized:
- repository-safe software development;
- deterministic simulation and host tests;
- contracts/schemas;
- non-actuating FC firmware development;
- bench-safe diagnostic software;
- documentation, independent review and checkpointing.

Not authorized:
- physical motor/ESC operation;
- propulsive or autonomous physical flight;
- targeting/interception implementation;
- production Pi5 runtime modification;
- unrelated TANGRA production modification.

Physical actuator authority and arming remain OFF.

## Authoritative baseline

- Canonical docs: `nevincho/TANGRA-DOCS`, PR #13.
- Verified PR state at campaign creation: OPEN, head `1ce87e6a76822c757029be67ee9bccb342774d0a`.
- Current FC source location recorded by TANGRA evidence: `D:\\RaspberryPi5\\TANGRA\\WORKSPACE\\TANGRA_FC_ESP32`.
- Architecture: Raspberry Pi 5 <-> USB/MAVLink <-> custom ESP32 FC.
- Master ESP32 excluded from FC architecture.
- Current installed bench candidate: `TANGRA-FC-HW-DIAG-MPU-SCHED-02` / `0.9.1-hw-diag-candidate`.
- Mission Lifecycle v1 is complete in current evidence.
- Resolved attitude-divergence and scheduler-overrun defects remain CLOSED unless new evidence reopens them.

## Dependency graph

STEP_1 Mission Lifecycle v1 -> COMPLETE
STEP_2 Command-source arbitration + Safety Supervisor integration -> ACTIVE
STEP_3 Closed-loop Quad-X vehicle simulation -> LOCKED on STEP_2 PASS + checkpoint
STEP_4 Vertical state and altitude stack -> LOCKED on STEP_3
STEP_5 Local position and velocity model -> LOCKED on prior required state contracts
STEP_6 Horizontal guidance/local-position control -> LOCKED on STEP_5
STEP_7 Waypoint/trajectory executor -> LOCKED on guidance + Mission Lifecycle reuse
STEP_8 Pi supervisor/MAVLink contract -> LOCKED on internal mission/navigation contracts
STEP_9 Versioned parameters/persistence -> DEFER until interfaces stabilize
STEP_10 Watchdog/reset-cause integration -> DEFER until runtime contracts stabilize
STEP_11 GNSS + compass integration -> DEFER until local navigation contracts exist
STEP_12 Mission Planner compatibility -> DEFER until internal mission model/protocol are stable

No dependent implementation unit may run in parallel.

## Protected components

Preserve by default:
- MPU6050 driver;
- BMP280 driver;
- corrected estimator behavior;
- current scheduler behavior;
- cascaded attitude/rate controller;
- virtual Quad-X mixer;
- Mission Lifecycle v1;
- existing MAVLink compatibility;
- safety-off physical-output state;
- rollback capability.

## Current first unit

Canonical task: `TANGRA-FC-SA-02-01-COMMAND-ARBITRATION.md`.

Routing state: READY -> Scout/Prep.

Scout must determine current implementation before Planner or Worker routing. No STEP_3 or later task is created by this campaign record.
