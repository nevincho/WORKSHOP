# TANGRA-COG-V1-EXP-PERSIST-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f
CANDIDATE: tangra-cog-v1-exp-persist-01@437211b0bfd69a387ed6c6d852168c4a9482c6ba

## Upstream qualified dependencies

- TANGRA-COG-V1-EXP-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS

## Final repository delta

Exactly two files differ from the qualified EXP-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_persistence_adapter.py
  - blob efcfbf1cefa028efe40735835f25f2c86b8cb812
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_persistence_adapter.py
  - blob 41124f5be9cc5a45b4bb36bcc7eba428b942d807

Temporary qualification workflow changes were restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected component blobs unchanged from base:
- EXP-01 adapter: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- COG-30 lifecycle artifact: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only bounded durable snapshot mechanics around the existing reviewed COG-22 fixture contract:
- save payload is exactly ExperienceStore.export_fixture();
- pre-commit validation reloads through ExperienceStore.from_fixture();
- persistent write uses a temporary file in the explicit destination directory, flush, fsync, os.replace, then directory fsync;
- caller must provide the path and its parent must already exist;
- no target path discovery or Pi/production location is encoded;
- failed replace preserves the prior valid snapshot and cleans the adapter temporary file;
- load is bounded by max_snapshot_bytes;
- load reconstructs only through ExperienceStore.from_fixture();
- noncanonical, malformed, empty, oversized or non-file snapshots are not returned as valid ExperienceStore;
- missing snapshot returns NOT_FOUND and never fabricates an empty store;
- adapter result authority is NONE and operational authority empty.

COG-30 lifecycle-policy state is not imported, invoked, modified or persisted.

## Executed qualification

GitHub Actions run: 36265034508
Executed head: 57712dbbac4f7d91d5e2610a3e58b6f8a6c1addb

PASS:
- Cognitive Bridge: 17/17
- DIAG-01 adapter: 15/15
- CORR-01 integration: 12/12
- HYP-01 integration: 13/13
- INT-01 integration: 13/13
- EXP-01 integration: 13/13
- EXP-PERSIST-01 integration: 13/13
- current reviewed COG-22 source tests: 36/36

Bounded total: 132 PASS / 0 FAIL.

The final implementation/test blobs are identical to those exercised at the passing run. The later candidate commit only restored the pre-existing workflow byte-for-byte.

## Qualified behavior

- EXP-01 RAW_EVIDENCE record persists as exact reviewed COG-22 fixture;
- a fresh/new adapter load reconstructs a new reviewed ExperienceStore;
- ExperienceRecord identity, lifecycle, bindings, provenance, JSON and semantic hash remain exact;
- reviewed COG-22 get/query operate after reload;
- reviewed COG-22 duplicate semantics remain unchanged after reload;
- missing/corrupt/noncanonical snapshot cannot become valid cognitive Experience;
- save failure does not replace previously valid snapshot;
- no lifecycle semantics or promotion policy were added.

## Scope

COG-22 implementation: NOT MODIFIED.
COG-30 lifecycle integration: NOT STARTED / NOT MODIFIED.
COG-30 lifecycle state persistence: NOT STARTED.
COG-21: NOT STARTED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Historical Cognitive Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback target:
tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f

Removing/reverting the two EXP-PERSIST-01 files restores the qualified EXP-01 state.
