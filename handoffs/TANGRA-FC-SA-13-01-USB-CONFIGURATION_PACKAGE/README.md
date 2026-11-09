# STEP_13 USB Configuration

Standalone PC <-> USB configuration service layered on the existing STEP_9 ParameterStore.

Commands:
- IDENTITY
- SCHEMA COUNT / SCHEMA <index>
- GET / SET
- VALIDATE
- SAVE
- DEFAULTS
- EXPORT / IMPORT

The service does not own a second parameter store. It receives ParameterStore and IParameterStorage references.

QUAD_X remains the implemented/default vehicle profile. FIXED_WING, TWIN_MOTOR_PUSHER and VTOL are reserved profile descriptors only; selecting them fails closed until their control adapters exist.

Schema groups cover vehicle profile, motor/ESC mapping, servos, IMU orientation/calibration, GNSS/compass, PID, navigation limits, failsafe/watchdog, telemetry/MAVLink.

Actual local USB CDC/MAVLink transport/multiplexing remains INTEGRATION_ADAPTER_REQUIRED.
Physical outputs and arming remain OFF.
