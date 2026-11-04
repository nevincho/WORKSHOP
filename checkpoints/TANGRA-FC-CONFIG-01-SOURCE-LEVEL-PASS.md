# TANGRA-FC-CONFIG-01 — source-level BENCH_ONLY qualified checkpoint

TASK_ID: TANGRA-FC-CONFIG-01
CHECKPOINT_CLASS: SOURCE_LEVEL_BENCH_ONLY
VERDICT: INDEPENDENT_REVIEW_PASS
QUALIFIED_DATE: 2026-11-04

BASELINE_ZIP_SHA256: fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32
CORRECTED_PACKAGE_SHA256: 99368879ed581801626d4f18991e5d73e377a57e5ae651ac868140c2aaef01a4
CORRECTED_PATCH_SHA256: 5c7580f7d9caf605cd9d97170e3fe158da537b3019d8df365a367cf3c2951571
MANIFEST_SHA256: b5354056abd1f491a84c77a422a681008149a246ecb60b8933bc0eb7bdec61db
SOURCE_MANIFEST: 59/59 MATCH
GIT_PATCH_REPLAY: PASS
HOST_REGRESSION: PASS
ASAN_UBSAN: PASS
PROJECT_VALIDATORS: 4/4 PASS
INDEPENDENT_REVIEW: review/TANGRA-FC-CONFIG-01-INDEPENDENT-CORRECTED.md
SCOPE: Source-level MAVLink PARAM + Preferences/NVS implementation for BENCH_ONLY with disarmed maintenance write and parser bounds guard.
NOT_VERIFIED: ESP32 native build, real NVS latency and reboot/power loss, UART interoperability, physical bench safety, current flashed firmware.
NO_CHANGE: No Codex, flashing, motor activation, production or Pi5 changes.

Rollback: use exact original source archive and reverse the corrected patch in the development copy; no physical device modifications were made. New NVS namespace/key remains inert in the original baseline unless separately changed.
This is NOT a hardware or production qualification checkpoint.
