# TANGRA-COG-V1-EXP-PERSIST-01 — COG-22 Durable Experience Snapshot Store

TASK_ID: TANGRA-COG-V1-EXP-PERSIST-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Add the smallest repository-side durable snapshot adapter around the reviewed COG-22 ExperienceStore so WORKSHOP_QUALIFIED EXP-01 RAW_EVIDENCE records survive restart and remain retrievable.
UPSTREAM_CHECKPOINTS:
- TANGRA-COG-V1-EXP-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS
CURRENT_STATE:
- Qualified EXP-01 base: nevincho/TANGRA-2.0:tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f
- Reviewed COG-22 is in-memory but provides exact export_fixture()/from_fixture() serialization semantics.
- COG-30 lifecycle semantics are separate and explicitly excluded from this task.
PREREQUISITES:
- Persist the exact COG-22 fixture representation only.
- Reload exclusively through ExperienceStore.from_fixture().
- No Pi path or production storage location is prescribed.
DEPENDENCIES:
- EXP-01
- reviewed COG-22 ExperienceStore serialization contract
AFFECTED_COMPONENTS:
- One bounded durable snapshot adapter.
- Bounded integration qualification tests.
PROTECTED_COMPONENTS:
- Cognitive Bridge.
- DIAG-01, CORR-01, HYP-01, INT-01, EXP-01 adapters.
- COG-22 ExperienceRecord/ExperienceStore implementation.
- COG-30 lifecycle artifact and lifecycle-policy state.
- COG-21 and all later Cognitive dependencies.
- production TANGRA / Raspberry Pi / runtime wiring.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. COG-22 implementation is reused unchanged.
2. Snapshot payload is exactly ExperienceStore.export_fixture().
3. Reload uses only ExperienceStore.from_fixture().
4. Atomic storage uses a temporary file in the destination directory plus flush/fsync and os.replace; no database/network/vector store.
5. Destination path is explicit caller input; no Pi/production path is inferred.
6. Parent directory must already exist; adapter performs no filesystem discovery.
7. Successful save leaves a complete UTF-8 snapshot and no adapter temp file.
8. Save failure does not replace a previously valid snapshot.
9. Missing snapshot is reported as bounded NOT_FOUND/failed-load state, never fabricated as empty Experience.
10. Malformed/truncated snapshot is rejected and never returned as valid ExperienceStore.
11. Fresh adapter/process-style reload reconstructs a new reviewed ExperienceStore.
12. Experience IDs, lifecycle, bindings, provenance, semantic hashes and JSON round-trip remain exact after reload.
13. Reloaded store supports reviewed get()/query().
14. Duplicate semantic handling remains the reviewed COG-22 behavior after reload.
15. Only RAW_EVIDENCE EXP-01 behavior is exercised; no lifecycle promotion.
16. COG-30 is not imported, invoked, modified or persisted.
17. AUTHORITY=NONE and operational_authority=[] on adapter results.
18. All upstream qualification suites through EXP-01 remain PASS.
19. Current reviewed COG-22 source tests remain PASS.
VALIDATION_METHOD:
- Bounded authoritative GitHub Actions execution.
- Execute Bridge, DIAG-01, CORR-01, HYP-01, INT-01, EXP-01, PERSIST-01 and reviewed COG-22 source tests.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f
ROLLBACK_METHOD:
- Revert/remove PERSIST-01 files to exact EXP-01 checkpoint.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-EXP-PERSIST-01/WORKER.md
- review/TANGRA-COG-V1-EXP-PERSIST-01.md
- checkpoints/TANGRA-COG-V1-EXP-PERSIST-01.md

COG-30: NOT STARTED
COG-30_LIFECYCLE_STATE_PERSISTENCE: NOT STARTED
COG-21: NOT STARTED
PI_CHANGES: NONE
CODEX: NOT USED
