# TASK-008 — CODEX GATE

ROLE: WORKSHOP CODEX GATE
TASK_ID: TASK-008
DECISION: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25
CODEX_USED: no

## Gate basis
TASK-007 and TASK-010 are PASS/reviewed. Direct human evidence verifies authenticated RTSP substream 1 from IMOU Cruiser SE+ `IPC-K7CP-3H1WE`, while credentials remain intentionally outside Git.

Current `nevincho/LIVE@Legacy` head at preparation: `cf911176be543393f1a05e578b4ea30d70f010bb`.

Current reusable implementation:
- `family_guardian_ai/SOURCE_V09/app/camera_adapter.py` exists but currently accepts integer local camera indices only.
- `family_guardian_ai/SOURCE_V09/app/perception_ingress.py` is the common candidate-only perception ingress.
- shared event-envelope and HomeNode/DeviceRegistry foundations already exist.

## Minimal handoff
Objective:
Implement the smallest backward-compatible extension of the existing camera path that can open an explicit RTSP/network stream source, capture/read a real frame from the verified IMOU substream when the camera is available, and emit bounded observation/event metadata through existing ingress/contracts without creating a parallel vision or memory architecture.

Required pre-execution human inputs/gates:
1. explicit approval for TASK-008 Codex execution;
2. current authorized camera target remains `192.168.0.154` on the user's LAN;
3. runtime credential/RTSP URL supplied outside Git and logs with secrets redacted;
4. Windows execution host and pre-change checkpoint confirmed;
5. permission for a bounded credentialed RTSP connection/read to that camera only.

Affected components:
- existing `camera_adapter.py` and its tests;
- existing perception/event integration only where required for a bounded observation path.

Protected components:
VK Core, canonical personality/memory, memory promotion/provenance semantics, credentials/secrets, unrelated services/adapters.

Acceptance:
- existing local integer camera behavior remains compatible;
- network stream source is supported without hard-coded or committed credentials;
- no parallel registry/vision/memory subsystem is created;
- one controlled read from the actual RTSP substream returns a real frame when the camera is available;
- event/observation metadata uses existing ingress/contracts and does not auto-promote memory;
- failures are explicit and bounded;
- repository tests and relevant regression tests PASS;
- exact target commit, validation commands/results, checkpoint and rollback are recorded;
- independent Reviewer PASS.

Validation method:
Repository tests plus controlled Windows-local credentialed RTSP frame/read and ingress/event evidence against the actual device. Repository-only evidence cannot establish operational PASS.

Rollback:
Restore the pre-change LIVE `Legacy` commit/checkpoint or revert only TASK-008 changes; remove/disable network-stream use without changing existing local-camera behavior.

Non-goals:
No ONVIF, PTZ, cloud API, continuous background polling, facial recognition, new memory subsystem, Core/personality changes, credential storage, or broad LAN scanning.

## Outcome
CODEX HANDOFF: PREPARED.
STATUS: READY_FOR_CODEX_REVIEW.
CODEX USAGE: NONE.
Execution requires fresh explicit Vlad approval for TASK-008.
