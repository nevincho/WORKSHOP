# WORKSHOP State Machine

STATUS: MANDATORY

Task states:

READY -> IN_PROGRESS -> REVIEW -> COMPLETE

Alternative transitions:
- READY -> HOLD
- READY/IN_PROGRESS/REVIEW -> BLOCKED
- REVIEW -> REWORK -> IN_PROGRESS
- any non-COMPLETE state -> HUMAN_GATE when policy requires

Rules:
1. READY requires task schema completeness sufficient to evaluate prerequisites.
2. IN_PROGRESS requires a verified executor/routing decision.
3. REVIEW requires execution evidence or a reviewable diagnostic result.
4. COMPLETE requires independent Reviewer PASS and checkpoint reference when implementation changed.
5. BLOCKED must record blocker, evidence, affected dependency chain, and smallest required unblock action.
6. HOLD is intentional deferral, not failure.
7. HUMAN_GATE requires a Control Room decision record before the blocked chain resumes.
8. A report, agent claim, or Codex completion cannot transition a task directly to COMPLETE.

Independent tasks may progress while another dependency chain is blocked.