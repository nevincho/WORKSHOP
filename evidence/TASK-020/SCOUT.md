# TASK-020 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility / duplicate check
TASK-019 is PASS/reviewed. TASK-020 is the next canonical Mysticarium task. Search of the authoritative target found no existing Oracle gateway/premium-reading implementation to reuse or reconcile.

## Canon / architecture boundary
The Oracle is a premium deep-reading service and must remain functionally distinct from free deterministic readers. Current architecture deliberately leaves external provider/model and payment provider NOT VERIFIED / not selected. Therefore this task may define only a provider-neutral interface/contract and mockable invocation boundary.

## Smallest justified implementation
Implement a pure gateway adapter that:
- accepts an injected provider object implementing a narrow `generate(request)` contract;
- validates a provider-neutral premium-reading request with question + permitted session/reading context;
- emits an explicit Oracle/premium/deep-reading request envelope;
- returns a normalized gateway response containing provider result data without inventing provider guarantees;
- exposes no credentials, provider selection, payment or live-network behavior.

Tests use an in-memory mock provider and prove request/response contract, Oracle/free-reader distinction, context forwarding and explicit provider failure propagation.

## Protected / non-goals
No provider credentials, HTTP client, paid/live external call, payment integration, provider retention claim, deterministic free-reader modification, visual/canon modification or Pi4 deploy.

## Validation
Interface contract tests/mocks only, no live call, independent review.

## Codex decision
The interface is bounded and provider-neutral with no remote execution. Worker can implement mechanically; Codex is not justified.

SCOUT RESULT: READY_FOR_WORKER
