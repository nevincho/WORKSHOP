# TASK-011 — Horoscopes Five-Reader Pipeline Audit

TASK_ID: TASK-011
PROJECT: HOROSCOPES
PRIORITY: HIGH
STATUS: BLOCKED
OBJECTIVE: Discover and verify the actual five reader/fortune-teller components configured in the Horoscopes system, their current code/runtime state, data flow, inputs, outputs, dependencies, and canonical plan before any implementation expansion.
SOURCE_PLAN_OR_REQUEST: Vlad request 2026-08-24; exact five-reader definitions must come from current Pi4/project evidence.
CURRENT_STATE: Exact project path, repository, five-reader names/components, canonical plan and runtime state NOT VERIFIED.
PREREQUISITES: TASK-004 PASS for Horoscopes/Pi4 route or equivalent verified read-only access.
DEPENDENCIES: TASK-004 PASS for HOROSCOPES route.
AFFECTED_COMPONENTS: read-only audit of Horoscopes project/runtime.
PROTECTED_COMPONENTS: existing validated horoscope outputs/data and any working production service; preserve until evidence supports change.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO for discovery/audit.
ACCEPTANCE_CRITERIA: all five reader components are named from direct evidence; current implementation status and interfaces are mapped; canonical plan/TODO is identified; duplicates/missing prerequisites are reported; end-to-end target chain is defined without inventing missing behavior.
VALIDATION_METHOD: direct Pi4/repository inspection + code/config/runtime evidence + independent review.
PRE_CHANGE_CHECKPOINT: NOT APPLICABLE — read-only.
ROLLBACK_METHOD: NOT APPLICABLE — no target changes.
EVIDENCE_PATHS: `evidence/TASK-011/`, `review/TASK-011.md`.
