# TANGRA-FC-CONFIG-01 — Independent Source Review

TASK_ID: TANGRA-FC-CONFIG-01
DATE: 2026-11-04
VERDICT: FAIL
INTEGRATION_READY: NO
CODEX: NOT_USED

## Exact inspected artifacts and provenance
- User-supplied original archive: `TANGRA_FC_ESP32.zip`, SHA-256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
- Worker candidate: `TANGRA-FC-CONFIG-01-engineering-candidate.zip`, SHA-256 `6e82ab0041867fd983d4e930f2a392026154e2593836c211ab1e4aad07b4cdc9`.
- Proposed patch: `TANGRA-FC-CONFIG-01.patch`, SHA-256 `bd46561ecb32a4d1d4f3276cde04e6e69440a35cc2433668c7b9e6d96b7fc253`.
- Manifest SHA-256 `a4a28a8a6bedeac6588cf715c57cba796380c1fa26ce3668f45f8f7a24742e32`.
- Actual inspected files: `src/config/runtime_config.cpp/.h`, `src/mavlink/mavlink2_minimal.cpp/.h`, `TANGRA_FC_ESP32.ino`, `src/fc/fc_pipeline.cpp`, `src/fc/quad_x_controller.cpp`, `scheduler.cpp`, `tests/test_fc_config.cpp`, `tests/run_host_tests.sh`, `CONFIG_INTEGRATION_HANDOFF.md`, old baseline source.

## Provenance replay
Original source archive extracted (non-source backup/build paths excluded); clean temporary Git repository created. `git apply --check`: PASS; `git apply`: PASS. All candidate files compared to replayed source: zero mismatches. No baseline/production files modified.

## Independently rerun test
`bash tests/run_host_tests.sh` -> PASS (exit 0). GCC emits existing `mavlink2EncodeStatusText()` -Wformat-truncation warning.

## Independent adversarial test — FAILED
The public `mavlink2ParseFrame` accepts a direct caller's CRC-valid MAVLink2 known message with a 130-byte payload, then copies 130 bytes into fixed `g_lastPayload[118]` without capacity check. Reproduction uses the existing frame fixture's CRC builder; creates message 21 payload length 130, CRC extra 159, then calls the public parser directly. Compiled under `g++ -std=c++17 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer` against candidate sources, stubs and fixture dependencies. ASan reports global-buffer-overflow at `src/mavlink/mavlink2_minimal.cpp:228`, write immediately after `g_lastPayload[118]`, program aborted. This is pre-existing in source archive, not introduced by this patch. Existing `mavlink2ReceiveByte` bounds USB framing to its 128-byte buffer, so this reproduction does NOT establish USB-path exploitability or a hardware fault. Because the public parser remains unbounded and candidate touches parser, qualification should cover this invariant without refactoring transport.

## DEFECTS

### D1 — HIGH — NVS blocking in 2 ms control task
Locations: `src/config/runtime_config.cpp:runtimeConfigSet`, `src/mavlink/mavlink2_minimal.cpp:mavlink2SerialService`, `scheduler.cpp:fastControlPlaceholder`.
Path: `schedulerRun() -> fastControlPlaceholder() -> mavlink2SerialService() -> handleParamMessage(23) -> runtimeConfigSet() -> Preferences::putBytes() / prefs.end()`.
The scheduled fast-control task period is 2000 us. This implementation synchronously performs flash storage inside that task. No bounded worst-case NVS latency or scheduler isolation is present. The host `Preferences` stub returns immediately, so existing tests do not measure this objective. Actual delay/jitter is NOT VERIFIED; a potential deadline overrun is structurally established. Since runtime update only allows disarmed state, this is not evidence of armed physical actuation, but it remains an unqualified time-critical scheduler change.
Smallest correction: decouple NVS writes from the 2ms scheduler's serial processing path, with bounded request admission and an explicitly safe, non-critical commit context; retain deterministic ACK/response and rollback semantics. Prove busy-write and recovery behavior with deterministic delayed-NVS fixture.

### D2 — HIGH — out-of-bounds public parser copy
Location: `src/mavlink/mavlink2_minimal.cpp:mavlink2ParseFrame`, line 228. A valid CRC frame with payloadLen 130 causes ASan global-buffer-overflow copying into `g_lastPayload[118]`. Pre-existing baseline issue, USB receive path separately bounded. Smallest correction: enforce input payload capacity in the public parse function before copying; add direct-parser oversized known-message regression under ASan/UBSan. No broad MAVLink rewrite.

## Other review observations
- Actual message CRC extras 20=214, 21=159, 22=220, 23=168, 69=243 align with MAVLink common dialect values; the test suite checks these fixture CRCs, although CRC fixtures share a locally duplicated algorithm rather than an independent MAVLink library.
- PARAM_REQUEST_READ wire order and PARAM_SET wire order align with common MAVLink layouts, and broadcast targeting is supported. Existing tests use partial responses checks and do not establish external GCS interoperability.
- The 4-param numeric REAL32 registry uses bounded values and checks finite numbers. `runtimeConfigInitialize` loads a versioned/checksummed Preferences snapshot and falls back to defaults; `runtimeConfigApply` wires into Quad-X after initialization.
- The write limiter suppresses unchanged/invalid/rate-limited updates in unit tests. Host storage stub does not simulate ESP32 NVS flash commit duration, power failure atomicity, or hardware reboot.
- `FC_CMD_YAW` cross-field check against `maxRateDps` is present.
- Source safety gates check `systemGetState()`, virtual arming and virtual controller activity. No physical output or firmware deployment occurred.
- Main loop's `schedulerRun` calls `mavlink2SerialService` in the fast task; 4-frame PARAM_REQUEST_LIST transmission may also consume task time, not measured, but no confirmed overrun claimed.
- Arduino-ESP32 native compile was NOT performed, and source review cannot establish toolchain-specific compatibility.

## Test assessment
Worker host suite PASS does not prove the public parser's full input domain or NVS timing. Independent ASan adversarial test FAIL exposes a real bounds violation. The existing suite validates many nominal PARAM and NVS behaviors but cannot justify release-level correctness or real timing. No overall PASS.

## Correction unit / next review
Return only MAVLink PARAM/NVS scheduling implementation and parser bounds checks for bounded repair; preserve all unrelated FC components. Rerun existing host tests, new oversized direct-parser ASan test, and delayed storage fixture. Then a fresh independent review of exact corrected candidate + evidence is required. No Codex until PASS.

## Hardware/integration gates
ESP32 native compilation; full USB MAVLink interoperability and RX/TX timing; real NVS reboot, corruption/power-loss and commit-time qualification; bench safety and explicit human integration approval. All NOT VERIFIED.

## Checkpoint
Candidate hashes listed above are provenance markers only. They are NOT qualified/validated checkpoints. Original user archive is preserved for rollback. `checkpoints/TANGRA-FC-CONFIG-01-REVIEW-FAIL.md` records unqualified state.
