# Planner — TANGRA-FC-SA-13-01-USB-CONFIGURATION

STATUS: IMPLEMENTATION_READY

## Architecture

Extend STEP_9 minimally with atomic multi-parameter apply, reset-to-defaults and read-only definition enumeration. Keep serialization, migration, rollback and storage semantics as the existing source of truth.

Create STEP_13 as a configuration service/schema layer that receives an existing ParameterStore and IParameterStorage reference. No duplicate persistence/state architecture.

The PC/USB application protocol supports:
IDENTITY, SCHEMA COUNT/INDEX, GET, SET, VALIDATE, SAVE, DEFAULTS, EXPORT, IMPORT.

Actual USB CDC/MAVLink stream multiplexing is an INTEGRATION_ADAPTER_REQUIRED local-FC concern. The standalone package exposes IUsbConfigurationTransport/UsbConfigurationSession so Codex can bind it minimally.

Vehicle profile registry:
- QUAD_X: implemented/default, requires 4 motors;
- FIXED_WING, TWIN_MOTOR_PUSHER, VTOL: reserved profile descriptors, control_implemented=false.
Selecting a non-implemented profile must fail closed. No alternate flight-control law is introduced.

## Validation

- schema enumeration and identity;
- valid writes;
- range/dependency rejection;
- persistence/reload;
- defaults;
- export/import;
- transport session;
- STEP_9 legacy generic-store backward compatibility;
- existing STEP_2-12 module regression;
- existing autonomy_stack end-to-end regression.
