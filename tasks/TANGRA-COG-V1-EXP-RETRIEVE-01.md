# TANGRA-COG-V1-EXP-RETRIEVE-01 — Restart-Safe Read-Only VALIDATED_EXPERIENCE Retrieval

TASK_ID: TANGRA-COG-V1-EXP-RETRIEVE-01
PROJECT: TANGRA
STATUS: IN_PROGRESS
TYPE: BOUNDED UNIT-6 READ-ONLY INTEGRATION / QUALIFICATION

OBJECTIVE:
Add the smallest restart-safe read-only retrieval boundary for persisted VALIDATED_EXPERIENCE using qualified EXP-PERSIST-01 loading and existing reviewed COG-22 ExperienceQuery semantics.

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-exp-validated-01@dd3f74b21cf7c2860bd82674867936dbe73c6a82

REQUIRED:
- load only through DurableExperienceSnapshotStore.load()
- require LOADED snapshot result before querying
- query only through reviewed COG-22 ExperienceStore.query()
- force lifecycle=VALIDATED_EXPERIENCE
- return genuine reviewed COG-22 ExperienceRecord values unchanged
- allow existing reviewed COG-22 read-only filters: event_type, subsystem_domain, outcome, evidence_ref, start/end timestamp, configuration_profile_ref, limit
- preserve reviewed COG-22 deterministic ordering/truncation/status
- no fallback to RAW_EVIDENCE or CANDIDATE_LESSON
- missing/invalid snapshot returns bounded retrieval failure/no records
- MISSION_CONSTRAINED remains unsupported per reviewed COG-22
- AUTHORITY=NONE / operational_authority=[]

PROTECTED:
- reviewed COG-22
- reviewed COG-30
- EXP-PERSIST-01
- EXP-VALIDATED-01 and all earlier Experience gates
- Cognitive Bridge

PROHIBITED:
- Canonical Promotion / CANONICAL_SYSTEM_KNOWLEDGE
- post-mission orchestration wiring
- FAST/verbal integration
- model/LLM work
- COG-21
- Pi/production wiring
- Codex
- write/append/transition/promotion APIs

VALIDATION:
- all bounded suites through EXP-VALIDATED-01
- EXP-RETRIEVE-01 suite
- reviewed COG-22 source tests
- reviewed COG-30 lifecycle tests
- independent Reviewer PASS before checkpoint

ROLLBACK:
Remove only EXP-RETRIEVE-01 additive files and return to EXP-VALIDATED-01 checkpoint.

NEXT_IF_QUALIFIED:
Reconcile the smallest post-mission orchestration composition that consumes the qualified read-only VALIDATED_EXPERIENCE retrieval boundary. Do not implement orchestration in this task.

CANONICAL_PROMOTION: DEFERRED
CODEX: NOT_USED
PI_CHANGES: NONE
