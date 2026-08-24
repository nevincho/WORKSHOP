# TASK-007 — VK Home Node and Device Layer

TASK_ID: TASK-007
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
OBJECTIVE: Prepare and, only when execution capability is verified, implement the non-Core home node/device integration layer described by current VK architecture and current Control Room request.
SOURCE_PLAN_OR_REQUEST: `family_guardian_ai/VK_CANONICAL_FOUNDATION_2026-08-21.md` sections on capability discovery, sensor/input ingestion, communication/bootstrap, Vision/Sensors/Nodes; Vlad request 2026-08-24.
CURRENT_STATE: Architecture intent VERIFIED; implementation/runtime state NOT VERIFIED.
PREREQUISITES: TASK-004 PASS for VK route; current VK runtime/repository inspection; confirm no equivalent existing device/node abstraction.
DEPENDENCIES: TASK-004 PASS; if selected as first implementation, TASK-005/TASK-006 govern first change.
AFFECTED_COMPONENTS: non-Core runtime adapters, capability discovery, device registry, sensor/input ingestion, network device plumbing.
PROTECTED_COMPONENTS: VK Core, canonical personality, approved-memory promotion, provenance semantics.
EXECUTION_CLASS: CODEX_CANDIDATE
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: Device/node abstraction is evidence-backed, reuses shared ingestion/event mechanisms, avoids duplicate per-device memory stacks, exposes explicit capability/status information, and preserves protected Core semantics.
VALIDATION_METHOD: repository diff + unit/integration tests + runtime capability/status inspection; live device validation required before claiming device-specific operational status.
PRE_CHANGE_CHECKPOINT: REQUIRED before implementation.
ROLLBACK_METHOD: restore pre-change checkpoint and previous runtime adapter/config state.
EVIDENCE_PATHS: `evidence/TASK-007/`, `review/TASK-007.md`.

## Constraint
Do not hard-code IMOU or Echo-specific architecture before the shared node/device layer is verified. Device-specific adapters should attach through stable interfaces.
