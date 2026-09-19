# SELF-MODEL-02 — HUMAN GATE / EXECUTION ROUTE

STATUS: HUMAN_GATE
DATE: 2026-09-19
TASK: SELF-MODEL-02

## Exact blocker

SELF-MODEL-02 requires one execution route that can both mutate `nevincho/TANGRA-2.0:tai-cog-32-package` and execute its Python primary/confirmation/regression tests. No currently authorized and verified non-Codex route satisfies both capabilities.

## Routes checked

1. WORKSHOP repository Worker / GitHub repository route
   - Repository read/write: VERIFIED.
   - Target branch access: VERIFIED.
   - Command/Python runner: unavailable in the current route.
   - Result: cannot satisfy validation policy.

2. WORKSHOP AUTO/controller route
   - Current WORKSHOP state defines repository read/write/review as autonomous when authorized.
   - No shell/command/runner connection for TANGRA is defined or verified.
   - Result: no additional executable capability beyond repository-side operations is evidenced.

3. TANGRA local/runtime route
   - `registry/CONNECTIONS.md`: TANGRA production/runtime host/path NOT VERIFIED.
   - `projects/TANGRA.md`: Phase A permits repository-safe engineering/tests but defines no local checkout/runner/SSH connection.
   - Result: no verified local executable route.

4. SSH route
   - WORKSHOP only records an expected/verified SSH route for Horoscopes/Pi4, not TANGRA engineering.
   - No TANGRA SSH host/path/credentials/runner is defined.
   - Result: unavailable for SELF-MODEL-02; cross-project route must not be inferred.

5. Windows/local human bridge
   - WORKSHOP defines Windows local execution for VK/ESP32 contexts, not for the TANGRA-2.0 engineering checkout.
   - No verified TANGRA-2.0 local checkout/test route is recorded.
   - Result: unavailable until explicitly provided/authorized.

6. Codex
   - Capable in principle of local/SSH execution only where separately authorized.
   - `projects/TANGRA.md`: `TAI_CODEX_AUTHORITY: NONE`.
   - `tasks/SELF-MODEL-02.md`: `CODEX_ALLOWED: NO`.
   - Result: prohibited for this task under current policy.

## Affected dependency chain

SELF-MODEL-02 only. SELF-MODEL-03 must not start.

## Safe current checkpoint

`nevincho/TANGRA-2.0:tai-cog-32-package @ 9629a624358b8ae539ac1af54af72b9828ba5632`

No SELF-MODEL-02 implementation mutation exists.

## Smallest human decision/action required

Provide and authorize a local executable checkout/runner route for `nevincho/TANGRA-2.0:tai-cog-32-package` that the WORKSHOP Worker can use for repository mutation and Python test execution.

This does NOT require a Codex exception if a Worker-accessible local checkout/runner is supplied. If no such Worker route can be supplied, the alternative requires an explicit task-specific Codex exception from Vlad; current policy does not permit WORKSHOP to grant that exception itself.

## Allowed independent work

No dependent Self Model implementation work. Existing unrelated campaigns remain governed by their own state/policy.
