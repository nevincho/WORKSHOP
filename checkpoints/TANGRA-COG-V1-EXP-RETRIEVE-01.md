# TANGRA-COG-V1-EXP-RETRIEVE-01 — Qualified Checkpoint

DATE: 2026-09-26
STATE: WORKSHOP_QUALIFIED
REVIEW: PASS
CONTROL_AUTHORITY: NONE

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BRANCH: tangra-cog-v1-exp-retrieve-01
VALIDATED_CANDIDATE_HEAD: 102619a31ae9b8f931e91f68ab451fde2ec42c7a
PRE_CHANGE_CHECKPOINT: tangra-cog-v1-exp-validated-01@dd3f74b21cf7c2860bd82674867936dbe73c6a82

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_retrieval_adapter.py
  blob: 0fdb956b95051850d637d9f60c894dff2fd35117
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_retrieval_adapter.py
  blob: c39da9cb28c1eec38e4ffd52191a1410c7b40df2

PROTECTED_BLOBS_UNCHANGED:
- EXP-PERSIST-01 adapter: efcfbf1cefa028efe40735835f25f2c86b8cb812
- EXP-VALIDATED-01 adapter: 06e28d91dfb63661e9f1805783705d80be51c341
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64
- qualification workflow restored to baseline: 9d28f0fd44886b7901f061258b5f028deab4bd8b

QUALIFICATION_HISTORY:
- Run 36270414653: FAIL in EXP-RETRIEVE-01 test fixture only.
  - classification: TEST FIXTURE / VALIDATION METHODOLOGY DEFECT
  - cause: synthetic record IDs replayed CANDIDATE before RAW under reviewed COG-22 from_fixture() deterministic sorted order
  - correction: test fixture IDs only
  - no retrieval implementation defect established
- Run 36270463432: PASS
  - executed head: da026ae80f1191d6d11c12133c000d388e05cc47
  - final implementation/test blobs identical to passing run; later commit only restored qualification workflow

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
- EXP-VALIDATE-REVIEW-01: 13/13 PASS
- EXP-VALIDATED-01: 10/10 PASS
- EXP-RETRIEVE-01: 11/11 PASS
- reviewed COG-22: 36/36 PASS
- reviewed COG-30: 15/15 PASS
- bounded total: 211 PASS / 0 FAIL

QUALIFIED_BEHAVIOR:
- persisted Experience state reloads only through qualified DurableExperienceSnapshotStore;
- retrieval is forced to lifecycle=VALIDATED_EXPERIENCE;
- returned records are genuine reviewed COG-22 ExperienceRecord values;
- existing reviewed COG-22 filters/order/limit/truncation/status semantics are preserved;
- no RAW_EVIDENCE or CANDIDATE_LESSON fallback exists;
- exact record JSON, semantic hash, evidence bindings, provenance, limitations and unknowns survive restart retrieval;
- missing/invalid snapshots return no records;
- MISSION_CONSTRAINED remains unsupported;
- retrieval is read-only and does not change snapshot bytes;
- Canonical Promotion is not required;
- authority=NONE;
- operational_authority=[].

DEFERRED / NOT STARTED:
- COG-30 Canonical Promotion / CANONICAL_SYSTEM_KNOWLEDGE
- post-mission orchestration composition
- FAST/verbal integration
- model work
- COG-21
- Pi/production wiring

REVIEW_EVIDENCE:
- evidence/TANGRA-COG-V1-EXP-RETRIEVE-01/WORKER.md
- review/TANGRA-COG-V1-EXP-RETRIEVE-01.md

ROLLBACK:
- exact rollback target: tangra-cog-v1-exp-validated-01@dd3f74b21cf7c2860bd82674867936dbe73c6a82
- remove/revert only EXP-RETRIEVE-01 additive files.

NEXT_DEPENDENCY:
- Reconcile the smallest post-mission orchestration composition that consumes the qualified read-only VALIDATED_EXPERIENCE retrieval boundary.
- Do not begin FAST/verbal integration or any later dependency during that reconciliation.

CODEX: NOT USED
PI_CHANGES: NONE
HISTORICAL_317_REGRESSION: NOT EXECUTED

FINAL_RESULT:
WORKSHOP_QUALIFIED / REVIEWER_PASS / AUTHORITY_NONE
