# TANGRA-COG-V1-EXP-CANDIDATE-01 — Authorized RAW_EVIDENCE → CANDIDATE_LESSON Mechanical Transition

TASK_ID: TANGRA-COG-V1-EXP-CANDIDATE-01
PROJECT: TANGRA
STATUS: COMPLETE — WORKSHOP_QUALIFIED / REVIEWER_PASS
TYPE: BOUNDED UNIT-6 INTEGRATION / QUALIFICATION

OBJECTIVE:
Consume only a qualified EXP-REVIEW-01 RawCandidateReviewResult(status=AUTHORIZED, decision=APPROVE) and perform the existing reviewed COG-22 RAW_EVIDENCE → CANDIDATE_LESSON explicit transition.

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-exp-review-01@249234f5265a9ae4595fbcfc8b91ef82efc353a8

REQUIRED:
- genuine RawCandidateReviewResult
- status AUTHORIZED
- decision APPROVE
- source ID exactly matches existing source record
- source lifecycle remains RAW_EVIDENCE
- reviewed COG-30 disposition remains ACTIVE
- create new immutable CANDIDATE_LESSON record
- deterministic candidate ID from exact source ID + review_ref
- preserve source semantic content unchanged except experience_id, lifecycle, supersedes_experience_id
- supersedes_experience_id = source ID
- append through reviewed COG-22 ExperienceStoreRequest with explicit_transition_from=RAW_EVIDENCE
- identical replay is deterministic/idempotent
- AUTHORITY=NONE / operational_authority=[]

REJECT:
- non-AUTHORIZED review result
- non-APPROVE decision
- source missing
- source not RAW_EVIDENCE
- source not ACTIVE
- source/result mismatch
- reviewed COG-22 transition rejection

PROTECTED:
- reviewed COG-22 implementation
- reviewed COG-30 implementation
- EXP-REVIEW-01 contract
- all upstream adapters

PROHIBITED:
- CANDIDATE_LESSON → VALIDATED_EXPERIENCE
- candidate validation/evaluation policy
- autonomous learning
- thresholds/scores/count/time rules
- model/LLM authorization
- COG-30 mutation or policy-state persistence
- durable review ledger
- COG-21
- Pi/production wiring
- Codex

VALIDATION:
- upstream suites through EXP-REVIEW-01
- EXP-CANDIDATE-01 integration suite
- reviewed COG-22 source tests
- reviewed COG-30 lifecycle tests
- independent Reviewer PASS required

ROLLBACK:
Remove only EXP-CANDIDATE-01 additive files and return to EXP-REVIEW-01 checkpoint.

NEXT_IF_QUALIFIED:
Reconcile CANDIDATE_LESSON → VALIDATED_EXPERIENCE authorization/evidence contract only; do not implement it in this task.

CODEX: NOT_USED
PI_CHANGES: NONE

RESULT:
- WORKSHOP_QUALIFIED
- REVIEWER_PASS
- CHECKPOINT: checkpoints/TANGRA-COG-V1-EXP-CANDIDATE-01.md
- TARGET_HEAD: nevincho/TANGRA-2.0:tangra-cog-v1-exp-candidate-01@3397777b0a2f246bbbf9b1901cfec5c766e8d6a8
- TESTS: 177 PASS / 0 FAIL on bounded qualification surface
- RAW_TO_CANDIDATE: QUALIFIED
- CANDIDATE_TO_VALIDATED: NOT STARTED
- HISTORICAL_317_REGRESSION: NOT EXECUTED
- CODEX: NOT USED
- PI_CHANGES: NONE
- NEXT_DEPENDENCY: reconcile explicit bounded authorization/evidence contract for CANDIDATE_LESSON -> VALIDATED_EXPERIENCE
