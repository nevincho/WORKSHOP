# TASK-003 — Execution Capability Audit

STATUS: READY
PRIORITY: HIGH
TYPE: NON-DESTRUCTIVE INFRASTRUCTURE AUDIT
SOURCE PLAN: `planning/EXECUTION_CAPABILITY_AUDIT.md`

## Objective
Establish, from direct evidence, the real execution and validation capabilities available to WORKSHOP for TANGRA, VK, and HOROSCOPES before autonomous implementation work is authorized.

## Scope
For each project, determine and record only what can actually be demonstrated in the current execution context:
- repository read/search/history/diff access;
- WORKSHOP write capability;
- target repository write capability, if any;
- runtime/host/filesystem access;
- command/test/build execution capability;
- logs/process/service inspection capability;
- independent validation capability;
- checkpoint/backup/rollback capability;
- protected/destructive-operation boundaries;
- Codex execution route and whether it is actually available.

Expected routes to investigate, not assume:
- TANGRA: WORKSHOP -> `nevincho/TANGRA-DOCS` + controlled Pi5 route.
- VK: WORKSHOP -> `nevincho/TANGRA-DOCS` + `nevincho/LIVE` -> controlled Codex/Windows runtime route.
- HOROSCOPES: WORKSHOP -> controlled Codex/SSH -> Pi4 project/runtime.

## Mandatory methodology
1. Read `planning/EXECUTION_CAPABILITY_AUDIT.md`, `AGENTS.md`, current policies, registry and project profiles before assessment.
2. Repository visibility MUST NOT be treated as proof of runtime access.
3. Use direct tool/evidence checks where available.
4. Record `NOT VERIFIED` for every capability that cannot be demonstrated.
5. Do not fabricate hostnames, paths, SSH availability, credentials, services, tests, or runtime state.
6. Reviewer must evaluate whether the evidence actually proves each claimed capability rather than accepting agent reports.

## Prohibitions
- NO target project implementation changes.
- NO production deployment or service restart.
- NO destructive commands or deletion.
- NO database migration.
- NO force push/history rewrite.
- NO major dependency upgrades.
- NO secrets export.
- NO Codex implementation work. Codex availability may be assessed only within existing policy and without spending capacity on coding.

## Required outputs
- `evidence/TASK-003/CAPABILITY_MATRIX.md`
- `review/TASK-003.md`
- blocker record(s) under `blockers/` for material missing execution routes, if applicable.
- registry/project profile updates ONLY when new facts are directly verified and the update does not overwrite established validated policy.

## Acceptance criteria
1. TANGRA, VK, and HOROSCOPES each have explicit capability status for read/write/execute/validate/checkpoint/rollback.
2. Every VERIFIED capability is backed by direct evidence.
3. Every unavailable or untested capability is `NOT VERIFIED` or `BLOCKED`, not inferred.
4. Independent validation path is identified for each environment claimed operational.
5. Protected/destructive operations remain bounded by existing WORKSHOP policies.
6. No target project/runtime modifications occur.
7. Codex token budget is preserved.
8. Independent Reviewer issues PASS / FAIL / NOT VERIFIED against the audit objective.

## Completion meaning
PASS means the execution capability map is trustworthy enough to decide what autonomous project work may safely be authorized next. PASS does NOT mean all three project execution routes are operational.
