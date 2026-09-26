# TANGRA-COG-V1-EXP-VALIDATED-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-validate-review-01@3b9d81aad454189770079b73b0757eb2e076646a
CANDIDATE: tangra-cog-v1-exp-validated-01@dd3f74b21cf7c2860bd82674867936dbe73c6a82

## Final repository delta

Exactly two files differ from the qualified EXP-VALIDATE-REVIEW-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_validated_transition_adapter.py
  - blob 06e28d91dfb63661e9f1805783705d80be51c341
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_validated_transition_adapter.py
  - blob 98673afd63fb352abddbd4b6e65ff26a775cd183

Temporary qualification workflow restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected blobs unchanged:
- EXP-VALIDATE-REVIEW-01 contract: 88dacc2dbf7d43a18edd05ccb26941ed2cf3aa76
- EXP-CANDIDATE-01 adapter: 9191e16bb4a12b1dd4640006504e957531ffdc77
- EXP-REVIEW-01 contract: 691378fdbf35181e66da17acde5c710995c6c5ed
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a bounded mechanical CANDIDATE_LESSON -> VALIDATED_EXPERIENCE adapter:
- requires genuine CandidateValidationReviewResult;
- requires status AUTHORIZED, decision APPROVE, authorized=True;
- source candidate must still exist;
- source lifecycle must remain CANDIDATE_LESSON;
- reviewed COG-30 disposition must remain ACTIVE;
- validated ID is deterministic from exact candidate ID + Stage-2 review_ref;
- creates a new immutable record via dataclasses.replace();
- changes only experience_id, lifecycle=VALIDATED_EXPERIENCE, supersedes_experience_id=candidate ID;
- preserves all other candidate semantics unchanged;
- delegates append to existing reviewed COG-22 with explicit_transition_from=CANDIDATE_LESSON;
- identical replay returns IDEMPOTENT;
- source candidate remains immutable;
- COG-30 policy state remains unchanged;
- no CANONICAL_SYSTEM_KNOWLEDGE is created;
- no canonical-promotion API is invoked.

## Executed qualification

GitHub Actions run: 36269361890
Executed head: e2b3b92e4132e16ab40d7bc8e81cd14201f09ac1

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
- EXP-VALIDATED-01: 10/10
- reviewed COG-22: 36/36
- reviewed COG-30: 15/15

Bounded total: 200 PASS / 0 FAIL.

Final implementation/test blobs are identical to the passing run. Later candidate commit only restored qualification workflow.

## Qualified behavior

- a genuine Stage-2 AUTHORIZED/APPROVE result can drive one reviewed COG-22 CANDIDATE_LESSON -> VALIDATED_EXPERIENCE transition;
- candidate must still be CANDIDATE_LESSON and ACTIVE;
- validated record deterministically supersedes the exact Candidate;
- semantic fields are preserved except required transition identity/lifecycle/link fields;
- candidate remains immutable;
- identical replay is deterministic/idempotent;
- reviewed COG-22 unsupported/rejection behavior is not bypassed;
- COG-30 state remains unchanged;
- no canonical record is created;
- authority=NONE / operational_authority=[].

## Limitations

- canonical promotion: NOT STARTED / NOT EXECUTED.
- CANONICAL_SYSTEM_KNOWLEDGE creation: NOT STARTED.
- human identity authentication: NOT VERIFIED.
- durable review ledger: NOT IMPLEMENTED.
- COG-30 policy-state persistence: NOT STARTED.
- historical cumulative 317-test regression: NOT EXECUTED.
- Pi/production wiring: NOT STARTED.

CODEX: NOT USED
PI_CHANGES: NONE
