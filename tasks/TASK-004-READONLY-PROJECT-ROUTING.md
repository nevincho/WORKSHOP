# TASK-004 — Read-Only Project Routing Validation

STATUS: READY
PRIORITY: HIGH
DEPENDS_ON: TASK-003 PASS — SATISFIED
TYPE: NON-DESTRUCTIVE VALIDATION

## Objective
Using only execution routes VERIFIED by TASK-003, validate read-only routing into each project environment that is proven accessible.

## Rules
- Do not attempt unverified routes.
- Do not modify target repositories/runtimes.
- Do not use Codex for discovery or routine inspection.
- Preserve existing WORKSHOP policies and project protection boundaries.
- TASK-003 verified repository read routes for TANGRA and VK; it did NOT verify Pi5, Windows-runtime, Horoscopes target, or Pi4 routes.

## Required outputs
- `evidence/TASK-004/ROUTING_VALIDATION.md`
- `review/TASK-004.md`

## Acceptance criteria
1. Each VERIFIED execution route from TASK-003 is exercised read-only.
2. Each route is independently reviewed.
3. Any route not available remains NOT VERIFIED/BLOCKED.
4. No target modification occurs.

## Unblock condition
SATISFIED: TASK-003 independent review PASS identified usable repository read-only routes.