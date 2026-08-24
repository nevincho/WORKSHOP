# WORKSHOP Checkpoint Schema

STATUS: MANDATORY FORMAT FOR VALIDATED WORKING POINTS

Each checkpoint record must include:
- CHECKPOINT_ID
- PROJECT
- TASK_ID
- TIMESTAMP
- TARGET_REPOSITORY_OR_RUNTIME
- BRANCH_OR_RUNTIME_CONTEXT
- COMMIT_SHA / TAG / SNAPSHOT_REFERENCE or NOT VERIFIED
- VALIDATION_EVIDENCE
- TESTS_RUN
- PROTECTED_COMPONENT_STATUS
- ROLLBACK_METHOD
- KNOWN_LIMITATIONS
- REVIEW_VERDICT

Create a checkpoint after every independently validated working point when implementation changed. Reporting cadence is not a substitute for checkpoints.

Do not call a backup/checkpoint validated unless rollback reference and review evidence are sufficient to restore or identify the known-good state.