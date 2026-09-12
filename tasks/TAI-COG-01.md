# TAI-COG-01

TASK_ID: TAI-COG-01
PROJECT: TANGRA / TAI
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Build a standalone passive bounded State/Event Recorder using reviewed TAI-COG-00 contracts.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room task 2026-09-12.
CURRENT_STATE: IMPLEMENTED_AND_REVIEWED
PREREQUISITES: TAI-COG-00 Reviewer PASS at 7036cb78580d446ba700e318daf0bbe8c60d4afc.
DEPENDENCIES: TAI-COG-00 StateEvent / identity / provenance / realism / SerializableModel contracts.
AFFECTED_COMPONENTS: New Phase A package only at TANGRA_2_0/00_FOUNDATION/TAI_COG_01/.
PROTECTED_COMPONENTS: TAI-COG-00 contracts; existing TANGRA implementation; HQ/Hailo/NanoTracker/CA/CURRENT_TARGET/HOROS; production/runtime.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
PRE_CHANGE_CHECKPOINT: nevincho/TANGRA-2.0 commit 7036cb78580d446ba700e318daf0bbe8c60d4afc
ROLLBACK_METHOD: discard branch tai-cog-01; base checkpoint remains unchanged.
EVIDENCE_PATHS: evidence/TAI-COG-01/WORKER.md; review/TAI-COG-01.md; checkpoints/TAI-COG-01.md

## Acceptance criteria
1. valid StateEvent records and round-trips;
2. ordering/sequence deterministic;
3. provenance and realism unchanged;
4. UNKNOWN/SOURCE_GAP unchanged;
5. malformed records rejected safely;
6. retention/rotation bounded;
7. recorder I/O failure fails open;
8. replay returns original event semantics;
9. deterministic tests PASS;
10. COG-00 reviewed tests remain valid/unregressed.

## Validation method
Repository diff containment, Python py_compile, deterministic unittest suite, static fixture replay, fail-open injection, bounded rotation tests, and exact COG-00 blob identity against reviewed checkpoint.
