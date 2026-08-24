# EXECUTION ROUTING POLICY

STATUS: MANDATORY
APPLIES TO: ALL AGENTS, CONTROLLERS, CODEX HANDOFFS

## Routing order
1. Verify current target repository/runtime state.
2. Use the cheapest capable execution path that can safely satisfy the task.
3. Use Codex only when required by complexity/risk and only after inexpensive preparation is complete.
4. Use human manual transfer only as a fallback where automated/Codex access cannot complete the required step.

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