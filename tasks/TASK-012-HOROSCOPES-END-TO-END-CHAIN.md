# TASK-012 — Horoscopes End-to-End Five-Reader Chain

TASK_ID: TASK-012
PROJECT: HOROSCOPES
PRIORITY: HIGH
STATUS: BLOCKED
OBJECTIVE: Build and validate the complete Horoscopes processing chain across the five verified reader components according to the canonical plan established by TASK-011, using the smallest justified changes and preserving working behavior.
SOURCE_PLAN_OR_REQUEST: canonical Horoscopes plan/TODO discovered by TASK-011 + Vlad request 2026-08-24.
CURRENT_STATE: NOT VERIFIED until TASK-011 completes.
PREREQUISITES: TASK-011 PASS; verified Pi4 write/execute/test route; exact five-reader interfaces and missing implementation identified; pre-change checkpoint.
DEPENDENCIES: TASK-011 PASS.
AFFECTED_COMPONENTS: only components proven necessary by TASK-011 for the end-to-end horoscope chain.
PROTECTED_COMPONENTS: existing validated outputs, user data, working services and unrelated Pi4 applications.
EXECUTION_CLASS: CODEX_CANDIDATE
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: all five verified readers participate according to canonical design; shared inputs/normalization/orchestration/output path is coherent; tests prove each stage and the end-to-end objective; failures are attributed to implementation/integration/environment/methodology correctly; no unrelated refactor.
VALIDATION_METHOD: unit/component tests + deterministic integration fixtures where possible + Pi4 end-to-end runtime test + independent review; evening human/live review where output quality requires subjective/product validation.
PRE_CHANGE_CHECKPOINT: REQUIRED.
ROLLBACK_METHOD: restore checkpoint and previous service/config/code state.
EVIDENCE_PATHS: `evidence/TASK-012/`, `review/TASK-012.md`, checkpoint under `checkpoints/`.
