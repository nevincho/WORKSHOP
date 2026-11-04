# TANGRA-FC-CONFIG-01 — existing task

TASK_ID: TANGRA-FC-CONFIG-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
REVIEW_VERDICT: FAIL
NEXT_ACTION: BOUNDED_CORRECTION
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
