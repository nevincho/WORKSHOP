# TAI-COG-02

TASK_ID: TAI-COG-02
PROJECT: TANGRA / TAI
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Build a standalone evidence-only Evidence Packet Builder over reviewed COG-00 StateEvent and COG-01 RecordedEvent contracts.
SOURCE_PLAN_OR_REQUEST: Vlad explicit Control Room task, 2026-09-12.
CURRENT_STATE: Repository-side Phase A package implemented on nevincho/TANGRA-2.0 branch tai-cog-02.
PREREQUISITES: COG-00 checkpoint 7036cb78580d446ba700e318daf0bbe8c60d4afc; COG-01 checkpoint 56a670e9afc3fa9e91e3e835c496b1f26928e1e1.
DEPENDENCIES: Reviewed COG-00 contracts and COG-01 RecordedEvent.
AFFECTED_COMPONENTS: TAI_COG_02 only.
PROTECTED_COMPONENTS: COG-00, COG-01, existing TANGRA, production/runtime authority.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA: deterministic bounded evidence selection, preservation of semantics, explicit missing/truncation metadata, serialization round-trip, malformed rejection, tests/review/checkpoint PASS.
VALIDATION_METHOD: deterministic Python unit tests plus branch diff/static contract review.
PRE_CHANGE_CHECKPOINT: 56a670e9afc3fa9e91e3e835c496b1f26928e1e1
ROLLBACK_METHOD: discard tai-cog-02 branch.
EVIDENCE_PATHS: evidence/TAI-COG-02/WORKER.md; review/TAI-COG-02.md; checkpoints/TAI-COG-02.md
