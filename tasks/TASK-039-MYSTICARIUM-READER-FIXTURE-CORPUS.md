# TASK-039 — Mysticarium Reader Fixture Corpus

TASK_ID: TASK-039
PROJECT: MYSTICARIUM
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Create a compact canonical fixture corpus for the four free readers — Djalma, Morrigan, Selene and Al-Hakim — so later implementations can be tested against character/domain boundaries without hard-coding full predictions.

## Basis
`MYSTICARIUM_CANON.md` locks each character's role/domain and requires rich coherent free readings.

## Allowed work
Create representative normalized input fixtures and expected structural/domain properties only. Include positive and negative/invalid-domain cases. Do not prescribe exact prose outputs.

## Acceptance
- fixtures cover all four free readers;
- domain boundaries reflected correctly;
- fixtures test structure/contract rather than exact prose;
- no Oracle conflation;
- evidence + independent review.

## Non-goals
No reader implementation, no deterministic engine, no paid Oracle, no visual assets.