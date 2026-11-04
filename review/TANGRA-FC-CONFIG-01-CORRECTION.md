# TANGRA-FC-CONFIG-01 — corrected candidate review gate

TASK_ID: TANGRA-FC-CONFIG-01
DATE: 2026-11-04
VERDICT: BLOCKED (INDEPENDENT_REVIEW_NOT_ESTABLISHED)
INTEGRATION_READY: NO

## Source-level re-examination
Corrected patch applies to original archive SHA-256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`, patch SHA-256 `5c7580f7d9caf605cd9d97170e3fe158da537b3019d8df365a367cf3c2951571`, full source ZIP SHA-256 `99368879ed581801626d4f18991e5d73e377a57e5ae651ac868140c2aaef01a4`.

Reviewed source location: `src/config/runtime_config.cpp/.h`, `src/mavlink/mavlink2_minimal.cpp/.h`, `TANGRA_FC_ESP32.ino`, `scheduler.cpp`, `tests/test_fc_config.cpp`, host Preferences stubs and test runner.
D2 previous public parser OOB: fixed at `mavlink2ParseFrame` via explicit g_lastPayload capacity check; CRC-valid 130-byte direct-parse adversarial fixture now rejected under ASan/UBSan (PASS).
D1 previous direct Preferences.putBytes in fast-control path: fixed by staging `PARAM_SET` and deferring commit to DISARMED main-loop maintenance; 700ms stub delay leaves the MAVLink fast handler unchanged until commit (PASS).
The maintenance commit remains synchronous in the single-threaded `loop()`, so missed scheduler cycles are possible during a long write. This is a known, explicitly disarmed/virtual-inactive BENCH-ONLY maintenance trade-off, not proven acceptable for armed flight or real-time production. The full actual NVS delay remains NOT VERIFIED.

## Test and independence conclusion
All local host/source validation and replay evidence: PASS; neither physical ESP32 build nor physical timing tested.
No separate independent Reviewer execution has examined and approved the final hashes. The authoring session's source-level reinspection and reruns cannot become an independent Reviewer PASS.

VERDICT: BLOCKED pending a separate independent Reviewer on this exact corrected candidate, or explicit review of the disarmed maintenance timing trade-off if required by the gate. No candidate code defect of the originally reported parser overflow remains in the host reproduction. No fully-qualified software checkpoint is issued.

## Next gate
A separate Reviewer checks precise source diffs and the acceptance of DISARMED-only deferred maintenance latency, signs PASS/FAIL against exact SHA-256 package; only then create qualified checkpoint and integration handoff. No Codex.
