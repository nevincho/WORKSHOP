# TASK-014 — SCOUT / PLANNER PREPARATION

STATUS: READY_FOR_CODEX_GATE
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility
- TASK-013: PASS.
- TASK-033: PASS.
- TASK-022: PASS after exact-blob provenance verification and isolated Node test execution.
- Canonical backlog therefore allows TASK-014 to enter implementation review.

## Authoritative target
- repository: `nevincho/TANGRA-DOCS`
- branch: `agent/mysticarium`
- current verified head before TASK-014 implementation: `31a60a8da267bbda7d8a2ffd6cd63f40cd65b5e9`
- architecture: `projects/mysticarium/ARCHITECTURE.md`

## Verified architecture contract
The architecture requires a deterministic reading pipeline:
`input -> normalize/classify -> determine deterministic seed -> perform divination -> ...`

Identical relevant inputs under the same defined conditions must not reroll fate. Normalization/versioning must be explicit so content updates do not silently alter active-session readings.

## Smallest justified implementation
Implement only the deterministic core contract, isolated from reader-specific pipelines:
- a versioned normalization function for a deliberately small, explicit input schema;
- a deterministic seed function based only on normalized relevant inputs + normalization version;
- a stable pure helper that maps the seed to a bounded integer/index for downstream divination selection;
- tests for identical input stability, irrelevant key ordering, meaningful input changes, and explicit version influence.

Suggested affected area:
- new pure module under `projects/mysticarium/engine/` or equivalent minimal project-local path;
- extend/replace the fixture-only harness under `projects/mysticarium/tests/` to test the real module;
- update `TESTING.md` only as required.

## Protected / non-goals
- do not modify existing web prototype behavior;
- do not implement Djalma/Morrigan/Selene/Al-Hakim reader pipelines;
- do not add session persistence, provider/payment logic, CMS, or Pi4 deployment;
- do not modify canon content;
- no external dependencies unless technically unavoidable and explicitly justified.

## Acceptance criteria
1. Version constant/contract is explicit.
2. Normalization is deterministic and documented for the supported schema.
3. Same relevant input + same version => identical seed/output.
4. Input object key insertion order does not affect result.
5. A meaningful relevant input change affects the deterministic result in test coverage.
6. Version change is represented in the seed contract.
7. Existing TASK-033 harness route runs tests against exact committed bytes.
8. Rollback point is recorded.
9. Independent review confirms no reader pipeline/runtime scope leakage.

## Why this is not mechanical Worker work
The precise normalization schema and seed contract become a compatibility boundary for all downstream readers and sessions. A poor choice would create architectural debt and silent reading instability. Precision implementation is therefore justified for Codex Gate review rather than ad-hoc Worker coding.

SCOUT RESULT: READY_FOR_CODEX_GATE
