# TANGRA-COG-V1-EXP-PERSIST-01 — Qualified Checkpoint

DATE: 2026-09-26
STATE: WORKSHOP_QUALIFIED
REVIEW: PASS
CONTROL_AUTHORITY: NONE

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BRANCH: tangra-cog-v1-exp-persist-01
VALIDATED_CANDIDATE_HEAD: 437211b0bfd69a387ed6c6d852168c4a9482c6ba
PRE_CHANGE_CHECKPOINT: tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f

UPSTREAM_DEPENDENCIES:
- TANGRA-COG-V1-EXP-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_persistence_adapter.py
  blob: efcfbf1cefa028efe40735835f25f2c86b8cb812
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_persistence_adapter.py
  blob: 41124f5be9cc5a45b4bb36bcc7eba428b942d807

PROTECTED_BLOBS_UNCHANGED:
- EXP-01 adapter: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- COG-30 lifecycle artifact: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64
- qualification workflow restored to baseline: 9d28f0fd44886b7901f061258b5f028deab4bd8b

QUALIFICATION_RUN:
- GitHub Actions run 36265034508
- executed head: 57712dbbac4f7d91d5e2610a3e58b6f8a6c1addb
- final implementation/test blobs are identical to the passing run; later commit only restored the qualification workflow.

TESTS:
- Cognitive Bridge: 17/17 PASS
- DIAG-01 adapter: 15/15 PASS
- CORR-01 integration: 12/12 PASS
- HYP-01 integration: 13/13 PASS
- INT-01 integration: 13/13 PASS
- EXP-01 integration: 13/13 PASS
- EXP-PERSIST-01 integration: 13/13 PASS
- current reviewed COG-22 source tests: 36/36 PASS
- bounded total: 132 PASS / 0 FAIL

QUALIFIED_BEHAVIOR:
- EXP-01 RAW_EVIDENCE COG-22 store persists as exact reviewed fixture representation;
- save uses bounded same-directory temporary file, fsync, atomic os.replace and directory fsync;
- failed replacement preserves prior valid snapshot;
- fresh reload reconstructs a new reviewed ExperienceStore through from_fixture();
- Experience IDs, lifecycle, bindings, provenance, JSON and semantic hashes survive reload exactly;
- reviewed COG-22 get/query and duplicate semantics survive restart;
- missing/malformed/noncanonical/oversized snapshot cannot become valid Experience;
- authority=NONE;
- operational_authority=[].

LIFECYCLE_BOUNDARY:
- COG-30 lifecycle semantics: NOT INTEGRATED.
- COG-30 lifecycle-policy state persistence: NOT STARTED.
- COG-22 lifecycle/store semantics: UNCHANGED.
- EXP-PERSIST-01 qualifies storage mechanics only.

REVIEW_EVIDENCE:
- evidence/TANGRA-COG-V1-EXP-PERSIST-01/WORKER.md
- review/TANGRA-COG-V1-EXP-PERSIST-01.md

ROLLBACK:
- exact rollback target: tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f
- remove/revert the two EXP-PERSIST-01 files.

LIMITATIONS:
- Historical Cognitive Bridge cumulative 317-test regression remains NOT EXECUTED.
- Durability qualification is repository/Linux-CI level only; Pi/production storage behavior is not established.
- COG-30 lifecycle integration was not started.
- COG-21 was not started.

CODEX: NOT USED
PI_CHANGES: NONE

FINAL_RESULT:
WORKSHOP_QUALIFIED / REVIEWER_PASS / AUTHORITY_NONE
