# TANGRA Cognitive V1 — CANDIDATE_LESSON → VALIDATED_EXPERIENCE Second-Stage Human Review Contract

DATE: 2026-09-26
DECISION_ID: TANGRA-COG-V1-CANDIDATE-VALIDATED-REVIEW-CONTRACT-01
STATUS: ARCHITECTURE_DECIDED / IMPLEMENTATION_NOT_STARTED
PROJECT: TANGRA
SCOPE: Unit 6 Experience lifecycle second operator-approval boundary

## Decision

No existing reviewed TANGRA contract authorizes CANDIDATE_LESSON → VALIDATED_EXPERIENCE.

The qualified RAW_EVIDENCE → CANDIDATE_LESSON authorization is the first operator gate and MUST NOT be reused as the second approval.

Introduce one additive second-stage human-review authorization contract in the Unit-6 integration layer. COG-22 and COG-30 remain unchanged.

Planned implementation:
TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_validation_review_contract.py

This contract authorizes only eligibility for a later bounded mechanical CANDIDATE_LESSON → VALIDATED_EXPERIENCE transition. It does not execute that transition.

## Two-stage invariant

Stage 1:
RAW_EVIDENCE
→ explicit human APPROVE under qualified RawCandidateReview
→ CANDIDATE_LESSON

Stage 2:
CANDIDATE_LESSON
→ separate explicit human APPROVE under CandidateValidationReview
→ eligible for later VALIDATED_EXPERIENCE transition

The Stage-2 review_ref MUST differ from the Stage-1 review_ref.
A Stage-1 AUTHORIZED result can never substitute for Stage-2 authorization.

## CandidateValidationReview

Required fields:
- review_ref
- source_candidate_experience_id
- reviewer_id
- decision: APPROVE | REJECT
- evidence_refs: non-empty
- reason: non-empty
- prior_raw_candidate_review_ref
- authority=NONE
- operational_authority=[]

No model, score, confidence, count, duration, age, threshold or automatic decision field exists.

## Deterministic validation

Inputs:
- CandidateValidationReview
- genuine prior qualified RawCandidateReviewResult
- reviewed COG-22 ExperienceStore
- reviewed COG-30 ExperienceLifecyclePolicy

Validation requires:
1. CandidateValidationReview schema valid.
2. prior RawCandidateReviewResult is genuine, AUTHORIZED and APPROVE.
3. Stage-2 prior_raw_candidate_review_ref exactly equals prior result.review_ref.
4. Stage-2 review_ref differs from Stage-1 review_ref.
5. Candidate exists.
6. Candidate lifecycle is exactly CANDIDATE_LESSON.
7. Candidate.supersedes_experience_id equals prior result.source_experience_id.
8. Candidate ID equals the qualified deterministic Stage-1 candidate-ID rule for prior source ID + Stage-1 review_ref.
9. Candidate COG-30 disposition is ACTIVE.
10. Every Stage-2 evidence_ref is already bound to the exact Candidate ExperienceRecord.
11. reviewer_id is explicit human/reviewer identity and model/backend identities are forbidden.
12. reason is explicit/non-empty.
13. authority=NONE and operational_authority empty.
14. Validation does not mutate COG-22 or COG-30.
15. No claim class/outcome/evidence content is promoted or changed.

## Result

Statuses:
- AUTHORIZED
- REJECTED
- INVALID_REVIEW
- PRIOR_AUTHORIZATION_INVALID
- REVIEW_STAGE_CONFLICT
- SOURCE_NOT_FOUND
- SOURCE_NOT_CANDIDATE
- SOURCE_CHAIN_MISMATCH
- SOURCE_NOT_ACTIVE
- EVIDENCE_NOT_BOUND
- REVIEW_CONFLICT

AUTHORIZED means only:
the exact Candidate Experience is eligible for consideration by a later mechanical CANDIDATE_LESSON → VALIDATED_EXPERIENCE transition.

It does NOT mean:
- transition occurred
- FACT
- VERIFIED_CAUSE
- canonical knowledge
- runtime or operational authority

## Replay / idempotency

- identical Stage-2 canonical payload under same review_ref => identical semantic result
- same Stage-2 review_ref with changed payload => REVIEW_CONFLICT
- Stage-1 review_ref reused as Stage-2 review_ref => REVIEW_STAGE_CONFLICT
- approval applies only to exact source_candidate_experience_id
- REJECT authorizes nothing
- no majority, last-write-wins, timestamp, score or threshold conflict resolution

## Rejection behavior

REJECT:
- creates no VALIDATED_EXPERIENCE
- does not mutate candidate
- does not mutate COG-30
- does not invalidate the Stage-1 review
- does not automatically retry

## Authority

AUTHORITY=NONE
operational_authority=[]

The second human gate is data-lifecycle authorization only.

## COG-22 impact

NONE.

Existing explicit transition mechanism will be used only by a later separate mechanical transition task.

## COG-30 impact

NONE.

Existing ACTIVE disposition is a prerequisite only.

## Out of scope

- actual CANDIDATE_LESSON → VALIDATED_EXPERIENCE transition
- canonical promotion
- model/LLM review
- deterministic/automatic validation thresholds
- identity-authentication infrastructure
- durable review-ledger persistence
- COG-30 policy-state persistence
- Pi/production wiring
- COG-21

## Next implementation gate

TANGRA-COG-V1-EXP-VALIDATE-REVIEW-01 implements/qualifies only this second-stage authorization contract.
