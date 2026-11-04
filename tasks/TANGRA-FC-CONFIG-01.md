# TANGRA-FC-CONFIG-01 — existing task

TASK_ID: TANGRA-FC-CONFIG-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
REVIEW_VERDICT: BLOCKED_ON_NEW_INDEPENDENT_REVIEW
NEXT_ACTION: INDEPENDENT_REVIEW_OF_CORRECTED_CANDIDATE
CODEX_ALLOWED: NO

OBJECTIVE: Implement bounded MAVLink runtime parameter subsystem on actual source preserving existing Quad-X/MANUAL_CONTROL(69), bench restrictions and motor safety.

SOURCE_CHECKPOINT: Original archive SHA256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
SOURCE_ACCESS: RESOLVED_FOR_SUPPLIED_ARCHIVE
CANDIDATE: ZIP SHA256 `6e82ab0041867fd983d4e930f2a392026154e2593836c211ab1e4aad07b4cdc9`.
PATCH: SHA256 `bd46561ecb32a4d1d4f3276cde04e6e69440a35cc2433668c7b9e6d96b7fc253`.
PATCH_REPLAY: PASS, byte-identical.
HOST_TESTS: PASS (original suite); INDEPENDENT_ADVERSARIAL_ASAN: FAIL.

DEFECTS:
- D1 HIGH: `runtimeConfigSet` synchronous Preferences.putBytes invoked within scheduler 2ms fast task via MAVLink PARAM_SET. NVS write latency unbounded/not tested. Bound commit to safe non-critical context.
- D2 HIGH: `mavlink2ParseFrame` public direct parser copies payload>118 bytes to `g_lastPayload[118]`; independent valid-CRC payloadLen=130 ASan global-buffer-overflow. Pre-existing baseline issue; not demonstrated over normal serial path. Add bounded check and regression.

REVIEW_EVIDENCE: `review/TANGRA-FC-CONFIG-01.md`
WORKER_EVIDENCE: `evidence/TANGRA-FC-CONFIG-01/ENGINEERING.md`
UNQUALIFIED_CHECKPOINT: `checkpoints/TANGRA-FC-CONFIG-01-REVIEW-FAIL.md`
PROTECTED: Pi5 production, current flashed FC, stabilisation/PID, physical motors/ESC, sensor stack, Master, MicroNodes.
NO_CHANGE: No flash, motors, Pi5, Codex or production modifications.
GATES: bounded repair -> tests + independent review PASS -> reviewed qualified checkpoint -> separately authorized dev-copy integration/Arduino-ESP32 build -> bench testing -> separate promotion decision.

## Bounded correction addendum (2026-11-04)

Source-specific D1/D2 candidate correction completed and host-tested; original source-access blocker remains resolved. No new task ID.

CORRECTED_PACKAGE_ZIP_SHA256: `99368879ed581801626d4f18991e5d73e377a57e5ae651ac868140c2aaef01a4`.
CORRECTED_PATCH_SHA256: `5c7580f7d9caf605cd9d97170e3fe158da537b3019d8df365a367cf3c2951571`.
CORRECTION_EVIDENCE: `evidence/TANGRA-FC-CONFIG-01/CORRECTION.md`.
CURRENT_REVIEW_GATE: `review/TANGRA-FC-CONFIG-01-CORRECTION.md`.

D1: direct flash write removed from 2 ms MAVLink fast-control handler; a single pending transaction commits only in DISARMED main-loop maintenance. Delayed-NVS host test PASS. Single-threaded maintenance still delays scheduler during commit: actual timing NOT VERIFIED.
D2: public MAVLink parser now rejects payload >118 before copying; CRC-valid 130-byte ASan/UBSan regression PASS.
Host tests / four source validators / patch replay: PASS. No independent Reviewer PASS for corrected exact hashes yet; therefore no qualified checkpoint, no integration authorization, no Codex, flashing or production modifications.
