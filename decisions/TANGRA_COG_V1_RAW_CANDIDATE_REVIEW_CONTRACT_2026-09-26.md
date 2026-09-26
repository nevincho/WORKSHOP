# TANGRA Cognitive V1 — RAW_EVIDENCE → CANDIDATE_LESSON Human Review Authorization Contract

DATE: 2026-09-26
DECISION_ID: TANGRA-COG-V1-RAW-CANDIDATE-REVIEW-CONTRACT-01
STATUS: ARCHITECTURE_DECIDED / IMPLEMENTATION_NOT_STARTED
PROJECT: TANGRA
SCOPE: Unit 6 Experience lifecycle authorization boundary

## Problem

WORKSHOP_QUALIFIED EXP-LIFE-01 establishes that persisted/restored RAW_EVIDENCE can attach to reviewed COG-30 as ACTIVE/RETAIN, but no reviewed contract authorizes RAW_EVIDENCE → CANDIDATE_LESSON.

Existing reviewed mechanisms are intentionally insufficient:
- COG-22 ExperienceStoreRequest.explicit_transition_from mechanically constrains lifecycle sequencing but does not express human authorization.
- COG-30 DispositionReview is restricted to DEPRECATED/INVALIDATED.
- COG-30 CanonicalPromotionReview is restricted to VALIDATED_EXPERIENCE → CANONICAL_SYSTEM_KNOWLEDGE.
- COG-14 ProposalAssurance may produce ELIGIBLE_FOR_REVIEW but explicitly remains NOT_APPROVED / NOT_EXECUTED.
- WORKSHOP HUMAN_GATE_POLICY controls engineering execution, not Cognitive Experience lifecycle records.

Therefore the missing boundary is an additive explicit human-review authorization contract.

## Architectural location

The contract belongs in the Cognitive V1 Unit-6 integration layer beside the existing Experience integration adapters.

It MUST NOT be added to or alter reviewed COG-22 or reviewed COG-30 implementations.

Planned implementation location:
TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_candidate_review_contract.py

This contract is an authorization record/validator only. It does not itself create CANDIDATE_LESSON and does not expose a generic promotion method.

## Contract

### ReviewDecision

Exact values:
- APPROVE
- REJECT

No UNKNOWN, AUTO, MODEL_APPROVED, ELIGIBLE, confidence-derived, or implicit decision state is permitted.

### RawCandidateReview

Required fields:
- review_ref: unique review identifier.
- source_experience_id: exact COG-22 RAW_EVIDENCE Experience ID under review.
- reviewer_id: explicit human/reviewer identity string.
- decision: ReviewDecision.APPROVE or ReviewDecision.REJECT.
- evidence_refs: non-empty tuple of evidence/result refs used for the decision.
- reason: non-empty human justification.
- authority: exactly NONE.
- operational_authority: exactly empty tuple/list.

No model identity, confidence score, count threshold, age/time threshold, probability or learned score is an authorization field.

### Deterministic validation

Given RawCandidateReview + reviewed COG-22 ExperienceStore + reviewed COG-30 ExperienceLifecyclePolicy:

1. Schema and required fields must validate.
2. source_experience_id must resolve to exactly one existing COG-22 record.
3. Source lifecycle must be exactly RAW_EVIDENCE.
4. COG-30 disposition of source must be ACTIVE.
5. evidence_refs must be non-empty.
6. Every review evidence ref must already be bound to that exact source ExperienceRecord through one of:
   - evidence_refs
   - diagnostic_result_refs
   - correlation_refs
   - hypothesis_refs
   - interpretation_refs
   - signal_refs
   - configuration_profile_refs
7. review_ref must identify one deterministic review decision.
8. reviewer_id must be explicit and non-empty.
9. reason must be explicit and non-empty.
10. authority must equal NONE.
11. operational_authority must be empty.
12. No model/backend output may be treated as reviewer identity or authorization.
13. No confidence/count/time/score rule may synthesize APPROVE.
14. Validation does not change the COG-22 record, COG-30 state, or any operational state.

### Validation result

A bounded validator may return:
- AUTHORIZED — only for a valid explicit APPROVE review.
- REJECTED — for a valid explicit REJECT review.
- INVALID_REVIEW — malformed/invalid review contract.
- SOURCE_NOT_FOUND.
- SOURCE_NOT_RAW.
- SOURCE_NOT_ACTIVE.
- EVIDENCE_NOT_BOUND.
- REVIEW_CONFLICT.

Result fields must include:
- review_ref
- source_experience_id
- decision
- status/code
- authority=NONE
- operational_authority=[]

AUTHORIZED means only:
"the explicitly referenced RAW_EVIDENCE record is authorized to be considered by a later bounded mechanical RAW_EVIDENCE → CANDIDATE_LESSON transition."

AUTHORIZED does NOT mean:
- transition already occurred;
- FACT;
- VERIFIED_CAUSE;
- validated experience;
- canonical knowledge;
- runtime/operational authority;
- command/config/mission/target authority.

## Replay / idempotency

The deterministic review identity is keyed by review_ref.

For a review ledger/set supplied to the validator:
- replay of the identical canonical review payload with the same review_ref is IDEMPOTENT and must return the same semantic outcome;
- same review_ref with different canonical payload is REVIEW_CONFLICT and must authorize nothing;
- multiple distinct APPROVE review_refs for the same source do not multiply authority and still authorize only that exact source;
- APPROVE for source A can never authorize source B;
- REJECT never creates or authorizes a lifecycle transition;
- an APPROVE and REJECT under different review_refs for the same source are not silently resolved by timestamp, confidence, majority, count, or last-write-wins. Such cross-review conflict requires a later explicit reconciliation policy and must not authorize promotion automatically.

The first implementation task is limited to single-review validation plus deterministic same-review_ref replay/conflict behavior. Cross-review conflict resolution remains outside scope.

## Rejection behavior

REJECT is terminal for that review record only:
- no COG-22 append;
- no COG-30 mutation;
- no candidate creation;
- no implicit retry or inversion;
- no automatic override.

A later independent review, if architecture later permits it, is a separate review_ref and does not retroactively alter the rejected review record.

## Authority boundary

AUTHORITY=NONE.
operational_authority=[].

Human review authorizes only a bounded data-lifecycle transition eligibility for one exact Experience ID.
It grants no runtime authority and no epistemic promotion.

No LLM/model can populate or substitute reviewer authorization.
Natural-language reason remains untrusted descriptive data and cannot alter deterministic validation semantics.

## COG-22 impact

NONE.

COG-22 remains unchanged.
Its existing explicit_transition_from mechanism remains the eventual mechanical transition gate.
This architecture contract supplies the missing authorization prerequisite only.

## COG-30 impact

NONE.

COG-30 remains unchanged.
Its existing ACTIVE state is a prerequisite to authorization.
No COG-30 disposition, canonical-promotion, retention, or policy-state persistence semantics are extended.

## Out of scope

- actual RAW_EVIDENCE → CANDIDATE_LESSON record creation;
- CANDIDATE_LESSON → VALIDATED_EXPERIENCE;
- canonical promotion;
- COG-30 policy-state persistence;
- review UI;
- identity authentication infrastructure;
- autonomous thresholds;
- model authorization;
- Pi/production wiring.

## Next implementation gate

TANGRA-COG-V1-EXP-REVIEW-01 must implement and qualify only this additive contract and deterministic validator.

No transition execution is authorized by this architecture decision alone.
