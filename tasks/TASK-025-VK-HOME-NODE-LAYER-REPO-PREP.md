# TASK-025 — VK Home Node/Device Layer Repository Preparation

TASK_ID: TASK-025
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
DEPENDS_ON: TASK-024 PASS
TYPE: REPOSITORY-ONLY PREPARATION / IMPLEMENTATION SCAFFOLD
OBJECTIVE: Prepare or complete the non-Core shared node/device abstraction in repository scope so later live integrations attach through one stable capability/status/input interface.

RELATION TO TASK-007:
- TASK-025 is the repository-only preparation/scaffold phase.
- TASK-007 remains the later runtime integration/validation task.

BOUNDARY:
- no `D:\Store\AI` changes;
- no Core/personality/memory-promotion changes;
- no IMOU/Echo-specific parallel registries;
- no runtime operational claims.

VALIDATION: repository diff, unit/mock tests, interface reuse evidence, independent review.
