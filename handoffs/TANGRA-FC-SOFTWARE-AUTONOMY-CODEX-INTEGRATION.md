# TANGRA FC Software Autonomy — Codex Integration Handoff

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-11-09

## Objective

Integrate the reviewed standalone WORKSHOP software into the authoritative local custom ESP32 FC with the smallest compatibility adaptations. Do not recreate the modules.

Authoritative local source:
`D:\RaspberryPi5\TANGRA\WORKSPACE\TANGRA_FC_ESP32`

Architecture:
`Pi5 <-> USB/MAVLink <-> custom ESP32 FC`.
Master ESP32 excluded.

## Reviewed software packages

- STEP_2: `handoffs/TANGRA-FC-SA-02-01_COMMAND_ARBITRATION_PACKAGE/`
- STEP_3: `handoffs/TANGRA-FC-SA-03-01-QUADX-SIM_PACKAGE/`
- STEP_4: `handoffs/TANGRA-FC-SA-04-01-VERTICAL_PACKAGE/`
- STEP_5: `handoffs/TANGRA-FC-SA-05-01-LOCAL-STATE_PACKAGE/`
- STEP_6: `handoffs/TANGRA-FC-SA-06-01-GUIDANCE_PACKAGE/`
- STEP_7: `handoffs/TANGRA-FC-SA-07-01-WAYPOINT-EXECUTOR_PACKAGE/`
- STEP_8: `handoffs/TANGRA-FC-SA-08-01-MISSION-PROTOCOL_PACKAGE/`
- STEP_9: `handoffs/TANGRA-FC-SA-09-01-PARAMETERS_PACKAGE/`
- STEP_10: `handoffs/TANGRA-FC-SA-10-01-WATCHDOG_PACKAGE/`
- STEP_11: `handoffs/TANGRA-FC-SA-11-01-GNSS-COMPASS_PACKAGE/`
- STEP_12: `handoffs/TANGRA-FC-SA-12-01-MISSION-PLANNER_PACKAGE/`

Cross-module integration:
`handoffs/TANGRA-FC-SOFTWARE-AUTONOMY_INTEGRATION_PACKAGE/`

## Integration adapters required

1. Map local FC setpoint/clock/bench/safety inputs to STEP_2 arbitration.
2. Bind existing controller/mixer/estimator to STEP_3 adapter interfaces.
3. Map estimator/barometer Z/VZ and vertical output to existing controller path.
4. Bind local navigation producers to STEP_5 state contract.
5. Bind STEP_6 attitude-style setpoints to existing attitude controller with arbitration/safety upstream.
6. Bind `IMissionLifecyclePort` to reviewed Mission Lifecycle v1; do not create another lifecycle.
7. Bind STEP_8 contract to existing USB/MAVLink transport; Pi retains high-level goal authority only.
8. Provide ESP32 persistence backend and explicit future schema migration mapping.
9. Bind ESP32 watchdog/reset-cause APIs and diagnostics.
10. Bind verified M10FLY GNSS transport and actual verified compass chip/interface; exact compass interface is NOT VERIFIED.
11. Bind Mission Planner/MAVLink item parsing to STEP_12 adapter; internal architecture remains TANGRA-native.

## Protected local behavior

Preserve MPU6050/BMP280 drivers, sensor health/freshness, approximately 90-degree transform, corrected estimator, cascaded attitude/rate controller, virtual Quad-X mixer, scheduler, Mission Lifecycle v1, existing MAVLink compatibility, rollback capability, and physical-output/arming OFF boundary unless direct local evidence proves a minimal adapter change is required.

## Build and qualification expectations

- inspect real local FC before integration;
- map adapters minimally;
- compile actual FC;
- run existing FC regressions plus portable standalone tests;
- run cross-module integration gate;
- build a non-actuating firmware candidate;
- preserve source/artifact identity and rollback;
- bench install/read-back and hardware qualification only under separate authorized non-actuating phase.

WORKSHOP proves standalone software behavior only.
REAL_FC_INTEGRATION_NOT_YET_PERFORMED.
HARDWARE_QUALIFICATION_NOT_PERFORMED.

Final review: `review/TANGRA-FC-SOFTWARE-AUTONOMY-FINAL.md`
Final checkpoint: `checkpoints/TANGRA-FC-SOFTWARE-AUTONOMY-FINAL.md`


## 2026-11-09 Codex acceptance rework

Prior Codex acceptance: ACCEPT=NO.

Blocking rework checkpoint:
`checkpoints/TANGRA-FC-SA-ACCEPTANCE-REWORK-01.md`

Independent review:
`review/TANGRA-FC-SA-ACCEPTANCE-REWORK-01.md`

Result:
- 8/8 supplied blockers CLOSED;
- 11/11 standalone module tests PASS;
- actual STEP_2-12 closed-loop end-to-end qualification PASS;
- STEP_3 Quad-X plant participates in the real software loop;
- STEP_4/5 state producers added;
- STEP_2 duplicate/out-of-order replay semantics defined;
- STEP_7 consumes shared Mission Lifecycle v1 contract;
- STEP_8 includes configurable MAVLink goal/ACK/telemetry software binding;
- STEP_9 malformed numeric parsing is fail-closed;
- STEP_10/11/12 participate meaningfully in end-to-end qualification.

Remaining boundary:
REAL_FC_INTEGRATION_NOT_YET_PERFORMED.
Concrete local MAVLink IDs/frame transport and binding to the existing local Lifecycle v1 implementation remain Codex integration adapters.


## STEP_13 USB configuration extension

Checkpoint:
`checkpoints/TANGRA-FC-SA-13-01-USB-CONFIGURATION.md`

Package:
`handoffs/TANGRA-FC-SA-13-01-USB-CONFIGURATION_PACKAGE/`

Reuse requirement:
STEP_9 ParameterStore/IParameterStorage remains the single configuration persistence backend.

Codex local adapters:
- bind IUsbConfigurationTransport to the actual ESP32 USB/MAVLink stream/multiplexer;
- provide real firmware/build identity;
- map schema values into existing local FC components without bypassing validated control/safety layers;
- bind STEP_9 IParameterStorage to real ESP32 persistence;
- preserve Quad-X default behavior and do not enable reserved future profiles until their control implementations exist.

STEP_13 REVIEWER_VERDICT: SOFTWARE_IMPLEMENTATION_PASS.
CODEX_INTEGRATION_READY: YES.
