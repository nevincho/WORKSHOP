# TANGRA-COG-V1-EXP-REVIEW-01

TASK_ID: TANGRA-COG-V1-EXP-REVIEW-01
PROJECT: TANGRA
STATUS: READY
TYPE: BOUNDED CONTRACT IMPLEMENTATION / QUALIFICATION

OBJECTIVE:
Implement and qualify the additive RAW_EVIDENCE -> CANDIDATE_LESSON human-review authorization contract defined in:
decisions/TANGRA_COG_V1_RAW_CANDIDATE_REVIEW_CONTRACT_2026-09-26.md

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-exp-life-01@b6db74d02365ccf2aad5e1a6e755525233c51584

IMPLEMENTATION_LOCATION:
TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_candidate_review_contract.py

REQUIRED CONTRACT:
- review_ref
- source_experience_id
- reviewer_id
- explicit APPROVE or REJECT
- non-empty bound evidence_refs
- non-empty reason
- authority=NONE
- operational_authority=[]

REQUIRED VALIDATION:
- source exists in reviewed COG-22 store
- source lifecycle is RAW_EVIDENCE
- reviewed COG-30 policy reports source ACTIVE
- every review evidence ref is already bound to the exact source record
- APPROVE returns AUTHORIZED only for that source
- REJECT returns REJECTED and authorizes nothing
- malformed input cannot authorize
- identical payload with same review_ref is idempotent
- same review_ref with different payload is REVIEW_CONFLICT
- no model, confidence, count, time, score, threshold, majority, or last-write-wins authorization
- COG-22 and COG-30 remain unchanged

PROHIBITED:
- modifying COG-22
- modifying COG-30
- creating CANDIDATE_LESSON
- CANDIDATE_LESSON -> VALIDATED_EXPERIENCE
- canonical promotion
- COG-30 policy-state persistence
- durable review-ledger persistence
- COG-21
- model/LLM work
- Pi/production wiring
- Codex

ACCEPTANCE:
- deterministic immutable review contract
- deterministic validator
- source-specific explicit human review
- evidence binding enforced
- replay/idempotency and review_ref conflict behavior qualified
- authority=NONE / []
- no epistemic promotion
- EXP-LIFE-01 regression PASS
- reviewed COG-22 tests PASS
- reviewed COG-30 tests PASS
- independent Reviewer PASS before checkpoint

ROLLBACK:
Remove only EXP-REVIEW-01 additive files and return to the EXP-LIFE-01 checkpoint.

NEXT_IF_QUALIFIED:
Separate reconciliation for the smallest mechanical adapter consuming AUTHORIZED review and using existing COG-22 explicit transition machinery.

CODEX: NOT_USED
PI_CHANGES: NONE
