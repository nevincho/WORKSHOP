# TASK-040 — VK Sensor/Event Envelope + Provenance Contract

TASK_ID: TASK-040
PROJECT: VK
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Define and validate the shared event envelope for camera/microphone/network/sensor observations so future device integrations normalize into one reusable mechanism while preserving provenance.

## Basis
VK canonical foundation requires shared event representation, sensor/input ingestion, provenance/confidence and reuse-before-replication. Camera, microphone, chat and later LoRa must not create independent memory architectures.

## Allowed work
Inspect current repository interfaces, define the smallest compatible event contract, add mock fixtures/tests where justified, and avoid Core/personality mutation.

## Acceptance
- source device/type/time/provenance/confidence or equivalent explicitly represented;
- distinguishes VK_ORIGINATED / EXTERNAL_FACT / INFERENCE where applicable without promoting to canonical memory;
- mock fixtures for at least camera, microphone and network/device event classes;
- deterministic contract validation;
- evidence + independent review.

## Non-goals
No live sensor access, no memory promotion, no Core schema redesign, no IMOU/Echo runtime integration.