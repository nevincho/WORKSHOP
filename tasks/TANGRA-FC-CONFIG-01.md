# TANGRA-FC-CONFIG-01 — current task state

TASK_ID: TANGRA-FC-CONFIG-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

## Objective and scope
Source-derived bounded MAVLink runtime configuration implementation for the ESP32-WROOM-32 FC. Preserve bench-only motor/arming restrictions, existing message 69 and FC control logic. No flashing, actuation, Pi changes or Codex.

## Source checkpoint
- Human-supplied archive: `TANGRA_FC_ESP32.zip`, SHA-256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
- Confirmed inside archive: `config.h`, `TANGRA_FC_ESP32.ino`, `src/mavlink/mavlink2_minimal.cpp/.h`, `src/fc/*`, sensors, build options and old firmware artifacts.
- Source-reported version: `0.7.0-quad-x-usb-bench`; USB serial 115200; MAVLink2 MANUAL_CONTROL (69).
- Current device flash identity: NOT VERIFIED.
- File-level SHA-256 inventory generated as `source_manifest.json` within engineering package.

## Implementation artifacts
- `TANGRA-FC-CONFIG-01.patch` (SHA-256 `bd46561ecb32a4d1d4f3276cde04e6e69440a35cc2433668c7b9e6d96b7fc253`).
- `TANGRA-FC-CONFIG-01-engineering-candidate.zip` (SHA-256 `6e82ab0041867fd983d4e930f2a392026154e2593836c211ab1e4aad07b4cdc9`).
- Created in isolated execution environment and supplied as downloadable artifacts in Control Room; NOT integrated into a GitHub target branch.
- Candidate includes complete source tree (excluding historical backups/build binaries), tests and integration notes.
- Registry: `FC_ANGLE_KP` [0.1,10], `FC_HOVER_THR` [0,1], `FC_CMD_ANGLE` [0,45], `FC_CMD_YAW` [0,180], all REAL32 and from config.h factory defaults.
- NVS: Preferences namespace `tangra_fc`, key `params_v1`; single versioned checked blob; startup restore before controller init; fallback to factory defaults; minimum 5 seconds between changed writes.
- Existing compile-time safety flags remain compile-time and unexposed.

## Evidence
- Host deterministic C++ tests compiled and executed PASS including MAVLink 20/21/22/23, target filtering, CRC rejection, malformed payload, unsupported IDs/types, bounds, NVS corruption/restore/write-rate, sim arming restrictions, message 69 regression.
- GCC ASan+UBSan execution: PASS.
- Four existing Python static/fixture validators exit 0 (after test output directory established). They are not actual ESP32 build/hardware tests.
- Git patch replay using exact baseline: git apply --check PASS; replayed files byte-identical to candidate; replayed host tests PASS.
- Existing `STATUSTEXT` formatter triggers a host GCC truncation warning; unrelated baseline code.

## Protected components
No changes to production Pi5/runtime, FC device flash, serial ports, ESC, motors, Master or MicroNodes. Stabilization/PID algorithm, sensors, failsafe and existing message 69 command interpretation preserved.

## Remaining gates
Independent WORKSHOP Reviewer must review candidate source/diff and actual evidence; Reviewer PASS required before qualified integration handoff. Target ESP32 Arduino compile, real NVS reboot, USB protocol and timing/bench hardware: NOT VERIFIED. Codex integration and flashing not authorized.

## Current assessment
SOURCE_ACCESS blocker: RESOLVED for this supplied source snapshot.
ENGINEERING_CANDIDATE: PRODUCED; HOST_TESTS: PASS.
INDEPENDENT_REVIEW: NOT_PERFORMED.
INTEGRATION_GATE: CLOSED.
