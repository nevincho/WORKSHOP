# TANGRA-FC-SA-13-01-USB-CONFIGURATION

PROJECT: TANGRA
CAMPAIGN: TANGRA-FC-SOFTWARE-AUTONOMY
STEP: 13
STATUS: COMPLETE
MODE: STANDALONE_SOFTWARE_ENGINEERING
DATE: 2026-11-09

## Objective

Add PC <-> USB configuration support before final Codex integration without creating a second parameter store.

## Reuse

- STEP_9 ParameterStore is the only parameter/persistence backend.
- Existing FC USB/MAVLink architecture remains the integration boundary.
- Existing STEP_2-12 behavior and Mission Lifecycle v1 are protected.

## Required software

- firmware identity;
- parameter schema enumeration;
- get/set/validate/save/defaults/export/import;
- vehicle profile abstraction with QUAD_X default;
- schema groups for motor/ESC, servos, IMU, GNSS/compass, PID, navigation, failsafe/watchdog, telemetry/MAVLink;
- host-side USB configuration protocol/session;
- future fixed-wing/twin-motor-pusher/VTOL profile descriptors without implementing those control laws.

PHYSICAL_OUTPUTS: OFF
ARMING: OFF
LOCAL_FC_INTEGRATION: NOT_YET_PERFORMED

REVIEWER_VERDICT: SOFTWARE_IMPLEMENTATION_PASS
CHECKPOINT: checkpoints/TANGRA-FC-SA-13-01-USB-CONFIGURATION.md
CODEX_INTEGRATION_READY: YES
