# TASK-041 — VK Device Registry Contract + Fixtures

TASK_ID: TASK-041
PROJECT: VK
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Prepare the device-registry contract and fixtures needed by future Home Node/device work without implementing the live node layer itself.

## Basis
VK architecture requires smart-home/device inventory, capability discovery and reusable shared mechanisms. TASK-028 remains the later implementation authority for Device Registry.

## Allowed work
Define a minimal registry schema/contract and mock fixtures for cameras, audio devices and generic LAN nodes. Reconcile with existing repository interfaces where present. Do not implement TASK-028 runtime behavior.

## Acceptance
- stable device identity, type, capabilities, connectivity/status and provenance fields or justified equivalents;
- fixtures include IMOU-like camera, Echo-like audio endpoint and generic node without embedding credentials;
- deterministic schema validation/tests;
- clear handoff notes for TASK-028;
- evidence + independent review.

## Non-goals
No device discovery, no live network scanning, no runtime registration service, no credentials, no Core mutation.