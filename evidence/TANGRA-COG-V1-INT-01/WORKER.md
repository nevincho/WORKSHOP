# TANGRA-COG-V1-INT-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-hyp-01@6247f1b6e42131319dd5e3d3094d12b99974c97e
CANDIDATE: tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e

## Upstream qualified dependencies

- TANGRA-COG-V1-DIAG-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-CORR-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-HYP-01: WORKSHOP_QUALIFIED
- TAI-COG-20: REVIEWER PASS

## Final repository delta

Exactly two files differ from the qualified HYP-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_diagnostic_interpretation_adapter.py
  - blob c486d89f17621d9c5ee0ceb0fe1fd517d7db9d59
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_diagnostic_interpretation_adapter.py
  - blob 86977a60fa6cfc6b1eb787eae8cdd94a2f5c1ee3

Temporary qualification workflow changes were restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected component blobs unchanged from base:
- HYP-01 adapter: 8a6014c65769a02534383d78ea70192cffbfe55c
- CORR-01 adapter: 1a99368b19cd57859378c40d1547fd5d000dc1f4
- DIAG-01 adapter: a72b88a884499931b0630d7a24618dfe7122b2f2
- reviewed COG-20 interpreter: db0b95599dcec92467b0e75f5077264a9ed46820
- COG-02 EvidencePacket builder: e9c4ec380794d2e834e18f06ca1364d810d0f5d4
- COG-06 backend contract: 1be7d65daaa4a7a415da4dd30b135b54e1c64908
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a thin COG-20 composition adapter:
- requires a pre-existing validated COG-02 EvidencePacket; it does not synthesize one from evidence refs;
- extracts unchanged DiagnosticResult objects from qualified COG-16 DiagnosticExecutionResult values;
- validates and reuses COG-18 correlation records from qualified DiagnosticCorrelationResult;
- validates and reuses COG-19 hypotheses from qualified DiagnosticHypothesisResult;
- constructs the existing reviewed CognitiveDiagnosticInterpretationRequest;
- executes the existing reviewed CognitiveDiagnosticInterpreter through an injected COG-06 CognitiveBackend;
- adapter input/interpreter exceptions remain bounded and non-authoritative;
- no interpretation, epistemic, model, correlation, hypothesis or evidence-building logic is recreated.

## Executed qualification

GitHub Actions run: 36262061474
Executed head: 9f3ed3319134f776c29c9c836614fd966f786fb3

PASS:
- Cognitive Bridge: 17/17
- DIAG-01 adapter: 15/15
- CORR-01 integration: 12/12
- HYP-01 integration: 13/13
- INT-01 integration: 13/13
- current reviewed COG-20 source tests: 23/23

Bounded total: 93 PASS / 0 FAIL.

The final implementation/test blobs are identical to those exercised at the passing run. The later candidate commit only restored the pre-existing workflow byte-for-byte.

## Qualified behavior

- authentic COG-02 EvidencePacket remains the interpretation evidence packet;
- COG-16 DiagnosticResult objects pass unchanged into COG-20;
- COG-18 correlation records pass unchanged into COG-20;
- COG-19 hypotheses pass unchanged into COG-20;
- request serialization is deterministic;
- upstream evidence and hypothesis refs remain visible in COG-20 backend projection;
- unsupported FACT promotion is rejected by reviewed COG-20;
- MISSION_CONSTRAINED remains unsupported;
- backend failure remains isolated;
- AUTHORITY=NONE;
- operational_authority=[].

## Scope

Reviewed COG-20 implementation: NOT MODIFIED.
COG-21: NOT STARTED.
Real LFM2.5 backend/runtime: NOT MODIFIED / NOT EXECUTED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Historical Cognitive Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback target:
tangra-cog-v1-hyp-01@6247f1b6e42131319dd5e3d3094d12b99974c97e

Removing/reverting the two INT-01 files restores the qualified HYP-01 state.
