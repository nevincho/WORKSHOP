# TASK-010 — CODEX GATE

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25
CODEX_USED: no

## Decision
TASK-010 has reached a real Human Codex/runtime gate. Automation MUST NOT invoke Codex or scan the local network. Vlad approval is required for this specific task and must include an authorized LAN scope before execution.

## Minimal handoff
Task: TASK-010 — VK Home Network Device Discovery.

Authoritative target:
- repo: `nevincho/LIVE`
- branch: `Legacy`
- current repository baseline at preparation: `553b0a1aa92b591aa431442555b859574112600d` plus TASK-032/TASK-029 subsequent repository commits; Codex must re-check actual HEAD before modifying or executing.

Objective:
Implement/validate the smallest bounded non-destructive discovery/status path that feeds existing TASK-007/TASK-028 abstractions and distinguishes observation from usable capability.

Prerequisites already prepared:
- TASK-007, TASK-028, TASK-032, TASK-029 PASS repository-side;
- TASK-043 sanitized discovery fixtures PASS.

Human inputs/gates required before execution:
1. explicit authorized local-network scope/range and allowed target devices;
2. confirmation of execution host/runtime route;
3. pre-change checkpoint/rollback confirmation;
4. permission for bounded non-destructive network discovery on that scope.

Acceptance:
- discovery restricted to authorized scope;
- no destructive scanning, credentials, or secret exposure;
- discovered service/port evidence is not promoted to protocol capability without validation;
- observations feed existing HomeNode/DeviceRegistry rather than creating duplicate state;
- confidence/status recorded;
- controlled LAN result compared with known device inventory;
- exact commits/test/runtime evidence and rollback recorded;
- independent Reviewer PASS.

Non-goals:
No VK Core/personality/memory changes; no credential extraction; no broad LAN scan; no IMOU/Echo feature implementation; no claim of live protocol support from fixtures.

Codex was not invoked by the controller.
