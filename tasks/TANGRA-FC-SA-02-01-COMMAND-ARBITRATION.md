# TANGRA-FC-SA-02-01 — Command-Source Arbitration + Safety Ownership

PROJECT: TANGRA
CAMPAIGN: TANGRA-FC-SOFTWARE-AUTONOMY
STEP: 2
STATUS: BLOCKED
ROUTE: CONTROL_ROOM_RECONCILE
SCOUT_EVIDENCE: evidence/TANGRA-FC-SA-02-01/SCOUT.md
BLOCKER: Windows-local FC implementation source not inspected; exact arbitration gap NOT_VERIFIED
CREATED: 2026-11-09
AUTHORIZATION: EXPLICIT_HUMAN_AUTHORIZATION

## Objective

Determine the actual current implementation state for command-source arbitration and Safety Supervisor ownership in the custom TANGRA ESP32 Flight Controller, then prepare the smallest implementation-ready STEP_2 boundary without implementing production code during Scout/Prep.

Conceptual command sources to reconcile:
- simulated autonomy;
- Raspberry Pi supervisor as an abstract/source-tagged host-fixture input only;
- bench/test source;
- safety override.

Safety must always have highest authority. Raspberry Pi must never obtain motor-level authority.

## Authoritative inputs

Scout must read:
- applicable WORKSHOP policies and role definitions;
- `registry/PROJECTS.md`;
- `registry/CONNECTIONS.md`;
- `projects/TANGRA.md`;
- `status/WORKSHOP_STATE.yaml`;
- `control_room/CURRENT.md`;
- current TANGRA canonical evidence at `nevincho/TANGRA-DOCS` PR #13, verified head at task creation `1ce87e6a76822c757029be67ee9bccb342774d0a`;
- relevant existing TANGRA FC tasks/evidence/checkpoints;
- current authoritative FC source/runtime evidence where accessible.

Recorded source path from TANGRA evidence:
`D:\\RaspberryPi5\\TANGRA\\WORKSPACE\\TANGRA_FC_ESP32`.

If direct current-source inspection is unavailable to Scout, mark the precise facts `NOT VERIFIED`; do not infer missing implementation state from stale WORKSHOP summaries.

## Known current evidence

Already present and protected:
- Mission Lifecycle v1 with INIT/READY/ACTIVE/HOLD/ABORT/COMPLETE/FAULT;
- guarded transitions, timeout handling, duplicate and stale/out-of-order rejection, communication-loss HOLD -> ABORT and deterministic trace;
- passive lifecycle telemetry MSTATE/MREASON/MSEQ;
- sensor acquisition/health/freshness;
- corrected approximately 90-degree MPU transform behavior;
- estimator;
- cascaded attitude/rate controller;
- virtual Quad-X mixer;
- cooperative scheduler;
- safety state;
- MAVLink telemetry;
- deterministic host-test infrastructure.

Current installed bench candidate:
- build `TANGRA-FC-HW-DIAG-MPU-SCHED-02`;
- version `0.9.1-hw-diag-candidate`;
- MPU6050 approximately 250 Hz;
- BMP280 fresh;
- SENS_ERR=0;
- SCH_OVR=0;
- repeated MAVLink capture CRC errors=0;
- stable bounded roll/pitch;
- lifecycle telemetry preserved;
- exact firmware installation/read-back verified.

Closed defects must not be reopened absent new evidence:
1. gravity-inclusive accelerometer calibration causing attitude divergence;
2. blocking UART diagnostics causing scheduler overruns.

## Scout requirements

Determine and persist:
1. whether arbitration, source ownership, priority/preemption, or Safety Supervisor integration already exists in whole or in part;
2. exact relevant files/modules/interfaces;
3. what is already validated versus merely present;
4. dependencies and prerequisites;
5. protected components and interfaces;
6. duplicate-work risk;
7. current phase and actual missing functionality;
8. validation prerequisites;
9. the smallest useful implementation boundary for Planner;
10. whether Worker authority is likely sufficient or whether later routing may require `ROUTE=CODEX_CANDIDATE`.

Scout must not implement production code.

## STEP_2 boundaries

In scope for the eventual implementation unit:
- source-tagged arbitration model;
- deterministic authority/priority rules;
- safety override as highest authority;
- explicit selected-source/decision observability where needed for validation;
- host fixtures for simulated autonomy, abstract Pi supervisor and bench/test sources;
- integration with existing Safety Supervisor/safety state only to the smallest extent proven necessary by repository evidence;
- deterministic host tests.

Explicitly out of scope:
- STEP_3 vehicle dynamics simulation;
- STEP_4+ navigation/altitude/local-position/guidance work;
- STEP_8 live Pi mission contracts, ACK/NACK, reconnect or resynchronization;
- live Pi command authority;
- physical arming or actuator output;
- motor/ESC operation;
- production Pi5 runtime changes;
- targeting/interception;
- broad redesign/refactor/tuning.

## Acceptance for Scout/Prep

Scout/Prep is complete only when WORKSHOP evidence establishes:
- current arbitration implementation status from authoritative evidence;
- already-complete portions versus actual gap;
- exact affected/protected components;
- a dependency-correct, non-duplicative smallest boundary suitable for Planner;
- a validation method that measures arbitration/safety ownership rather than future-phase behavior.

Scout output path:
`evidence/TANGRA-FC-SA-02-01/SCOUT.md`.

## Next route

On satisfactory Scout evidence:
SCOUT/PREP -> PLANNER.

Do not route directly to Worker.
Do not create or start STEP_3.
