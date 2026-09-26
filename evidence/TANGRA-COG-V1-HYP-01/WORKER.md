# TANGRA-COG-V1-HYP-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-corr-01@e5cf7a7e3f28eef1c97442c723d6a547dd1895ea
CANDIDATE: tangra-cog-v1-hyp-01@6247f1b6e42131319dd5e3d3094d12b99974c97e

## Upstream qualified dependencies

- TANGRA-COG-V1-DIAG-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-CORR-01: WORKSHOP_QUALIFIED
- Historical TAI-COG-19 implementation: PASS / REVIEWED

## Final repository delta

Exactly two files differ from the qualified CORR-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_diagnostic_hypothesis_adapter.py
  - blob 8a6014c65769a02534383d78ea70192cffbfe55c
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_diagnostic_hypothesis_adapter.py
  - blob 632ddc46b8b11fdc5fb33fca503da588bcab237e

Temporary qualification workflow changes were restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected component blobs unchanged from base:
- CORR-01 adapter: 1a99368b19cd57859378c40d1547fd5d000dc1f4
- DIAG-01 adapter: a72b88a884499931b0630d7a24618dfe7122b2f2
- reviewed COG-19 engine: ef75b5481550649ce9717b9410b0091a1fac65d5
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a thin reviewed-COG-19 connection adapter:
- DiagnosticHypothesisBinding explicitly binds result_ref + DiagnosticDomain + qualified COG-16 DiagnosticExecutionResult.
- COG-16 outputs without DiagnosticResult are rejected before COG-19.
- Existing HypothesisInput.from_execution is reused.
- Existing DiagnosticCorrelationResult records from qualified CORR-01 are validated and passed directly as reviewed COG-18 correlation records.
- Existing DiagnosticHypothesisRequest and DiagnosticHypothesisEngine are reused.
- No hypothesis rule, confidence rule, next-diagnostic rule, causality rule or diagnostic algorithm is recreated.
- adapter input failures map to bounded INVALID_REQUEST.
- engine exceptions are isolated into bounded FAILED.
- AUTHORITY=NONE and operational_authority=[] remain fixed.
- no COG-20 interpretation work was added.

## Executed qualification

GitHub Actions run: 36260858438
Executed head: 2fb3dfb23ad1f7059673428a70684415715b6f47

PASS:
- Cognitive Bridge: 17/17
- DIAG-01 adapter: 15/15
- CORR-01 integration: 12/12
- HYP-01 integration: 13/13
- current reviewed COG-19 source tests: 21/21

Bounded total: 78 PASS / 0 FAIL.

The final implementation/test blobs are identical to the passing run. The later candidate commit only restored the pre-existing workflow byte-for-byte.

## Qualified behavior

- real qualified DIAG-01 outputs and CORR-01 results drive the genuine reviewed COG-19 engine;
- evidence refs and supporting correlation refs remain traceable;
- claims remain ClaimClass.HYPOTHESIS;
- verified_cause remains NONE;
- authority remains NONE;
- operational_authority remains empty;
- UNKNOWN diagnostic evidence yields INSUFFICIENT_EVIDENCE rather than degradation hypothesis;
- MISSION_CONSTRAINED remains unsupported;
- next diagnostic remains suggestion-only with execution_performed=False;
- failures remain isolated and non-operational.

## Scope

COG-19 implementation: NOT MODIFIED.
COG-20: NOT STARTED / NOT MODIFIED.
Later Cognitive units: NOT MODIFIED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Historical Cognitive Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback target:
tangra-cog-v1-corr-01@e5cf7a7e3f28eef1c97442c723d6a547dd1895ea

Removing/reverting the two HYP-01 files restores the qualified CORR-01 state.
