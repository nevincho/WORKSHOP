# TASK-024 — VK Home Network Discovery Repository Preparation

TASK_ID: TASK-024
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
DEPENDS_ON: TASK-023 PASS
TYPE: REPOSITORY-ONLY PREPARATION / IMPLEMENTATION SCAFFOLD
OBJECTIVE: Prepare or implement the repository-side bounded home-network discovery/status layer using existing VK shared capability/device primitives, without claiming live network operation.

RELATION TO TASK-010:
- TASK-024 is the repository-only preparation/scaffold phase.
- TASK-010 remains the later live/runtime integration and validation task.
- TASK-024 must not duplicate or supersede TASK-010's live validation objective.

BOUNDARY:
- repository branch only; no local runtime deployment;
- passive/bounded discovery design only, no intrusive scanning;
- no credentials in repository;
- no parallel device architecture.

VALIDATION: fixture/mock tests for discovery, identity/status normalization and failure handling; independent review. Live LAN claims remain NOT VERIFIED until TASK-010 or equivalent live validation.
