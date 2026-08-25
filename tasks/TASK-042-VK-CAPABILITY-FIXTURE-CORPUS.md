# TASK-042 — VK Capability Discovery Fixture Corpus

TASK_ID: TASK-042
PROJECT: VK
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Create reusable mock host-capability fixtures and validation expectations for future TASK-032 capability discovery without implementing host probing itself.

## Basis
VK canonical foundation requires discovery of CPU/GPU/RAM/storage/network/display/audio/cameras/microphones/sensors/Bluetooth/Wi-Fi/LAN/models/tools and must not assume a fixed toolset or internet.

## Allowed work
Create fixture profiles for weak/normal/partial hosts, expected normalized capability records, missing/unknown cases and deterministic contract tests compatible with existing repository interfaces where verified.

## Acceptance
- at least three host profiles including partial/missing capability cases;
- unknown/unavailable is distinct from false/absent where justified;
- no fabricated live hardware state;
- deterministic fixture validation;
- clear support relationship to TASK-032, not duplicate implementation;
- evidence + independent review.

## Non-goals
No live hardware probing, no runtime deployment, no capability-health implementation, no Core mutation.