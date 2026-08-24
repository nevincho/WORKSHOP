# TASK-019 — Mysticarium Ephemeral Session and Privacy Layer

TASK_ID: TASK-019
PROJECT: HOROSCOPES / MYSTICARIUM
PRIORITY: MEDIUM
STATUS: BLOCKED
DEPENDS_ON: TASK-018 PASS
TYPE: REPOSITORY-ONLY IMPLEMENTATION
OBJECTIVE: Implement the canonical temporary session-memory contract with explicit TTL/cleanup and temporary media lifecycle scaffolding, without persistent user profiles.

BOUNDARY: repository branch only; no Pi4 deploy; no claims about third-party retention beyond verified provider behavior; no payment integration.
VALIDATION: session expiry tests, cleanup tests, no-persistent-profile evidence, independent review.
