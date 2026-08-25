# TASK-037 — Mysticarium Ephemeral Session TTL Contract

TASK_ID: TASK-037
PROJECT: MYSTICARIUM
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Prepare the temporary-session data contract and deterministic expiry/cleanup behavior required by the privacy architecture, without deploying a Pi4 session service.

## Basis
Architecture/canon require no mandatory account, no persistent behavioral profile, temporary session memory only, explicit TTL and cleanup.

## Allowed work
Define session fields/status/TTL semantics and implement harmless mock/fixture tests for create/read/expire/cleanup behavior using repository-side simulation only.

## Acceptance
- explicit TTL semantics and cleanup states;
- no implicit persistent user profile;
- deterministic mocked expiry tests including boundary cases;
- provenance/privacy notes consistent with canon;
- evidence + rollback + independent review.

## Non-goals
No live database, no Pi4 deployment, no authentication system, no payment/user-account implementation.