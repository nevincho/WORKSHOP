# TASK-014 — CODEX GATE

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25
CODEX_USED: no

## Decision
Codex is justified for the implementation itself because the versioned normalization/seed contract is an architecture-level compatibility boundary used by all downstream reader pipelines and session behavior.

Automation MUST NOT execute Codex. Vlad approval is required for this specific task.

## Minimal Codex handoff
Task: TASK-014 — Mysticarium Deterministic Divination Engine.

Authoritative target:
- repo: `nevincho/TANGRA-DOCS`
- branch: `agent/mysticarium`
- baseline head: `beebf9884e450cc29f4d0bbae3d89a27a0fc41c0`

Baseline refresh note:
- previous prepared baseline was `31a60a8da267bbda7d8a2ffd6cd63f40cd65b5e9`;
- branch is now 12 commits ahead due to completed/reviewed independent preparation TASK-035 through TASK-039;
- no TASK-014 implementation was detected in that advancement; the current head is the required Codex starting point.

Objective:
Implement the smallest pure deterministic core satisfying `projects/mysticarium/ARCHITECTURE.md`: explicit versioned normalization + deterministic seed + stable bounded selection helper. Preserve identical relevant input/context => identical result.

Required preparation already complete:
- TASK-013 PASS;
- TASK-033 harness PASS;
- TASK-022 provenance-preserving test route PASS;
- TASK-035 through TASK-039 independent preparation PASS/reviewed;
- reproducible test command: `node --test projects/mysticarium/tests/deterministic-harness.test.mjs`.

Affected components:
- new minimal pure module under `projects/mysticarium/engine/` (or equivalently narrow project-local path);
- deterministic test file(s) under `projects/mysticarium/tests/`;
- `projects/mysticarium/TESTING.md` only if command/coverage documentation needs update.

Protected components:
- existing `web/` prototype behavior;
- canon/design content;
- reader-specific pipelines;
- Pi4/runtime/services;
- provider/payment/session/CMS layers.

Acceptance:
1. explicit normalization/contract version;
2. deterministic documented normalization for supported fields;
3. same relevant input + version gives same seed/output;
4. object key insertion order cannot reroll;
5. meaningful relevant input changes are covered;
6. version participates in seed contract;
7. no external dependency unless justified;
8. tests pass through committed harness route;
9. exact commits, test output and rollback point recorded.

Non-goals:
Do not implement TASK-015+ reader pipelines, UI changes, runtime deployment, AI/provider/payment integration, or broad refactors.

After Codex completion, WORKSHOP Reviewer must independently inspect repository diff and rerun provenance-tied tests before PASS.
