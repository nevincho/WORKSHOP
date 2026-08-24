# TASK-027 — Mysticarium Ephemeral Session Memory

PROJECT: HOROSCOPES / MYSTICARIUM
STATUS: BLOCKED
DEPENDS_ON: TASK-026 PASS
OBJECTIVE: Implement repository-side ephemeral session context for names, relationships, prior questions/readings and relevant context with explicit expiry/cleanup semantics.
BOUNDARIES: No persistent user-profile database; preserve privacy canon; no unsupported retention claims.
ACCEPTANCE: Session lifecycle and cleanup tests PASS; no persistent profile semantics introduced; Reviewer PASS.
