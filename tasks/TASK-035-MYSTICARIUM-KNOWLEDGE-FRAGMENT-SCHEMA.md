# TASK-035 — Mysticarium Knowledge Fragment Schema

TASK_ID: TASK-035
PROJECT: MYSTICARIUM
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Define and validate the smallest structured knowledge-fragment schema needed by the documented free-reading pipeline so future readers can compose readings from reusable semantic fragments instead of canned full predictions.

## Authoritative design basis
- `projects/mysticarium/ARCHITECTURE.md`: structured semantic fragments/rules and free-reading pipeline.
- `projects/mysticarium/MYSTICARIUM_CANON.md`: free characters must provide coherent rich readings.

## Allowed work
- inspect current `agent/mysticarium` repository state;
- add minimal schema/contract documentation and harmless fixtures/tests in the project repository when justified;
- use representative sample fragments only;
- simulate retrieval/composition validation without implementing the full deterministic engine or reader pipelines.

## Acceptance
- explicit fields for identity/domain/context/meaning/tone/source/version or equivalent justified structure;
- provenance/versioning represented;
- at least one deterministic fixture validation or schema check;
- evidence records exact target ref/files/test result/rollback point;
- independent review.

## Non-goals
No TASK-014 engine, no Djalma/Morrigan/Selene/Al-Hakim full implementation, no Pi4 deployment, no Oracle AI, no production claims.