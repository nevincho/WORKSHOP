# WORKSHOP State Machine

STATUS: MANDATORY

Task states:

READY -> IN_PROGRESS -> REVIEW -> COMPLETE

Alternative transitions:
- READY -> HOLD
- READY/IN_PROGRESS/REVIEW -> BLOCKED
- BLOCKED -> READY only when ALL task-specific unblock conditions are independently verified as satisfied
- REVIEW -> REWORK -> IN_PROGRESS
- any non-COMPLETE state -> HUMAN_GATE when policy requires

Rules:
1. READY requires task schema completeness sufficient to evaluate prerequisites.
2. IN_PROGRESS requires a verified executor/routing decision.
3. REVIEW requires execution evidence or a reviewable diagnostic result.
4. COMPLETE requires independent Reviewer PASS and checkpoint reference when implementation changed.
5. BLOCKED must record blocker, evidence, affected dependency chain, and smallest required unblock action.
6. BLOCKED -> READY is an evidence-based promotion: dependency completion alone does not authorize it if any additional prerequisite, execution-route, validation, credential, hardware, policy, checkpoint, rollback or human-gate condition remains unsatisfied/NOT VERIFIED. The promotion decision and evidence must be persisted.
7. HOLD is intentional deferral, not failure.
8. HUMAN_GATE requires a Control Room decision record before the blocked chain resumes.
9. A report, agent claim, or Codex completion cannot transition a task directly to COMPLETE.
10. After a valid BLOCKED -> READY promotion, the Controller may process the newly eligible task in the same run; there is no fixed task-count limit.

Independent tasks may progress while another dependency chain is blocked.