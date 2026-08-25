# TASK-007 — CODEX GATE

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25
CODEX_USED: no

## Decision
Codex is justified only for the remaining architecture-dependent shared Home Node abstraction after repository-side preparation. The previous handoff incorrectly included registry operations that belong to TASK-028 and duplicated semantics already supplied by TASK-041. That scope conflict is now resolved.

Automation MUST NOT invoke Codex. Vlad approval is required for this specific task.

## Minimal Codex handoff
Task: TASK-007 — VK Home Node Abstraction.

Authoritative target:
- repo: `nevincho/LIVE`
- branch: `Legacy`
- verified baseline head: `078a534b6f0241507349f182626d308f2c0ff284`
- path: `family_guardian_ai/SOURCE_V09/`

Verified prerequisites:
- TASK-021 PASS;
- TASK-034 PASS;
- TASK-040 through TASK-044 PASS/reviewed;
- TASK-041 provides canonical device registry contract/fixtures;
- repository-side mock/test/checkpoint route exists.

Objective:
Implement the smallest non-Core shared Home Node/device base abstraction and adapter-facing interface that REUSES TASK-041 contract semantics. Expose stable identity, device/node kind, capability/status view, and a device-agnostic adapter boundary. Preserve existing `camera_adapter.py` behavior.

Explicit ownership boundary:
- TASK-007 owns shared Home Node/device base abstraction + adapter-facing interface only.
- TASK-041 owns registry schema/fixtures and is already PASS.
- TASK-028 owns runtime/in-memory registry service and add/update/remove/query/list operations.
- TASK-032 owns capability discovery.
- TASK-010 owns network discovery.
- TASK-008/TASK-009 own IMOU/Echo integrations.

Protected components:
- VK Core;
- canonical personality;
- approved-memory promotion/provenance semantics;
- live `D:\Store\AI` runtime;
- real IMOU/Echo/camera access.

Non-goals:
- no runtime registry operations;
- no new registry schema;
- no network or capability discovery;
- no device-specific integration;
- no live Windows deployment;
- no broad refactor of memory/chat/Core architecture.

Acceptance:
1. shared node/device base abstraction is narrow and testable;
2. TASK-041 identity/type/capability/status semantics are reused, not duplicated;
3. adapter-facing interface is device-agnostic;
4. no registry service operations are implemented in TASK-007;
5. existing camera adapter behavior is preserved;
6. no duplicate memory/provenance stack is introduced;
7. repository tests pass against existing fixture/contract route;
8. exact commit, diff, test output and rollback SHA are recorded.

Rollback SHA before implementation: `078a534b6f0241507349f182626d308f2c0ff284` unless LIVE Legacy advances again; Codex must re-check HEAD before modifying and stop if it differs without revalidation.

After implementation, Reviewer must inspect actual diff/tests before PASS. Live operational claims remain NOT VERIFIED until later runtime/device validation.
