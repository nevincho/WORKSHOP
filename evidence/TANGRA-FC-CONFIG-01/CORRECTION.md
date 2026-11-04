# TANGRA-FC-CONFIG-01 — D1/D2 bounded correction evidence

TASK_ID: TANGRA-FC-CONFIG-01
DATE: 2026-11-04
STATE: CORRECTED_CANDIDATE_TESTED / INDEPENDENT_REVIEW_NOT_COMPLETE
ORIGINAL_TASK: tasks/TANGRA-FC-CONFIG-01.md
PRIOR_REVIEW: review/TANGRA-FC-CONFIG-01.md
CODEX: NOT_USED

## Source provenance
Original archive SHA-256: fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32
Previous candidate SHA-256: 6e82ab0041867fd983d4e930f2a392026154e2593836c211ab1e4aad07b4cdc9

Corrected full patch against original source baseline SHA-256:
5c7580f7d9caf605cd9d97170e3fe158da537b3019d8df365a367cf3c2951571
Corrected source package ZIP SHA-256:
99368879ed581801626d4f18991e5d73e377a57e5ae651ac868140c2aaef01a4

The corrected patch was generated against a clean Git mirror of the source archive and independently replayed into another clean mirror: git apply --check PASS, git apply PASS; 13 relevant implementation/test/documentation files byte-identical, replayed host tests PASS. Files are available in this Control Room as `TANGRA-FC-CONFIG-01-corrected.patch` and `TANGRA-FC-CONFIG-01-corrected-engineering.zip`; not yet checked into a target implementation Git branch.

## D1 — correction
- `src/config/runtime_config.cpp`: `runtimeConfigSet` now validates and stages one pending transaction, returning `QUEUED` without opening Preferences.
- `runtimeConfigCommitPending` executes the blocking NVS write and controller application, only after rechecking system DISARMED, virtual DISARMED and inactive virtual controller. Failed writes preserve current runtime values and result in no successful apply. Pending request is discarded if arming changed.
- `src/mavlink/mavlink2_minimal.cpp`: accepted PARAM_SET is acknowledged after a deferred commit attempt; rejected/unknown requests preserve existing response behavior.
- `TANGRA_FC_ESP32.ino`: `mavlink2ServiceDeferredConfig` is called after `schedulerRun()`, outside `scheduler.cpp`'s 2 ms fast-control task. No new scheduler thread or task.
- Delayed NVS stub adds 700ms to fakeMillis on write. The MAVLink fast-only receive test verifies no storage write, no simulated 700ms advance, and no premature ACK until the main-loop maintenance service. One-pending-request bound and invalid/virtual-armed restrictions are tested.
- **Limitation**: the maintenance service remains synchronous in the single-threaded Arduino main loop. During real NVS flash commit, future schedulerRun invocations may be delayed/missed. The source design accepts this only as a disarmed bench maintenance window. Real flash latency/deadline impact is NOT VERIFIED. Do not claim hard real-time scheduler isolation or armed-use readiness.

## D2 — correction
- `src/mavlink/mavlink2_minimal.cpp:mavlink2ParseFrame` checks payloadLen against `sizeof(g_lastPayload)` before copy.
- Direct-parser CRC-valid 130-byte PARAM_REQUEST_LIST payload is rejected, while valid CRC 118-byte payload remains accepted; ASan/UBSan run PASS and no overflow observed.

## Tests actually executed
- Existing + extended host C++ regression suite: PASS.
- Delayed-NVS 700ms fake storage fixture: PASS, specifically fast-path no direct storage and deferred ACK/commit.
- Virtual arming transition between stage/commit: PASS (pending discarded, original value returned).
- Oversized direct-parser (CRC valid) and max-allowed payload fixtures: PASS.
- Existing MAVLink message 69 regression: PASS.
- AddressSanitizer and UndefinedBehaviorSanitizer on replayed modified sources: PASS, no reported overflow.
- `tools/validate_fc_software_complete.py`: exit 0.
- `tools/validate_fc_simulation.py`: exit 0.
- `tools/validate_quad_x_controller.py`: PASS / 20 checks.
- `tools/validate_quad_x_usb.py`: PASS / 22 checks.
- Git patch baseline replay: PASS, 13 corrected code/test/documentation files byte-identical, host tests PASS.

Known baseline `mavlink2EncodeStatusText` GCC format-truncation warning remains unchanged.

## Review boundary
Source-level regression checks were independently rerun on a fresh patch replay, but the same engineering session prepared the candidate. This does NOT constitute a distinct independent WORKSHOP Reviewer PASS. Do not mark COMPLETE or generate a qualified checkpoint based on the authoring session.
Native Arduino ESP32 compilation, physical USB/NVS timing, actual restart persistence, and production integration remain NOT VERIFIED. No physical operations and no Codex.
