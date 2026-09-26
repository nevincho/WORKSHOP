# TANGRA-COG-V1-EXP-LIFE-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-persist-01@437211b0bfd69a387ed6c6d852168c4a9482c6ba
CANDIDATE: tangra-cog-v1-exp-life-01@b6db74d02365ccf2aad5e1a6e755525233c51584

## Upstream qualified dependencies

- TANGRA-COG-V1-EXP-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-EXP-PERSIST-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS
- TAI-COG-30 Experience Lifecycle Artifact: REVIEWER PASS

## Final repository delta

Exactly two files differ from the qualified EXP-PERSIST-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_lifecycle_adapter.py
  - blob b7573bce130aa9dd2827142d5c63d1190126d28e
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_lifecycle_adapter.py
  - blob 586a9084b96f583dbedfe21b203ad5ff8b56bef5

Temporary qualification workflow changes were restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected component blobs unchanged from base:
- EXP-01 adapter: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- EXP-PERSIST-01 adapter: efcfbf1cefa028efe40735835f25f2c86b8cb812
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a read-only baseline lifecycle integration adapter:
- requires an existing reviewed COG-22 ExperienceStore;
- instantiates the existing reviewed COG-30 ExperienceLifecyclePolicy unchanged;
- reads policy.state(experience_id);
- reads policy.retention_action(experience_id);
- optionally delegates exact semantic duplicate lookup to policy.duplicate_of();
- verifies that COG-22 record JSON and semantic hash are unchanged by inspection;
- returns only lifecycle disposition, retention action, duplicate reference, authority NONE.

It introduces no:
- RAW_EVIDENCE -> CANDIDATE_LESSON transition;
- CANDIDATE_LESSON -> VALIDATED_EXPERIENCE transition;
- canonical promotion;
- disposition review;
- policy-state persistence/import;
- model/command/runtime authority.

## Executed qualification

GitHub Actions run: 36265571072
Executed head: 6b50797c2b78cc53ebe97c3336a1af6980218733

PASS:
- Cognitive Bridge: 17/17
- DIAG-01 adapter: 15/15
- CORR-01 integration: 12/12
- HYP-01 integration: 13/13
- INT-01 integration: 13/13
- EXP-01 integration: 13/13
- EXP-PERSIST-01 integration: 13/13
- EXP-LIFE-01 integration: 8/8
- current reviewed COG-22 source tests: 36/36
- reviewed COG-30 lifecycle tests: 15/15

Bounded total: 155 PASS / 0 FAIL.

The final implementation/test blobs are identical to those exercised at the passing run. The later candidate commit only restored the qualification workflow byte-for-byte.

## Qualified behavior

For a persisted and freshly restored EXP-01 RAW_EVIDENCE record:
- reviewed COG-30 policy attaches successfully;
- default LifecycleDisposition is ACTIVE;
- retention action is RETAIN;
- exact semantic duplicate lookup operates on restored COG-22 records;
- COG-22 record identity/JSON/semantic hash/lifecycle remain unchanged;
- policy export remains default empty state after read-only baseline inspection;
- no lifecycle transition or human/review object is created.

## Scope

COG-22: NOT MODIFIED.
COG-30: NOT MODIFIED.
RAW->CANDIDATE policy: NOT DEFINED / NOT IMPLEMENTED.
CANDIDATE->VALIDATED policy: NOT DEFINED / NOT IMPLEMENTED.
COG-30 policy-state persistence: NOT STARTED.
COG-21: NOT STARTED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Model work: NOT STARTED.
Historical Cognitive Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback target:
tangra-cog-v1-exp-persist-01@437211b0bfd69a387ed6c6d852168c4a9482c6ba

Removing/reverting the two EXP-LIFE-01 files restores the qualified EXP-PERSIST-01 state.
