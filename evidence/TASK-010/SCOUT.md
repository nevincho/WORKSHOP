# TASK-010 — SCOUT / PLANNER

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25

## Necessity / current state
Canonical VK chain prerequisites TASK-007, TASK-028, TASK-032 and TASK-029 are now PASS repository-side. TASK-043 supplies sanitized RFC 5737 discovery fixtures but explicitly does not establish live LAN behavior. Existing task acceptance requires a controlled local-network test and explicit authorization boundaries.

## Prerequisites
Satisfied repository-side:
- shared HomeNode abstraction (TASK-007 PASS)
- registry service (TASK-028 PASS)
- capability normalization layer (TASK-032 PASS)
- device health model (TASK-029 PASS)
- sanitized network-discovery fixtures (TASK-043 PASS)

Still human/runtime-gated:
- explicit authorized local-network scope;
- controlled local-network execution route;
- pre-change runtime checkpoint/rollback confirmation;
- device inventory comparison for acceptance.

## Protected components
VK Core, canonical personality, approved-memory promotion/provenance semantics, credentials/secrets, and unrelated runtime services.

## Validation method
Repository fixtures may validate normalization only. Final TASK-010 PASS requires controlled authorized LAN execution, bounded non-destructive discovery, comparison against known inventory, status/confidence evidence, and independent review. Repository-only evidence cannot satisfy this acceptance method.

## Scout decision
Do not run or simulate live LAN scanning automatically. Repository preparation is already sufficient to define the bounded handoff; additional repository implementation before the authorized runtime route would risk encoding unverified protocol/tooling assumptions.

Proceed to Human Codex Gate for the runtime-sensitive integration/validation step. No Codex invocation is authorized by this Scout result.
