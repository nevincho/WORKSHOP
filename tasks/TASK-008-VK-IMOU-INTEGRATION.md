# TASK-008 — VK IMOU Camera Integration Preparation

TASK_ID: TASK-008
PROJECT: VK
PRIORITY: HIGH
STATUS: COMPLETE
VERDICT: PASS
OBJECTIVE: Prepare the smallest safe IMOU camera integration path into VK using the verified shared node/device and sensor-ingestion interfaces, without creating a parallel vision/memory architecture.
SOURCE_PLAN_OR_REQUEST: VK canonical sensor/vision architecture + Vlad request 2026-08-24.
CURRENT_STATE: Independently reviewed PASS. Bounded authenticated IMOU RTSP `subtype=1` ingestion was validated on the actual `D:\Store\AI` runtime through the existing CameraAdapter and PerceptionIngress path. TASK-008 implementation checkpoint is `840f94abb18f10c87798c2e4a54796dd6dab2bc2`; pre-change rollback is `cf911176be543393f1a05e578b4ea30d70f010bb`. Current `nevincho/LIVE@Legacy` has a later commit and must be treated separately for downstream task mapping/validation.
PREREQUISITES: TASK-007 PASS; TASK-010 PASS; actual IMOU device and locally available stream verified by direct runtime evidence.
DEPENDENCIES: TASK-007 PASS; TASK-010 PASS.
AFFECTED_COMPONENTS: existing camera adapter, device registry, sensor/input ingestion, event normalization, capability/status UI where justified.
PROTECTED_COMPONENTS: VK Core, canonical personality/memory, provenance semantics, credentials/secrets.
EXECUTION_CLASS: CODEX_CANDIDATE
CODEX_ALLOWED: HUMAN_GATE_REQUIRED
ACCEPTANCE_CRITERIA: SATISFIED for TASK-008 checkpoint; verified camera connection method documented; adapter uses shared ingestion/event flow; no unsupported cloud/API assumptions; no continuous empty-view polling by default; existing local-camera behavior remains compatible; credentials are not committed; real camera frame and ingress event verified; independent review PASS.
VALIDATION_METHOD: adapter tests + controlled credentialed connection/read test against actual camera + event/input evidence + runtime status + independent review. Live camera validation completed.
PRE_CHANGE_CHECKPOINT: `cf911176be543393f1a05e578b4ea30d70f010bb`.
IMPLEMENTATION_CHECKPOINT: `840f94abb18f10c87798c2e4a54796dd6dab2bc2`.
ROLLBACK_METHOD: restore pre-change checkpoint or revert TASK-008 network-stream extension while preserving existing local-camera behavior.
EVIDENCE_PATHS: `evidence/TASK-008/CODEX_RUN.md`, `review/TASK-008.md`.
