# TASK-043 — VK Network Discovery Fixture Corpus

TASK_ID: TASK-043
PROJECT: VK
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Prepare deterministic mock network-discovery fixtures for future TASK-010 so device discovery logic can be tested without touching Vlad's live LAN.

## Allowed work
Create sanitized mock scan/discovery inputs for reachable/unreachable devices, known/unknown services and duplicate identities; define expected normalized outputs against existing contracts where verified.

## Acceptance
- fixtures cover at least camera-like, audio-like, generic and unknown LAN devices;
- service/port presence is treated as evidence, not proof of higher-level protocol functionality;
- no real credentials or private addresses required in committed fixtures;
- deterministic validation/tests;
- explicit support relationship to TASK-010;
- evidence + independent review.

## Non-goals
No live network scan, no IMOU stream claim, no Echo integration, no runtime deployment.