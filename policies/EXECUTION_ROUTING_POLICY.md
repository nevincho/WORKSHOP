# EXECUTION ROUTING POLICY

STATUS: MANDATORY
APPLIES TO: ALL AGENTS, CONTROLLERS, CODEX HANDOFFS

## Routing order
1. Verify current target repository/runtime state.
2. Use the cheapest capable execution path that can safely satisfy the task.
3. Use Codex only when required by complexity/risk and only after inexpensive preparation is complete.
4. Use human manual transfer only as a fallback where automated/Codex access cannot complete the required step.

## Repository-side Worker Python execution guard
For repository-side Worker Python validation in an isolated execution environment, lack of outbound GitHub network MUST NOT by itself be interpreted as inability to execute.

Before declaring `BLOCKED — EXECUTION ACCESS`, orchestration MUST check the established repository-payload execution route:
`authenticated repository/submitted payload -> temporary exact-content execution mirror -> Python/shell validation -> independent authoritative repository/blob identity verification`.

Rules:
- Do not invent authenticated Git clone/checkout inside the isolated Python environment as a prerequisite when the assigned execution model uses submitted repository payloads.
- Preserve repository-relative paths and exact source content in the temporary mirror.
- Record authoritative repository, ref, commit/tree identity and relevant blob identities before execution.
- Preserve raw commands, stdout/stderr, exit codes and relevant environment facts.
- Verify executed payload identity against authoritative repository content after execution before accepting qualification.
- A temporary execution mirror is not implementation authority and must not weaken repository-as-authority rules.
- If the payload-to-mirror platform operation itself is unavailable, name that exact boundary as the blocker; do not substitute generic Git/network failure.
- Historical incident and rationale: `control_room/WORKER_EXECUTION_INCIDENT_2026-09-20.md`.

## Project routing
### TANGRA
Default: monitor, audit, validate, report. No autonomous implementation unless explicitly authorized.

### VK
Default: autonomous work on runtime, tooling, UI, diagnostics, tests and approved non-Core integration.
Protected Core/canonical personality/approved-memory changes require human authorization.
Execution order: AUTO -> CODEX -> HUMAN BRIDGE.

### Horoscopes
Default: autonomous implementation against verified canonical plan/TODO.
Use Pi4/SSH path when available and authorized.
Execution order: AUTO -> CODEX/SSH.

## Mandatory constraints
- Never infer access that has not been verified in the current execution context.
- If an execution path is unavailable, record BLOCKED — EXECUTION ACCESS with evidence.
- Do not duplicate functionality because a preferred execution path is unavailable.
- Preserve validated interfaces and rollback capability.
