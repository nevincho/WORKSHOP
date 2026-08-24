# WORKSHOP Controller Run Ledger

Purpose: append-only operational ledger for every controller execution attempt that reaches WORKSHOP.

Each run must append one entry with:
- scheduled_time_uk
- observed_start_time_uk
- controller_name
- run_sequence/status
- queue_snapshot: READY/BLOCKED counts and selected task IDs
- actions_started
- actions_completed
- actions_failed_or_blocked
- Codex_used: yes/no
- repository_commits_created
- evidence/review files created
- exit_reason
- next_expected_run

Rules:
1. Append only. Do not rewrite or delete prior run entries except to repair formatting errors with an explicit correction note.
2. A scheduler event that never starts cannot write to this ledger. Absence of an expected entry is therefore evidence of a scheduler-level failure or non-start, not a task failure.
3. If a run starts but fails before task execution, record STARTED plus the failure/exit reason before returning whenever repository write remains available.
4. Do not treat this ledger as implementation authority; it is coordination telemetry only.

---
