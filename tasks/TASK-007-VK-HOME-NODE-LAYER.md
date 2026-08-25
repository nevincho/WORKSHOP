# TASK-007 — VK Home Node Abstraction

TASK_ID: TASK-007
PROJECT: VK
PRIORITY: HIGH
STATUS: READY_FOR_CODEX_REVIEW
OBJECTIVE: Implement the smallest non-Core shared Home Node abstraction and adapter-facing interface required by current VK architecture, reusing the already-completed TASK-041 device contract rather than duplicating registry responsibilities.
SOURCE_PLAN_OR_REQUEST: `family_guardian_ai/VK_CANONICAL_FOUNDATION_2026-08-21.md` sections on capability discovery, sensor/input ingestion, communication/bootstrap, Vision/Sensors/Nodes; Vlad request 2026-08-24.
CURRENT_STATE: Architecture intent VERIFIED; TASK-021 PASS; TASK-034 PASS; TASK-040 through TASK-044 PASS/reviewed; current LIVE Legacy baseline verified at `078a534b6f0241507349f182626d308f2c0ff284`.
PREREQUISITES: TASK-021 PASS; TASK-034 PASS; TASK-041 PASS; current LIVE Legacy HEAD verified before implementation.
DEPENDENCIES: none beyond listed prerequisites for repository implementation.
AFFECTED_COMPONENTS: non-Core Home Node base model/interface and adapter boundary under `family_guardian_ai/SOURCE_V09/`.
PROTECTED_COMPONENTS: VK Core, canonical personality, approved-memory promotion, provenance semantics, live `D:\Store\AI` runtime, real device access.
EXECUTION_CLASS: CODEX_CANDIDATE
CODEX_ALLOWED: HUMAN_GATE_REQUIRED

## Canonical scope boundary
TASK-007 owns ONLY:
- shared Home Node / device base abstraction;
- stable node/device identity representation by consuming the TASK-041 contract;
- adapter-facing interface/boundary;
- narrow capability/status exposure needed by adapters.

TASK-007 does NOT own:
- runtime registry service or add/update/remove/query registry operations — TASK-028 owns these;
- registry schema/fixtures — TASK-041 already completed these;
- capability discovery — TASK-032;
- network discovery — TASK-010;
- device-specific IMOU/Echo integration — TASK-008/TASK-009;
- live Windows deployment/runtime mutation.

ACCEPTANCE_CRITERIA:
1. A narrow shared Home Node/device abstraction exists and consumes/reuses TASK-041 device contract semantics rather than redefining them.
2. Adapter-facing interface is device-agnostic and does not implement runtime registry operations.
3. Existing `camera_adapter.py` behavior is preserved.
4. No duplicate memory/provenance/device-registry stack is introduced.
5. No IMOU/Echo/network-discovery implementation is included.
6. Repository-only tests pass using existing TASK-034/TASK-041 validation foundations.
7. Exact diff, test output, implementation commit and rollback SHA are recorded.

VALIDATION_METHOD: repository diff + unit tests + compatibility checks against TASK-041 contract/fixtures. Live runtime/device validation remains NOT VERIFIED and out of scope.
PRE_CHANGE_CHECKPOINT: current LIVE Legacy HEAD immediately before Codex implementation; presently `078a534b6f0241507349f182626d308f2c0ff284`.
ROLLBACK_METHOD: restore pre-change repository checkpoint; no live runtime deployment is authorized by this task.
EVIDENCE_PATHS: `evidence/TASK-007/`, `review/TASK-007.md`.
