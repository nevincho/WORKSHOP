# TASK-008 — VK IMOU Camera Integration Preparation

TASK_ID: TASK-008
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
OBJECTIVE: Prepare the smallest safe IMOU camera integration path into VK using the verified shared node/device and sensor-ingestion interfaces, without creating a parallel vision/memory architecture.
SOURCE_PLAN_OR_REQUEST: VK canonical sensor/vision architecture + Vlad request 2026-08-24.
CURRENT_STATE: Device model/network/API/runtime integration status NOT VERIFIED.
PREREQUISITES: TASK-007 PASS or verified equivalent existing abstraction; TASK-004 PASS for VK execution route; identify actual IMOU devices and locally available protocols/streams from direct evidence.
DEPENDENCIES: TASK-007 PASS.
AFFECTED_COMPONENTS: camera adapter, device registry, sensor/input ingestion, event normalization, capability/status UI where justified.
PROTECTED_COMPONENTS: VK Core, canonical personality/memory, provenance semantics.
EXECUTION_CLASS: CODEX_CANDIDATE
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: verified camera connection method is documented; adapter uses shared ingestion/event flow; static/on-demand/event-driven behavior respects canonical vision guidance; no unsupported cloud/API assumptions; no continuous empty-view polling by default.
VALIDATION_METHOD: adapter tests + connection/read test against actual camera when available + event/input evidence + runtime status; live camera validation required for operational PASS.
PRE_CHANGE_CHECKPOINT: REQUIRED.
ROLLBACK_METHOD: remove/disable adapter and restore prior runtime/config checkpoint.
EVIDENCE_PATHS: `evidence/TASK-008/`, `review/TASK-008.md`.
