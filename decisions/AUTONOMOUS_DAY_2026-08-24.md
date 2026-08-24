# Autonomous Repository Work Envelope — 2026-08-24

STATUS: ACTIVE UNTIL EVENING HUMAN REVIEW
OWNER DECISION: Vlad authorized autonomous repository-only work on VK and Mysticarium through the day, with live/runtime validation deferred until he returns.

## Allowed
- Process eligible VK and Mysticarium tasks in dependency order.
- Read canonical repositories/branches and current repository implementations.
- Create WORKSHOP evidence, reviews, checkpoints, blockers and task transitions.
- Make repository-only implementation changes where the task explicitly authorizes them and branch boundaries are clear.
- Run repository-level/static/unit/mock validation where available.
- Use Codex only through the existing strict Codex Gate and budget policy for justified non-trivial coding.

## Not allowed
- No TANGRA/Pi5 work; TANGRA remains OFFLINE_HOLD.
- No deployment or modification of Pi4 runtime.
- No modification of active Windows runtime `D:\Store\AI`.
- No service restart or production deployment.
- No VK Core/canonical personality mutation or memory promotion.
- No secrets/credentials in repositories.
- No destructive/irreversible operations.
- No claim of live/runtime PASS from repository-only tests.

## Evening gate
Repository PASS means only repository objective validated. Device/runtime integration remains NOT VERIFIED until live human/runtime validation. Any tasks requiring live hardware, credentials, runtime installation or protected-state decisions must stop that dependency chain and leave a precise evening validation/handoff package.

## Scheduling intent
Controller should continue all independent eligible repository-only work in priority/dependency order during each run rather than stopping because another runtime-dependent chain is blocked.
