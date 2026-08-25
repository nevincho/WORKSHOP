# TASK-008 — SCOUT / PLANNER

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25

## Necessity / current state
TASK-010 is now PASS/reviewed, so the VK chain prerequisite for TASK-008 is satisfied.

Authoritative `nevincho/LIVE@Legacy` was inspected at current head `cf911176be543393f1a05e578b4ea30d70f010bb`.

Existing relevant implementation:
- `app/camera_adapter.py` already exists and is the correct reuse point for camera capture.
- It currently accepts integer local camera indices and converts the device argument with `int(device)`; it therefore does not currently support an RTSP URL source.
- `app/perception_ingress.py` already provides the common candidate-only sensor ingress and explicitly does not write canonical memory.
- TASK-040 supplies the shared event-envelope contract.
- TASK-007/TASK-028 supply the shared HomeNode/DeviceRegistry path.

No separate IMOU-specific adapter should be created unless the existing camera adapter cannot be safely extended. A parallel vision/memory architecture would be a coordination error.

## Direct device evidence
Existing human evidence identifies IMOU Cruiser SE+ `IPC-K7CP-3H1WE` at `192.168.0.154/24` and verifies authenticated RTSP substream 1 displayed real video in VLC. Credentials/safety code are intentionally absent from WORKSHOP and must remain uncommitted.

TASK-010's latest controlled discovery did not observe `192.168.0.154`; that does not invalidate the prior direct RTSP evidence, but current camera availability is NOT VERIFIED.

## Prerequisites
Satisfied:
- TASK-007 PASS.
- TASK-010 PASS.
- shared registry/node layer available.
- common perception ingress available.
- direct RTSP substream evidence exists.

Human/runtime-gated for operational integration:
- current camera reachability;
- credentialed RTSP URL supplied at runtime without committing secrets;
- Windows runtime execution route/checkpoint;
- actual frame-read test and event/ingress evidence.

## Protected components
VK Core, canonical personality/memory, approved-memory promotion/provenance semantics, credentials/secrets, unrelated adapters/services.

## Smallest justified change
Extend/reuse the existing `CameraAdapter` to support an explicit network-stream source while preserving integer local-device behavior; keep secrets external to source/config committed to Git; emit only bounded observation/event metadata through existing ingress/contracts. Do not implement ONVIF/PTZ/cloud API in this task.

## Validation method
Repository tests must cover local-index backward compatibility, string/RTSP source handling without embedding credentials, failure behavior, and ingress/event semantics. Operational PASS additionally requires a controlled credentialed read from the actual camera and evidence of at least one real frame/observation on the authorized Windows host.

## Scout decision
Repository discovery/preparation is complete. Because final acceptance requires credentialed live camera execution and precision integration with existing adapter/ingress semantics, TASK-008 reaches a HUMAN CODEX/runtime gate.

SCOUT RESULT: READY_FOR_CODEX_REVIEW. No Codex invocation is authorized by this Scout result.
