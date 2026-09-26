# TANGRA-COG-V1-EXP-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e
CANDIDATE: tangra-cog-v1-exp-01@32ba33805b09c459a41a53d48c938aac4ca95b3f

## Upstream qualified dependencies

- TANGRA-COG-V1-DIAG-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-CORR-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-HYP-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-INT-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS

## Final repository delta

Exactly two files differ from the qualified INT-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_adapter.py
  - blob f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_adapter.py
  - blob 36ffa2bd5cb058779d9ad6f346284457fbf2a594

Temporary qualification workflow changes were restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected component blobs unchanged from base:
- INT-01 adapter: c486d89f17621d9c5ee0ceb0fe1fd517d7db9d59
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- COG-21 signal layer: 38042ac97bddf662f9b7dc7d200d18369c210f9b
- COG-30 lifecycle artifact: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a thin RAW Experience composition/store adapter:
- requires a genuine validated COG-02 EvidencePacket;
- requires qualified COG-16 DiagnosticExecutionResult values carrying DiagnosticResult;
- validates/reuses qualified COG-18 correlation records;
- validates/reuses qualified COG-19 hypotheses;
- requires a COMPLETED reviewed COG-20 interpretation result;
- creates only ExperienceLifecycle.RAW_EVIDENCE;
- binds authentic evidence refs, diagnostic execution IDs, correlation IDs, hypothesis IDs and interpretation result ID;
- signal_refs is always empty;
- state_before/change/state_after default to None;
- outcome is UNKNOWN;
- metrics are empty;
- context refs are explicit caller input only;
- submits through the existing reviewed COG-22 ExperienceStore.append;
- adds no persistence, lifecycle promotion, model, filesystem, network or COG-21/30 behavior.

## Executed qualification

GitHub Actions run: 36262981535
Executed head: edaca58df816b2fcef7d0bdb9df6a404b4a77764

PASS:
- Cognitive Bridge: 17/17
- DIAG-01 adapter: 15/15
- CORR-01 integration: 12/12
- HYP-01 integration: 13/13
- INT-01 integration: 13/13
- EXP-01 integration: 13/13
- current reviewed COG-22 source tests: 36/36

Bounded total: 119 PASS / 0 FAIL.

The final implementation/test blobs are identical to those exercised at the passing run. The later candidate commit only restored the pre-existing workflow byte-for-byte.

## Qualified behavior

- authentic COG-02 evidence reaches COG-22 binding;
- DIAG/CORR/HYP/INT refs remain traceable;
- COG-21 signals are not required;
- only RAW_EVIDENCE is created;
- no automatic lifecycle transition occurs;
- no state transition/outcome/metrics are invented;
- deterministic record serialization/semantic hash/experience ID for identical inputs;
- reviewed COG-22 duplicate handling remains authoritative;
- MISSION_CONSTRAINED remains unsupported by reviewed COG-22;
- AUTHORITY=NONE;
- operational_authority=[].

## Scope

COG-22 implementation: NOT MODIFIED.
COG-21: NOT STARTED / NOT MODIFIED.
COG-30: NOT STARTED / NOT MODIFIED.
Durable persistence: NOT STARTED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Historical Cognitive Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback target:
tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e

Removing/reverting the two EXP-01 files restores the qualified INT-01 state.
