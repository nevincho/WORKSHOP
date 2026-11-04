# TANGRA-FC-CONFIG-01 — source-derived engineering evidence

TASK_ID: TANGRA-FC-CONFIG-01
DATE: 2026-11-04
STATUS: ENGINEERING_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW
SOURCE_ACCESS_BLOCKER: RESOLVED_FOR_SUPPLIED_ARCHIVE

## Provenance
Archive: `TANGRA_FC_ESP32.zip` SHA-256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
Root includes `config.h`, FC entrypoint, `src/mavlink/mavlink2_minimal.cpp/.h`, `src/fc`, `src/sensors`, build options and older backups/readback evidence.
Current source `config.h` SHA-256: `ca3d432defa93e...`; exact 64-hex hashes for all extracted baseline files are in `source_manifest.json` within the candidate package.
Source version: `0.7.0-quad-x-usb-bench`.
Current flashed device identity NOT VERIFIED.

## Implementation
A complete development candidate (full source copy + tests + Git patch) was created in isolated container from the supplied archive. No target device or TANGRA production source touched.

Patch SHA-256: `bd46561ecb32a4d1d4f3276cde04e6e69440a35cc2433668c7b9e6d96b7fc253`
Candidate ZIP SHA-256: `6e82ab0041867fd983d4e930f2a392026154e2593836c211ab1e4aad07b4cdc9`

Changed files: `config.h`, `TANGRA_FC_ESP32.ino`, `src/fc/fc_pipeline.cpp`, `src/fc/quad_x_controller.cpp`, `src/mavlink/mavlink2_minimal.cpp`.
Added: `src/config/runtime_config.h`, `src/config/runtime_config.cpp`, host testing stubs and test runner, and integration handoff documentation.

Registry: `FC_ANGLE_KP` [0.1,10], `FC_HOVER_THR` [0,1], `FC_CMD_ANGLE` [0,45], `FC_CMD_YAW` [0,180]; factory defaults 4, 0.5, 15, 45 respectively. All MAV_PARAM_TYPE_REAL32.

Protocol: MAVLink2 20/21/22/23 with CRC extras 214/159/220/168. Existing 69 preserved. Unknown IDs ignored; known param rejected SET responds with current value. Target system/component filtering, strict payload size, invalid NaN/ranges, DISARMED and virtual arming checks.

Preferences/NVS: namespace `tangra_fc`, key `params_v1`, versioned + checksum + size + count; fallback to factory defaults on absent/corrupt/incompatible storage. At most one write per accepted changed parameter and minimum 5000ms interval; unchanged/rejected values never write. Existing Quad-X set-config consumer handles application.

## Executed validation
1. `bash tests/run_host_tests.sh` — PASS. C++17 host compile and deterministic execution against modified production C++ sources with Arduino/Preferences stubs. Tests MAVLink list/read/set/value, wrong target, unsupported ID/type, NaN/out-of-range value, corrupt frame, malformed payload, DISARMED/virtual-arm gates, NVS write suppression, reboot restoration and corrupted storage, original msg69 regression. Physical control remains mocked; this is not a hardware test.
2. `g++ -std=c++17 -fsanitize=address,undefined ...` + executable — PASS.
3. `python tools/validate_fc_software_complete.py` — exit 0 (source/fixture checks, NOT hardware).
4. `python tools/validate_fc_simulation.py` — exit 0 (source/fixture checks).
5. `python tools/validate_quad_x_controller.py` — PASS, 20 checks (static/fixture).
6. `python tools/validate_quad_x_usb.py` — PASS, 22 checks (static/fixture).
7. Fresh baseline `git apply --check TANGRA-FC-CONFIG-01.patch` — PASS; patch application — PASS; eight changed/new code/test files byte-identical to candidate — PASS; replayed host tests — PASS.

First patch-generation attempt (raw unified diff) failed on CRLF source files; replaced with git binary-aware patch; successful replay is final evidence. First static validators invocation failed only because excluded build_artifacts output directory was absent in isolated copy; directory added and reruns returned 0. Neither intermediate harness/output issue establishes a firmware defect.

Existing host warning: source `mavlink2_minimal.cpp` STATUSTEXT `snprintf` format-truncation warning from baseline untouched code; runner disables only that warning as fatal while retaining others.

## Independent review and limitations
No separate independent Reviewer agent has been run in this session. The authoring agent's own checks cannot be represented as independent reviewer PASS.
REVIEW_VERDICT: NOT_PERFORMED / BLOCKED_ON_INDEPENDENT_REVIEW_GATE.

Real ESP32 Arduino-core compile: NOT EXECUTED (no Arduino ESP32 compiler in this container).
Actual USB/MAVLink device compatibility, timed NVS commit latency and real reboot persistence: NOT VERIFIED.
Current flashed firmware identity: NOT VERIFIED.
No Codex, flash, serial access, Pi changes, hardware actuation or production promotion.

## Next gate
An independent WORKSHOP Reviewer must inspect the exact candidate package, diff, actual evidence, rollback, and suitability of NVS synchronous write latency while the bench controller is DISARMED. Reviewer PASS + checkpoint is required before any reviewed Codex integration handoff. No Codex action authorized.
