# TASK-024 — VK Home Network Discovery

TASK_ID: TASK-024
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
DEPENDS_ON: TASK-023 PASS
TYPE: REPOSITORY-ONLY IMPLEMENTATION
OBJECTIVE: Implement or complete a bounded home-network discovery/status layer using existing VK shared capability/device primitives.

BOUNDARY:
- repository branch only; no local runtime deployment;
- passive/bounded discovery design only, no intrusive scanning;
- no credentials in repository;
- no parallel device architecture.

VALIDATION: fixture/mock tests for discovery, identity/status normalization and failure handling; independent review.
