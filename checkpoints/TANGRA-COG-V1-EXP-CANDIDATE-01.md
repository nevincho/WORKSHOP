# TANGRA-COG-V1-EXP-CANDIDATE-01 — Qualified Checkpoint

DATE: 2026-09-26
STATE: WORKSHOP_QUALIFIED
REVIEW: PASS
CONTROL_AUTHORITY: NONE

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BRANCH: tangra-cog-v1-exp-candidate-01
VALIDATED_CANDIDATE_HEAD: 3397777b0a2f246bbbf9b1901cfec5c766e8d6a8
PRE_CHANGE_CHECKPOINT: tangra-cog-v1-exp-review-01@249234f5265a9ae4595fbcfc8b91ef82efc353a8

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_candidate_transition_adapter.py
  blob: 9191e16bb4a12b1dd4640006504e957531ffdc77
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_candidate_transition_adapter.py
  blob: 3828482d77c88ec56e50c32c1bebacb1c3c7d0b7

PROTECTED_BLOBS_UNCHANGED:
- EXP-REVIEW-01 contract: 691378fdbf35181e66da17acde5c710995c6c5ed
- EXP-LIFE-01 adapter: b7573bce130aa9dd2827142d5c63d1190126d28e
- EXP-PERSIST-01 adapter: efcfbf1cefa028efe40735835f25f2c86b8cb812
- EXP-01 adapter: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64
- qualification workflow restored to baseline: 9d28f0fd44886b7901f061258b5f028deab4bd8b

QUALIFICATION_RUN:
- GitHub Actions run 36267598011
- executed head: f460a9e076a443f8bed6debbaad08f1ce7723fc8
- final implementation/test blobs are identical to passing run; later commit only restored qualification workflow.

TESTS:
- Cognitive Bridge: 17/17 PASS
- DIAG-01: 15/15 PASS
- CORR-01: 12/12 PASS
- HYP-01: 13/13 PASS
- INT-01: 13/13 PASS
- EXP-01: 13/13 PASS
- EXP-PERSIST-01: 13/13 PASS
- EXP-LIFE-01: 8/8 PASS
- EXP-REVIEW-01: 12/12 PASS
- EXP-CANDIDATE-01: 10/10 PASS
- reviewed COG-22: 36/36 PASS
- reviewed COG-30: 15/15 PASS
- bounded total: 177 PASS / 0 FAIL

QUALIFIED_BEHAVIOR:
- genuine AUTHORIZED/APPROVE RawCandidateReviewResult can drive one explicit reviewed COG-22 RAW_EVIDENCE -> CANDIDATE_LESSON transition;
- source must still exist as RAW_EVIDENCE and remain ACTIVE under reviewed COG-30;
- candidate ID is deterministic from source ID + review_ref;
- candidate preserves source semantic fields unchanged except new experience_id, lifecycle=CANDIDATE_LESSON, supersedes_experience_id=source ID;
- RAW source remains immutable;
- identical replay is deterministic/idempotent;
- reviewed COG-22 rejection/unsupported mode is not bypassed;
- COG-30 policy state remains unchanged;
- no epistemic promotion occurs;
- authority=NONE;
- operational_authority=[].

EXPLICIT_NON_CAPABILITIES:
- CANDIDATE_LESSON -> VALIDATED_EXPERIENCE: NOT STARTED.
- candidate validation/evidence sufficiency contract: NOT DEFINED.
- human reviewer identity authentication: NOT VERIFIED.
- durable review-ledger persistence: NOT IMPLEMENTED.
- COG-30 policy-state persistence: NOT STARTED.
- COG-21: NOT STARTED.
- model/LLM authorization: NOT PRESENT.
- Pi/production wiring: NOT STARTED.

REVIEW_EVIDENCE:
- evidence/TANGRA-COG-V1-EXP-CANDIDATE-01/WORKER.md
- review/TANGRA-COG-V1-EXP-CANDIDATE-01.md

ROLLBACK:
- exact rollback target: tangra-cog-v1-exp-review-01@249234f5265a9ae4595fbcfc8b91ef82efc353a8
- remove/revert only EXP-CANDIDATE-01 additive files.

NEXT_DEPENDENCY:
- Reconcile the explicit bounded authorization/evidence contract required for CANDIDATE_LESSON -> VALIDATED_EXPERIENCE.
- Do not implement that transition until its human/reviewer validation semantics are justified from repository architecture.

CODEX: NOT USED
PI_CHANGES: NONE

FINAL_RESULT:
WORKSHOP_QUALIFIED / REVIEWER_PASS / AUTHORITY_NONE
