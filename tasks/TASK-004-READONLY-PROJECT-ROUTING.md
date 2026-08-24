# TASK-004 — Read-Only Project Routing Validation

STATUS: BLOCKED
PRIORITY: HIGH
DEPENDS_ON: TASK-003 PASS
TYPE: NON-DESTRUCTIVE VALIDATION

## Objective
Using only execution routes VERIFIED by TASK-003, validate read-only routing into each project environment that is proven accessible.

## Rules
- Do not attempt unverified routes.
- Do not modify target repositories/runtimes.
- Do not use Codex for discovery or routine inspection.
- Preserve existing WORKSHOP policies and project protection boundaries.

## Required outputs
- `evidence/TASK-004/ROUTING_VALIDATION.md`
- `review/TASK-004.md`

## Acceptance criteria
1. Each VERIFIED execution route from TASK-003 is exercised read-only.
2. Each route is independently reviewed.
3. Any route not available remains NOT VERIFIED/BLOCKED.
4. No target modification occurs.

## Unblock condition
TASK-003 independent review is PASS and identifies at least one usable read-only project route.
