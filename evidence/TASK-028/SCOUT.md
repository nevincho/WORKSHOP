# TASK-028 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25

## Necessity / duplication
TASK-028 is canonical and is the sole owner of runtime/in-memory registry service operations. No existing committed registry service implementation was found in LIVE. TASK-041 already owns schema/fixtures; TASK-007 now PASS owns shared Home Node abstraction. This task is therefore necessary and non-duplicate.

## Verified prerequisites
- TASK-041: PASS / reviewed.
- TASK-007: PASS / independently verified against LIVE commit `c4f524cac0054e400a1fb2cb6049697f8971fba3`.
- LIVE `Legacy` current head at Scout time: `c4f524cac0054e400a1fb2cb6049697f8971fba3`.
- Repository-side Python unit-test route exists.

## Exact objective
Implement the smallest in-memory registry service that stores `HomeNode` values and supports add, update, remove, get/query-by-id and list behavior while reusing TASK-041/TASK-007 semantics.

## Affected components
- new `family_guardian_ai/SOURCE_V09/app/device_registry.py`
- new deterministic repository tests under `family_guardian_ai/SOURCE_V09/tests/`

## Protected / excluded
- VK Core and canonical personality
- memory promotion/provenance architecture
- network discovery
- capability probing
- IMOU/Echo/device-specific adapters
- live Windows deployment
- TASK-041 contract/schema
- TASK-007 HomeNode abstraction

## Validation method
Repository-side exact-byte Python unit tests using the committed TASK-041 fixtures and TASK-007 `HomeNode`. Verify deterministic add/update/remove/get/list/status handling and duplicate/missing-device behavior. Record target commit and rollback SHA.

## Rollback/checkpoint
Pre-Worker rollback SHA: `c4f524cac0054e400a1fb2cb6049697f8971fba3`.

## Codex Gate
Codex is not justified for this bounded repository-local in-memory service. Worker can implement and test it directly. Codex usage: no.
