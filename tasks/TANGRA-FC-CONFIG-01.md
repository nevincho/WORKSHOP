# TANGRA-FC-CONFIG-01

TASK_ID: TANGRA-FC-CONFIG-01  
PROJECT: TANGRA  
PRIORITY: HIGH  
STATUS: BLOCKED

## OBJECTIVE
Develop a complete, implementation-ready MAVLink runtime configuration subsystem for the existing TANGRA ESP32 Flight Controller, preserving the existing FC architecture and bench-only safety restrictions.

## SOURCE_PLAN_OR_REQUEST
Human-directed Control Room request dated 2026-11-04. Target source supplied as:
`D:\RaspberryPi5\TANGRA\WORKSPACE\TANGRA_FC_ESP32`.

## CURRENT_STATE
- Canonical TANGRA coordination/source-of-truth repository inspected: `nevincho/TANGRA-DOCS`.
- TANGRA engineering repository `nevincho/TANGRA-2.0` inspected.
- WORKSHOP repository `nevincho/WORKSHOP` inspected.
- GitHub code search for `TANGRA_FC_ESP32`, `v0.7.0-quad-x-usb-bench`, and MAVLink MANUAL_CONTROL FC identifiers returned no authoritative FC source.
- Project/Library search found historical transcripts and inventory references to the Windows path, but no authoritative current source files suitable for implementation.
- Current flashed firmware identity: NOT VERIFIED.
- Baseline source findings supplied by the human remain NOT VERIFIED against current source in this execution context.

## PREREQUISITES
1. Direct readable access to the current authoritative FC source tree, or an exact current repository/branch/ref containing it.
2. Exact pre-change source checkpoint/hash or repository commit.
3. Existing build dependency/version information from the current source/build metadata.

## DEPENDENCIES
- Existing MAVLink implementation and `config.h`.
- Existing FC initialization order and runtime consumers.
- Existing hardware/arming/motor safety contracts.

## AFFECTED_COMPONENTS
Expected only after source inspection:
- FC MAVLink receive/response path.
- Runtime parameter registry.
- ESP32 Preferences/NVS persistence adapter.
- Supported parameter consumers.
- Repository-side tests/fixtures.

## PROTECTED_COMPONENTS
- Production Raspberry Pi 5.
- Active TANGRA service.
- Existing flashed FC firmware.
- Existing MAVLink communication behavior.
- ESP32 Master and MicroNodes.
- Physical motors and ESC outputs.
- Stabilization, PID, sensor drivers, failsafe and motor-safety behavior except minimal verified parameter-consumer wiring required by this task.

## EXECUTION_CLASS
HUMAN_GATE

## CODEX_ALLOWED
NO

## ACCEPTANCE_CRITERIA
As specified by the Control Room request, including:
- bounded runtime registry based only on existing supported FC configuration;
- MAVLink PARAM_REQUEST_LIST, PARAM_REQUEST_READ, PARAM_SET and PARAM_VALUE;
- correct framing/CRC/target filtering/encoding/responses;
- Preferences/NVS persistence with validation/recovery/write-frequency safeguards;
- defaults from config.h;
- preserved MANUAL_CONTROL message 69 behavior;
- invalid/malformed/unsupported request tests;
- reboot restoration and corruption recovery tests;
- independent Reviewer PASS;
- reviewed implementation package, rollback references and minimal Codex integration handoff.

## VALIDATION_METHOD
Repository-side build/static checks plus deterministic protocol/NVS fixtures against the actual current FC source. Hardware validation remains NOT VERIFIED unless separately executed on authorized hardware.

## PRE_CHANGE_CHECKPOINT
NOT VERIFIED — current FC source repository/ref/hash is unavailable in this execution context.

## ROLLBACK_METHOD
NOT ESTABLISHED until the current authoritative source checkpoint is available. No implementation changes performed.

## EVIDENCE_PATHS
- `AGENTS.md`
- `policies/TANGRA_ENGINEERING_TO_PROMOTION_WORKFLOW_POLICY.md`
- `projects/TANGRA.md`
- `blockers/TANGRA-FC-CONFIG-01-SOURCE-ACCESS.md`
