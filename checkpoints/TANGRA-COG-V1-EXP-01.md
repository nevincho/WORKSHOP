# TANGRA-COG-V1-EXP-01 — Qualified Checkpoint

DATE: 2026-09-26
STATE: WORKSHOP_QUALIFIED
REVIEW: PASS
CONTROL_AUTHORITY: NONE

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BRANCH: tangra-cog-v1-exp-01
VALIDATED_CANDIDATE_HEAD: 32ba33805b09c459a41a53d48c938aac4ca95b3f
PRE_CHANGE_CHECKPOINT: tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e

UPSTREAM_DEPENDENCIES:
- TANGRA-COG-V1-DIAG-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-CORR-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-HYP-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-INT-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_adapter.py
  blob: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_adapter.py
  blob: 36ffa2bd5cb058779d9ad6f346284457fbf2a594

PROTECTED_BLOBS_UNCHANGED:
- INT-01 adapter: c486d89f17621d9c5ee0ceb0fe1fd517d7db9d59
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- COG-21 signal layer: 38042ac97bddf662f9b7dc7d200d18369c210f9b
- COG-30 lifecycle artifact: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64
- qualification workflow restored to baseline: 9d28f0fd44886b7901f061258b5f028deab4bd8b

QUALIFICATION_RUN:
- GitHub Actions run 36262981535
- executed head: edaca58df816b2fcef7d0bdb9df6a404b4a77764
- final implementation/test blobs are identical to the passing run; later commit only restored the qualification workflow.

TESTS:
- Cognitive Bridge: 17/17 PASS
- DIAG-01 adapter: 15/15 PASS
- CORR-01 integration: 12/12 PASS
- HYP-01 integration: 13/13 PASS
- INT-01 integration: 13/13 PASS
- EXP-01 integration: 13/13 PASS
- current reviewed COG-22 source tests: 36/36 PASS
- bounded total: 119 PASS / 0 FAIL

QUALIFIED_BEHAVIOR:
- qualified chain through INT-01 creates one reviewed COG-22 RAW_EVIDENCE ExperienceRecord;
- authentic evidence/result/correlation/hypothesis/interpretation refs remain traceable;
- signal_refs remains empty;
- COG-21 is not required;
- no state transition/outcome/metrics are invented;
- reviewed COG-22 in-memory store handles storage/dedup;
- MISSION_CONSTRAINED remains unsupported;
- authority=NONE;
- operational_authority=[].

REVIEW_EVIDENCE:
- evidence/TANGRA-COG-V1-EXP-01/WORKER.md
- review/TANGRA-COG-V1-EXP-01.md

ROLLBACK:
- exact rollback target: tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e
- remove/revert the two EXP-01 files.

LIMITATIONS:
- Historical Cognitive Bridge cumulative 317-test regression remains NOT EXECUTED.
- COG-30 lifecycle integration was not started.
- Durable persistence was not started.
- COG-21 was not started.
- No Pi/production integration or runtime promotion is established.

CODEX: NOT USED
PI_CHANGES: NONE

FINAL_RESULT:
WORKSHOP_QUALIFIED / REVIEWER_PASS / AUTHORITY_NONE
