# TASK-036 — Mysticarium Presentation Metadata Contract

TASK_ID: TASK-036
PROJECT: MYSTICARIUM
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Define and validate the reading-to-chamber presentation metadata contract described by canon so future reading engines can return restrained environment reactions without coupling divination logic to UI implementation.

## Basis
`MYSTICARIUM_CANON.md` defines presentation metadata such as tone, intensity, event and element and maps them to restrained chamber reactions.

## Allowed work
Create a minimal versioned contract plus fixtures/tests for values such as hopeful/uncertain/warning/ominous, intensity bounds and optional event/element metadata. Preserve current visual/audio canon.

## Acceptance
- explicit versioned contract;
- invalid/unknown values handled deterministically;
- representative fixtures for at least four semantic tones;
- tests or deterministic schema validation;
- no modification of locked character canon;
- evidence + independent review.

## Non-goals
No scene-engine redesign, no new art/audio assets, no browser runtime deployment, no reader implementation.