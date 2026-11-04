# TANGRA-FC-CONFIG-01 — qualified, NON-EXECUTED Codex integration handoff

AUTHORIZATION: NOT_GRANTED; this file is a package for a later explicit human decision, not an invocation.
GATE: SOURCE_LEVEL_REVIEW_PASS / BENCH_ONLY

INPUTS
- Original source archive SHA256: `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
- Qualified corrected patch SHA256: `5c7580f7d9caf605cd9d97170e3fe158da537b3019d8df365a367cf3c2951571`.
- Corrected source package ZIP SHA256: `99368879ed581801626d4f18991e5d73e377a57e5ae651ac868140c2aaef01a4`.
- Source-level independent review: `review/TANGRA-FC-CONFIG-01-INDEPENDENT-CORRECTED.md`.
- Source-level checkpoint: `checkpoints/TANGRA-FC-CONFIG-01-SOURCE-LEVEL-PASS.md`.

FUTURE INTEGRATION BOUNDARY (only when separately authorized)
1. Work on a separate development copy of the exact source baseline, never a live firmware or production Pi source tree. Confirm baseline hash.
2. Apply the exact qualified patch with `git apply --check`, then `git apply`, verify changed-file manifest; preserve existing message69/bench safety.
3. Compile with matching ESP32 Arduino core and actual library dependencies; record FQBN, compiler/core versions, result, binary hash. Do not substitute host mocks for native compilation.
4. Run existing host regression and sanitizer fixtures; validate USB PARAM messages, real NVS reboot/corruption, delayed write jitter, physical-output prohibition, all on separately approved isolated bench hardware.
5. Stop if any mismatch, new source change, failure or safety regression; report to WORKSHOP. Do not auto-flash, auto-promote or introduce broader modifications. Any changes to source after this checkpoint require another review.

ROLLBACK: restore the original source snapshot for development; no physical firmware rollback is required from this review because device was never changed.
