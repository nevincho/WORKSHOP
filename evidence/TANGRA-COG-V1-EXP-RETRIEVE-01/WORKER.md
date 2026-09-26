# TANGRA-COG-V1-EXP-RETRIEVE-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-validated-01@dd3f74b21cf7c2860bd82674867936dbe73c6a82
CANDIDATE: tangra-cog-v1-exp-retrieve-01@102619a31ae9b8f931e91f68ab451fde2ec42c7a

## Final repository delta

Exactly two files differ from the qualified EXP-VALIDATED-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_retrieval_adapter.py
  - blob 0fdb956b95051850d637d9f60c894dff2fd35117
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_retrieval_adapter.py
  - blob c39da9cb28c1eec38e4ffd52191a1410c7b40df2

Temporary qualification workflow restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected blobs unchanged:
- EXP-PERSIST-01 adapter: efcfbf1cefa028efe40735835f25f2c86b8cb812
- EXP-VALIDATED-01 adapter: 06e28d91dfb63661e9f1805783705d80be51c341
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a restart-safe read-only retrieval boundary:
- loads persisted Experience state only through qualified DurableExperienceSnapshotStore.load();
- requires successful LOADED result;
- builds reviewed COG-22 ExperienceQuery with lifecycle forced to VALIDATED_EXPERIENCE;
- delegates all filtering/order/limit/status semantics to reviewed ExperienceStore.query();
- may expose existing reviewed filters: event_type, subsystem_domain, outcome, evidence_ref, timestamps, configuration_profile_ref, limit;
- returns genuine reviewed COG-22 ExperienceRecord objects unchanged;
- never falls back to RAW_EVIDENCE or CANDIDATE_LESSON;
- missing/invalid/failed snapshot returns no records;
- MISSION_CONSTRAINED remains unsupported through reviewed COG-22;
- adapter exposes no append/save/transition/promotion/orchestration/voice/model/command surface;
- authority=NONE / operational_authority=[].

Canonical Promotion is not imported, invoked or required.

## Qualification history

### Run 36270414653 — FAIL

Upstream suites through EXP-VALIDATED-01 passed.
EXP-RETRIEVE-01 failed 8 tests because the synthetic test fixture used lexicographically ordered IDs that caused reviewed COG-22 from_fixture() replay to encounter CANDIDATE before RAW.

Classification:
QUALIFICATION TEST FIXTURE / METHODOLOGY DEFECT.

No defect was established in the retrieval adapter.
The fix changed only test fixture IDs so predecessor lifecycle records replay in valid deterministic order.

### Run 36270463432 — PASS

Executed head: da026ae80f1191d6d11c12133c000d388e05cc47

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
- EXP-RETRIEVE-01: 11/11
- reviewed COG-22: 36/36
- reviewed COG-30: 15/15

Bounded total: 211 PASS / 0 FAIL.

Final implementation/test blobs are identical to the passing run. Later candidate commit only restored qualification workflow.

## Qualified behavior

- persisted VALIDATED_EXPERIENCE is reloadable through the qualified restart-safe snapshot boundary;
- retrieval returns VALIDATED_EXPERIENCE only;
- RAW/CANDIDATE records are never substituted when validated records are absent;
- retrieved records retain exact JSON, semantic hash, bindings, provenance, limitations, unknowns and zero-authority boundary;
- existing reviewed COG-22 filtering/order/limit/truncation semantics are preserved;
- retrieval does not modify snapshot bytes;
- no canonical knowledge is required.

## Scope / limitations

- Canonical Promotion: DEFERRED / NOT STARTED.
- post-mission orchestration wiring: NOT STARTED.
- FAST/verbal integration: NOT STARTED.
- model work: NOT STARTED.
- COG-21: NOT STARTED.
- Pi/production wiring: NOT STARTED.
- historical cumulative 317-test regression: NOT EXECUTED.

CODEX: NOT USED
PI_CHANGES: NONE
