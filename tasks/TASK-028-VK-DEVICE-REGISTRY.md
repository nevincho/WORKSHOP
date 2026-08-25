# TASK-028 — VK Unified Device Registry

PROJECT: VK
STATUS: BLOCKED
DEPENDS_ON: TASK-007 PASS; TASK-041 PASS
OBJECTIVE: Implement the runtime/in-memory device registry service using the already-completed TASK-041 registry contract/fixtures and the shared Home Node abstraction produced by TASK-007.
PROTECTED: VK Core, personality, approved-memory promotion and provenance semantics must not change.

## Canonical ownership
TASK-028 is the sole owner of runtime registry behavior, including add/update/remove/query/list operations and registry state management.

TASK-028 MUST reuse:
- TASK-041 `device_registry_v1` contract and fixtures;
- TASK-007 shared Home Node/device abstraction after TASK-007 PASS.

TASK-028 MUST NOT redefine the TASK-041 schema or create a second device abstraction.
TASK-028 does not own network discovery, capability probing, IMOU/Echo adapters or live runtime deployment.

ACCEPTANCE:
- runtime registry behavior conforms to TASK-041 contract/fixtures;
- uses TASK-007 abstraction rather than duplicating it;
- deterministic repository tests cover registry operations and status handling;
- protected Core/personality/provenance semantics unchanged;
- Reviewer PASS.
