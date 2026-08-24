# CHECKPOINT AND BACKUP POLICY

STATUS: MANDATORY
APPLIES TO: ALL PROJECT EXECUTION

## Principle
Time-based reports are not backups. Every independently validated working point must have a recoverable checkpoint before dependent work proceeds.

## Required behavior
- After validation PASS, record the exact repository commit/tag/branch/runtime snapshot reference that represents the working state.
- Preserve the immediately previous validated checkpoint until the new state is independently verified and rollback is demonstrated or clearly available.
- Do not label a checkpoint VALIDATED based only on an implementation-agent report.
- For runtime-only state that is not yet committed, record the minimum reproducible snapshot/backup reference permitted by the target-project policy.
- Never overwrite the only known-good state with an unvalidated state.

## Rollback record
Each task that changes implementation must identify:
- pre-change checkpoint;
- post-change validated checkpoint if PASS;
- rollback method;
- irreversible side effects, if any.

If rollback cannot be established for a risky change, invoke a HUMAN GATE before execution.