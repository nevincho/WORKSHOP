# TANGRA-COG-V1-EXP-CANDIDATE-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-review-01@249234f5265a9ae4595fbcfc8b91ef82efc353a8
CANDIDATE: tangra-cog-v1-exp-candidate-01@3397777b0a2f246bbbf9b1901cfec5c766e8d6a8

## Final repository delta

Exactly two files differ from the qualified EXP-REVIEW-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_candidate_transition_adapter.py
  - blob 9191e16bb4a12b1dd4640006504e957531ffdc77
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_candidate_transition_adapter.py
  - blob 3828482d77c88ec56e50c32c1bebacb1c3c7d0b7

Temporary qualification workflow restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected blobs unchanged:
- EXP-REVIEW-01 contract: 691378fdbf35181e66da17acde5c710995c6c5ed
- EXP-LIFE-01 adapter: b7573bce130aa9dd2827142d5c63d1190126d28e
- EXP-PERSIST-01 adapter: efcfbf1cefa028efe40735835f25f2c86b8cb812
- EXP-01 adapter: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a bounded mechanical RAW_EVIDENCE -> CANDIDATE_LESSON adapter:
- requires genuine RawCandidateReviewResult;
- requires status AUTHORIZED, decision APPROVE, authorized=True;
- source must still exist as RAW_EVIDENCE;
- reviewed COG-30 source disposition must still be ACTIVE;
- candidate ID is deterministic from exact source_experience_id + review_ref;
- creates new immutable candidate via dataclasses.replace();
- changes only experience_id, lifecycle=CANDIDATE_LESSON, supersedes_experience_id=source ID;
- all source evidence bindings, context, state tuple, outcome, metrics, limitations, unknowns, provenance and created_at are preserved;
- delegates append to existing COG-22 ExperienceStoreRequest with explicit_transition_from=RAW_EVIDENCE;
- identical replay returns IDEMPOTENT rather than creating another candidate;
- semantic duplicate returned by reviewed COG-22 is bounded as IDEMPOTENT;
- source COG-22 record remains unchanged;
- COG-30 policy state remains unchanged.

No CANDIDATE_LESSON -> VALIDATED_EXPERIENCE surface is implemented.

## Executed qualification

GitHub Actions run: 36267598011
Executed head: f460a9e076a443f8bed6debbaad08f1ce7723fc8

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
- reviewed COG-22: 36/36
- reviewed COG-30: 15/15

Bounded total: 177 PASS / 0 FAIL.

Final implementation/test blobs are identical to the passing run. Later candidate commit only restored the qualification workflow.

## Qualified behavior

- one valid authorized review creates one CANDIDATE_LESSON through reviewed COG-22 explicit transition;
- RAW source remains immutable RAW_EVIDENCE;
- candidate supersedes exact RAW source;
- candidate preserves source semantics except required transition identity/lifecycle/link fields;
- identical replay is deterministic/idempotent;
- non-authorized review creates nothing;
- missing or non-active source creates nothing;
- MISSION_CONSTRAINED remains rejected by reviewed COG-22;
- no epistemic promotion or COG-30 mutation occurs;
- authority=NONE / operational_authority=[].

## Limitations

- CANDIDATE_LESSON -> VALIDATED_EXPERIENCE: NOT STARTED.
- candidate validation criteria/policy: NOT DEFINED in this task.
- human identity authentication remains NOT VERIFIED from prior contract scope.
- durable review ledger remains NOT IMPLEMENTED.
- COG-30 policy-state persistence remains NOT STARTED.
- historical cumulative 317-test regression remains NOT EXECUTED.
- no Pi/production wiring.

CODEX: NOT USED
PI_CHANGES: NONE
