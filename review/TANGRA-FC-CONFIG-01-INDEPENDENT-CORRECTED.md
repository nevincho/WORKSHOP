# TANGRA-FC-CONFIG-01 — Independent review of corrected candidate

TASK_ID: TANGRA-FC-CONFIG-01
DATE: 2026-11-04
MODE: INDEPENDENT_SOURCE_REVIEW
VERDICT: PASS — SOURCE_LEVEL / BENCH_ONLY
INTEGRATION_READY: YES_FOR_SEPARATELY_AUTHORIZED_DEVELOPMENT_COPY_INTEGRATION_ONLY
CODEX_AUTHORIZED: NO
PRODUCTION_PROMOTION: NO

## Frozen provenance
Baseline `TANGRA_FC_ESP32.zip` SHA-256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
Corrected ZIP `TANGRA-FC-CONFIG-01-corrected-engineering.zip` SHA-256 `99368879ed581801626d4f18991e5d73e377a57e5ae651ac868140c2aaef01a4`.
Corrected patch `TANGRA-FC-CONFIG-01-corrected.patch` SHA-256 `5c7580f7d9caf605cd9d97170e3fe158da537b3019d8df365a367cf3c2951571`.
Manifest `TANGRA-FC-CONFIG-01-corrected-manifest.json` SHA-256 `b5354056abd1f491a84c77a422a681008149a246ecb60b8933bc0eb7bdec61db`.

Original archive separately extracted; source subset checked into fresh temporary Git repository, clean `git apply --check` PASS and `git apply` PASS. All 59 manifest paths compared with candidate for byte identity and manifest SHA-256: 59/59 MATCH.

## Independently inspected source
`TANGRA_FC_ESP32.ino` (setup and loop), `scheduler.cpp` (2 ms fast, 4 ms attitude, 20 ms safety/position), `src/config/runtime_config.cpp/.h`, `src/mavlink/mavlink2_minimal.cpp/.h`, `src/fc/fc_pipeline.cpp`, `src/fc/quad_x_controller.cpp`, `system_state.cpp`, `safety_manager.cpp`, `hardware_abstraction.cpp`, `config.h`, host test, Arduino/Preferences stubs, integration handoff.

## D1 — PASS, BENCH-ONLY
Call graph traced:
`loop() -> schedulerRun() -> fastControlPlaceholder() -> mavlink2SerialService() -> handleParamMessage(23) -> runtimeConfigSet()`.
This stages ONE pending candidate; does not call Preferences.putBytes or other NVS storage.
After scheduler returns, `loop() -> mavlink2ServiceDeferredConfig() -> runtimeConfigCommitPending()` rechecks `systemGetState()==DISARMED`, virtual arming DISARMED and `virtualControllerActive==false`, then persists Preferences data synchronously, changes runtime registry, invokes `runtimeConfigApply`, and emits PARAM_VALUE after commit attempt. On storage failure, configuration and controller remain unchanged and PARAM_VALUE reflects unchanged value. On arming transition pending write is rejected without storage, reply remains current. Initial restore occurs before Quad-X controller initialization, and config is applied after initialization.

Scheduler timing: 700 ms Preferences-stub delay does not affect the fast handler because commit is outside `schedulerRun`. The same Arduino `loop()` remains single-threaded, so real NVS flash latency can delay subsequent scheduler calls and register skipped cycles. This is acceptable *only* for current BENCH_ONLY DISARMED maintenance, with physical motor/arming disabled by `config.h` compile-time checks, no hardware/ESC output path in `hardware_abstraction.cpp`, virtual controller inactive on admission and commit, and `safetyPeriodic()` empty in this baseline. No claim of flight-ready hard real-time isolation. Actual NVS latency NOT VERIFIED.

## D2 — PASS
`mavlink2ParseFrame()` explicitly rejects `payloadLen > sizeof(g_lastPayload)` prior to copying. Independent direct-parser CRC-valid oversized 130-byte payload fixture rejected; valid 118-byte bound remains accepted. ASan/UBSan run PASS. No observed buffer overflow. Existing MANUAL_CONTROL message 69 host regression PASS.

## Independent commands and results
In clean replay path:
- `bash tests/run_host_tests.sh`: PASS, exit 0.
- `g++ -std=c++17 -g -O1 -Wall -Wextra -Wno-error=format-truncation -fsanitize=address,undefined -fno-omit-frame-pointer -Itests/host_stubs -I. tests/test_fc_config.cpp src/config/runtime_config.cpp src/mavlink/mavlink2_minimal.cpp src/fc/quad_x_controller.cpp system_state.cpp -o <review-temp>/fc_asan`; ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 execution: PASS, no sanitizer findings.
- `python tools/validate_fc_software_complete.py`: exit 0.
- `python tools/validate_fc_simulation.py`: exit 0.
- `python tools/validate_quad_x_controller.py`: PASS, 20 checks, exit 0.
- `python tools/validate_quad_x_usb.py`: PASS, 22 checks, exit 0.

Existing STATUSTEXT GCC format truncation warning present in baseline; unrelated to D1/D2; not a build error with this host test command.
Tests use mocked Arduino/Preferences, no native ESP32 toolchain, no real flash operations, and do not measure latency, hardware current draw, physical reboot/power loss, native compiler conformance or external GCS interoperability.

## Verdict boundary
PASS only for current source-level BENCH_ONLY acceptance. Previous D1 and D2 defects closed under that boundary. Qualification checkpoint: `checkpoints/TANGRA-FC-CONFIG-01-SOURCE-LEVEL-PASS.md`.
Minimal non-executed integration handoff: `handoffs/TANGRA-FC-CONFIG-01-CODEX-INTEGRATION.md`.
No Codex, source target branch, firmware flash, physical motor activation, Pi5 or production changes.
