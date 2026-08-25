# TASK-008 — VK IMOU Camera Integration Preparation

TASK_ID: TASK-008
PROJECT: VK
PRIORITY: HIGH
STATUS: READY_FOR_CODEX_REVIEW
OBJECTIVE: Prepare the smallest safe IMOU camera integration path into VK using the verified shared node/device and sensor-ingestion interfaces, without creating a parallel vision/memory architecture.
SOURCE_PLAN_OR_REQUEST: VK canonical sensor/vision architecture + Vlad request 2026-08-24.
CURRENT_STATE: TASK-007 and TASK-010 are PASS. Existing `CameraAdapter` supports local integer camera indices only; direct human evidence verifies authenticated IMOU RTSP substream 1, but current device availability and VK runtime ingestion remain NOT VERIFIED.
PREREQUISITES: TASK-007 PASS; TASK-010 PASS; identify actual IMOU device and locally available stream from direct evidence.
DEPENDENCIES: TASK-007 PASS; TASK-010 PASS.
AFFECTED_COMPONENTS: existing camera adapter, device registry, sensor/input ingestion, event normalization, capability/status UI where justified.
PROTECTED_COMPONENTS: VK Core, canonical personality/memory, provenance semantics, credentials/secrets.
EXECUTION_CLASS: CODEX_CANDIDATE
CODEX_ALLOWED: HUMAN_GATE_REQUIRED
ACCEPTANCE_CRITERIA: verified camera connection method is documented; adapter uses shared ingestion/event flow; static/on-demand/event-driven behavior respects canonical vision guidance; no unsupported cloud/API assumptions; no continuous empty-view polling by default; existing local-camera behavior remains compatible; credentials are not committed.
VALIDATION_METHOD: adapter tests + controlled credentialed connection/read test against actual camera + event/input evidence + runtime status + independent review; live camera validation required for operational PASS.
PRE_CHANGE_CHECKPOINT: REQUIRED.
ROLLBACK_METHOD: remove/disable TASK-008 network-stream extension and restore prior runtime/config checkpoint while preserving existing local-camera behavior.
EVIDENCE_PATHS: `evidence/TASK-008/`, `review/TASK-008.md`.
