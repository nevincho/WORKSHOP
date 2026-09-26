# TANGRA-COG-V1-EXP-VALIDATE-REVIEW-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-candidate-01@3397777b0a2f246bbbf9b1901cfec5c766e8d6a8
CANDIDATE: tangra-cog-v1-exp-validate-review-01@3b9d81aad454189770079b73b0757eb2e076646a

ARCHITECTURE_DECISION:
WORKSHOP/decisions/TANGRA_COG_V1_CANDIDATE_VALIDATED_REVIEW_CONTRACT_2026-09-26.md

## Reconciliation result

No existing reviewed TANGRA contract authorizes CANDIDATE_LESSON -> VALIDATED_EXPERIENCE.
The qualified RAW -> CANDIDATE approval cannot serve as the second approval.
A distinct additive Stage-2 human-review authorization contract was therefore required.

## Final repository delta

Exactly two files differ from the qualified EXP-CANDIDATE-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_validation_review_contract.py
  - blob 88dacc2dbf7d43a18edd05ccb26941ed2cf3aa76
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_validation_review_contract.py
  - blob 3e9f0a617a1fde46c80ee9d05476a28672b0e37c

Temporary qualification workflow restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected blobs unchanged:
- EXP-CANDIDATE-01 adapter: 9191e16bb4a12b1dd4640006504e957531ffdc77
- EXP-REVIEW-01 contract: 691378fdbf35181e66da17acde5c710995c6c5ed
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added second-stage immutable CandidateValidationReview contract:
- review_ref
- source_candidate_experience_id
- reviewer_id
- explicit APPROVE / REJECT
- non-empty evidence_refs
- reason
- prior_raw_candidate_review_ref
- authority=NONE
- operational_authority=[]

Validator requires:
- genuine prior RawCandidateReviewResult;
- prior result AUTHORIZED + APPROVE;
- Stage-2 prior review ref exactly matches Stage-1 review ref;
- Stage-2 review_ref differs from Stage-1 review_ref;
- exact Candidate exists and lifecycle=CANDIDATE_LESSON;
- candidate deterministic ID matches the qualified Stage-1 source ID + Stage-1 review_ref rule;
- candidate.supersedes_experience_id matches Stage-1 RAW source;
- reviewed COG-30 disposition remains ACTIVE;
- every Stage-2 evidence ref is already bound to that exact Candidate;
- explicit human reviewer identity; model/backend reviewer identities rejected.

Replay:
- identical Stage-2 review_ref + canonical payload is idempotent;
- changed payload under same Stage-2 review_ref yields REVIEW_CONFLICT.

No VALIDATED_EXPERIENCE record is created.
No COG-22 or COG-30 mutation occurs.

## Executed qualification

GitHub Actions run: 36268274403
Executed head: 7fd926dda28f37063fa9618ce202a533e29fd3ff

PASS:
- Cognitive Bridge: 17/17
- DIAG-01: 15/15
- CORR-01: 12/12
- HYP-01: 13/13
- INT-01: 13/13
- EXP-01: 13/13
- EXP-PERSIST-01: 13/13
- EXP-LIFE-01: 8/8
- EXP-REVIEW-01: 12/12
- EXP-CANDIDATE-01: 10/10
- EXP-VALIDATE-REVIEW-01: 13/13
- reviewed COG-22: 36/36
- reviewed COG-30: 15/15

Bounded total: 190 PASS / 0 FAIL.

Final implementation/test blobs are identical to passing run. Later commit only restored qualification workflow.

## Qualified behavior

- second operator approval is distinct from Stage-1 approval;
- Stage-1 approval cannot substitute for Stage-2;
- Stage-2 approval applies only to exact qualified Candidate chain;
- candidate must remain ACTIVE;
- evidence must be candidate-bound;
- Stage-2 REJECT authorizes nothing;
- no model/threshold/count/time/score authorization;
- no CANDIDATE -> VALIDATED transition occurs;
- authority=NONE / operational_authority=[].

## Limitations

- CANDIDATE_LESSON -> VALIDATED_EXPERIENCE mechanical transition: NOT IMPLEMENTED / NOT EXECUTED.
- human reviewer identity authentication: NOT VERIFIED.
- durable review ledger: NOT IMPLEMENTED.
- cross-review conflict resolution for distinct Stage-2 review_ref values: NOT IMPLEMENTED.
- COG-30 policy-state persistence: NOT STARTED.
- canonical promotion: NOT STARTED in this chain.
- historical cumulative 317-test regression: NOT EXECUTED.
- Pi/production wiring: NOT STARTED.

CODEX: NOT USED
PI_CHANGES: NONE
