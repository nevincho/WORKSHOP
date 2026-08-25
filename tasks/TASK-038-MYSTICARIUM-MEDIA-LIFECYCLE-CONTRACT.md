# TASK-038 — Mysticarium Temporary Media Lifecycle Contract

TASK_ID: TASK-038
PROJECT: MYSTICARIUM
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Define and test the temporary upload/media lifecycle required for future palm/coffee image processing without making unverified retention/privacy claims.

## Basis
Architecture/canon require temporary media handling, explicit cleanup, and privacy claims no stronger than eventual provider behavior.

## Allowed work
Prepare lifecycle states, mock upload metadata, expiry/delete behavior and deterministic cleanup tests. Keep provider-specific behavior marked NOT VERIFIED.

## Acceptance
- lifecycle states and deletion/expiry semantics documented;
- provider boundary explicit;
- mock tests cover normal cleanup, expired media and failed-processing cleanup;
- no durable raw media retention introduced;
- evidence + independent review.

## Non-goals
No vision API/provider selection, no real image upload service, no Pi4 deployment, no production privacy claim.