# TANGRA-COG-V1-EXP-VALIDATE-REVIEW-01 — Second-Stage Candidate Validation Review Contract

TASK_ID: TANGRA-COG-V1-EXP-VALIDATE-REVIEW-01
PROJECT: TANGRA
STATUS: COMPLETE — WORKSHOP_QUALIFIED / REVIEWER_PASS
TYPE: BOUNDED CONTRACT IMPLEMENTATION / QUALIFICATION

OBJECTIVE:
Implement and qualify only the second-stage human-review authorization contract defined by:
decisions/TANGRA_COG_V1_CANDIDATE_VALIDATED_REVIEW_CONTRACT_2026-09-26.md

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-exp-candidate-01@3397777b0a2f246bbbf9b1901cfec5c766e8d6a8

REQUIRED:
- CandidateValidationReview immutable contract
- separate Stage-2 review_ref
- exact source CANDIDATE_LESSON ID
- explicit reviewer identity
- explicit APPROVE / REJECT
- non-empty bound evidence refs
- explicit reason
- prior_raw_candidate_review_ref
- genuine prior qualified RawCandidateReviewResult(AUTHORIZED/APPROVE)
- exact Stage-1 -> Stage-2 chain validation
- candidate remains ACTIVE in reviewed COG-30
- authority=NONE / operational_authority=[]

TWO_STAGE_INVARIANT:
- Stage-1 RAW -> CANDIDATE authorization cannot substitute for Stage-2 authorization.
- Stage-2 review_ref must differ from Stage-1 review_ref.
- Stage-2 candidate must be the deterministic candidate generated from the prior Stage-1 source ID + Stage-1 review_ref.

PROHIBITED:
- actual CANDIDATE_LESSON -> VALIDATED_EXPERIENCE transition
- modification of COG-22
- modification of COG-30
- canonical promotion
- automatic/model/threshold validation
- identity-authentication infrastructure
- durable review ledger
- COG-30 policy-state persistence
- COG-21
- Pi/production wiring
- Codex

VALIDATION:
- upstream suites through EXP-CANDIDATE-01
- new second-stage review-contract suite
- reviewed COG-22 tests
- reviewed COG-30 tests
- independent Reviewer PASS before checkpoint

NEXT_IF_QUALIFIED:
Reconcile only the smallest mechanical adapter consuming Stage-2 AUTHORIZED and using existing reviewed COG-22 CANDIDATE_LESSON -> VALIDATED_EXPERIENCE transition. Do not implement it in this task.

CODEX: NOT_USED
PI_CHANGES: NONE

RESULT:
- WORKSHOP_QUALIFIED
- REVIEWER_PASS
- CHECKPOINT: checkpoints/TANGRA-COG-V1-EXP-VALIDATE-REVIEW-01.md
- TARGET_HEAD: nevincho/TANGRA-2.0:tangra-cog-v1-exp-validate-review-01@3b9d81aad454189770079b73b0757eb2e076646a
- TESTS: 190 PASS / 0 FAIL on bounded qualification surface
- TWO_STAGE_OPERATOR_APPROVAL: PRESERVED
- CANDIDATE_TO_VALIDATED_TRANSITION: NOT IMPLEMENTED / NOT EXECUTED
- HISTORICAL_317_REGRESSION: NOT EXECUTED
- CODEX: NOT USED
- PI_CHANGES: NONE
- NEXT_DEPENDENCY: reconcile mechanical AUTHORIZED Stage-2 review consumer for existing COG-22 CANDIDATE_LESSON -> VALIDATED_EXPERIENCE transition
