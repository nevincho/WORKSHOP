# TANGRA-COG-V1-EXP-VALIDATED-01 — Authorized CANDIDATE_LESSON → VALIDATED_EXPERIENCE Mechanical Transition

TASK_ID: TANGRA-COG-V1-EXP-VALIDATED-01
PROJECT: TANGRA
STATUS: IN_PROGRESS
TYPE: BOUNDED UNIT-6 INTEGRATION / QUALIFICATION

OBJECTIVE:
Consume only a qualified CandidateValidationReviewResult(status=AUTHORIZED, decision=APPROVE) and perform the existing reviewed COG-22 CANDIDATE_LESSON → VALIDATED_EXPERIENCE explicit transition.

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-exp-validate-review-01@3b9d81aad454189770079b73b0757eb2e076646a

REQUIRED:
- genuine CandidateValidationReviewResult
- status AUTHORIZED
- decision APPROVE
- exact source_candidate_experience_id exists
- source lifecycle remains CANDIDATE_LESSON
- reviewed COG-30 disposition remains ACTIVE
- create new immutable VALIDATED_EXPERIENCE record
- deterministic validated ID from exact candidate ID + Stage-2 review_ref
- preserve candidate semantic content unchanged except experience_id, lifecycle, supersedes_experience_id
- supersedes_experience_id = candidate ID
- append through reviewed COG-22 ExperienceStoreRequest with explicit_transition_from=CANDIDATE_LESSON
- identical replay deterministic/idempotent
- AUTHORITY=NONE / operational_authority=[]

PROTECTED:
- reviewed COG-22 implementation
- reviewed COG-30 implementation
- Stage-1 and Stage-2 review contracts
- all upstream Experience adapters

PROHIBITED:
- canonical promotion
- CANONICAL_SYSTEM_KNOWLEDGE creation
- modification of COG-22
- modification of COG-30
- automatic/model/threshold validation
- COG-30 policy-state persistence
- durable review-ledger work
- COG-21
- Pi/production wiring
- Codex

VALIDATION:
- all bounded suites through EXP-VALIDATE-REVIEW-01
- EXP-VALIDATED-01 integration suite
- reviewed COG-22 source tests
- reviewed COG-30 lifecycle tests
- independent Reviewer PASS required

ROLLBACK:
Remove only EXP-VALIDATED-01 additive files and return to EXP-VALIDATE-REVIEW-01 checkpoint.

NEXT_IF_QUALIFIED:
Reconcile canonical-promotion dependency separately. Do not implement canonical promotion in this task.

CODEX: NOT_USED
PI_CHANGES: NONE
