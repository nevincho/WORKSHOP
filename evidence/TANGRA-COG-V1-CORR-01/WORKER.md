# TANGRA-COG-V1-CORR-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-diag-01@a7df01456ef27e08caf5090cf34818e837e248ca
CANDIDATE: tangra-cog-v1-corr-01@e5cf7a7e3f28eef1c97442c723d6a547dd1895ea

## Final repository delta

Exactly two files differ from the qualified DIAG-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_diagnostic_correlation_adapter.py
  - blob 1a99368b19cd57859378c40d1547fd5d000dc1f4
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_diagnostic_correlation_adapter.py
  - blob 689038c973174b5f2ab6bd82c003b7647e98b8ba

Temporary qualification workflow changes were restored byte-for-byte to baseline blob:
- .github/workflows/cognitive-bridge-qualification.yml
- blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected component blobs are unchanged from base:
- DIAG-01 adapter: a72b88a884499931b0630d7a24618dfe7122b2f2
- reviewed COG-18 correlation engine: 48732fcfab19310583f277650f16ec2ca14dff75
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added only a thin reviewed-COG-18 connection adapter:
- DiagnosticCorrelationBinding requires explicit result_ref, DiagnosticDomain, COG-16 DiagnosticExecutionResult, timestamp, sequence_id and source_ref.
- No domain, timestamp, sequence identity or source reference is inferred.
- COG-16 results without a DiagnosticResult are rejected before correlation.
- Existing DiagnosticCorrelationInput.from_execution_result is reused.
- Existing DiagnosticCorrelationRequest and DiagnosticCorrelationEngine are reused.
- Adapter-level malformed input maps to INVALID_REQUEST.
- Engine exceptions are isolated as FAILED.
- AUTHORITY=NONE and operational_authority=[] remain fixed.
- No causation assertion is introduced; COG-18 causal_claim=NONE remains authoritative.
- No COG-19, Experience, FAST, Knowledge, model or runtime integration work was added.

## Executed qualification

GitHub Actions run: 36260593915
Executed head: 699020f72838259bc0d0012332936fde1a827ce9

PASS:
- Cognitive Bridge qualification: 17/17
- DIAG-01 adapter qualification: 15/15
- CORR-01 integration qualification: 12/12
- current reviewed COG-18 source tests: 31/31

Total bounded executed assertions: 75 PASS, 0 FAIL.

The final implementation/test blobs are identical to those exercised at the passing run. The later candidate commit only restored the pre-existing workflow byte-for-byte.

## Validation rework history

Two bounded validation-methodology defects were found:
1. First run could not import COG-18 because the qualification PYTHONPATH omitted the existing state_evidence package root required transitively by tangra_diagnostic_replay/tangra_state_recorder. Only the test environment was corrected.
2. Second run had one CORR-01 test using Python object identity (is) against a newly recomputed but equal DiagnosticResult. The test was corrected to contract equality (==). Implementation did not require rework.

No reviewed COG-18 implementation defect was established.

## Scope / authority

COG-18 implementation: NOT MODIFIED.
COG-19 and later units: NOT MODIFIED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Historical Cognitive Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback target:
tangra-cog-v1-diag-01@a7df01456ef27e08caf5090cf34818e837e248ca

Removing/reverting the two CORR-01 added files restores the qualified DIAG-01 state.
