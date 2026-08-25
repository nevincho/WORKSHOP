# TASK-019 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility
TASK-018 is PASS/reviewed. TASK-019 is the next canonical Mysticarium task.

## Existing preparation
The target already contains repository/simulation contracts for ephemeral sessions and temporary media, plus fixture-level TTL/media tests from prior preparation. Those tests currently implement helper behavior inline; no reusable session/media implementation module exists.

Verified session semantics: opaque session ID, explicit positive TTL, active only while `now < expires_at`, expiry at boundary, cleanup deletes temporary context and is idempotent, no account/profile/canonical-memory semantics.

Verified media semantics: bounded local lifecycle, expiry/failure/success cleanup to deleted, raw bytes not retained after deletion, provider transfer is evidence only and never proof of provider deletion.

## Smallest justified implementation
Promote the already-defined pure simulation semantics into reusable repository modules and point tests at those modules. Keep all clocks/timestamps caller-supplied for deterministic tests. Do not add persistence, database, account identity, provider or upload service.

## Protected / non-goals
No Pi4 deploy/service, persistent user profile, identity correlation, canonical memory, third-party retention claim, payment/provider integration, filesystem upload handler or web changes.

## Validation
Session expiry boundary, read-before-expiry, cleanup idempotence/context removal; media valid transitions, expiry/failure/success deletion semantics, idempotence/raw payload removal; evidence that no persistence/account/profile interface is introduced; independent review.

## Codex decision
Contracts and fixture behavior are explicit and implementation is mechanical/pure. Codex is not justified.

SCOUT RESULT: READY_FOR_WORKER
