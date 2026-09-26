# TANGRA-COG-V1-DIAG-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420
CANDIDATE: tangra-cog-v1-diag-01@a7df01456ef27e08caf5090cf34818e837e248ca

## Final repository delta

Exactly two files differ from base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_diagnostic_adapter.py
  - blob a72b88a884499931b0630d7a24618dfe7122b2f2
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_diagnostic_adapter.py
  - blob b9c588cf57f704a5f0b66072b76d5d004a5463aa

Temporary qualification workflow changes were restored byte-for-byte. Final workflow blob matches base:
- .github/workflows/cognitive-bridge-qualification.yml
- blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected reviewed components are unchanged from base:
- cognitive_bridge.py: 5f4a6346fa70e369452067d9d96f776a84468a64
- COG-15 registry.py: ecc2ec7eb99d0bbd39a69bc61c8e24d81f5d3525
- COG-16 executor.py: dc5cf6abaded26d9037baa28ca25bce375913fd8

## Implementation

Added a thin adapter only:
- explicit DiagnosticEventBinding binds a validated StateEvent to a reviewed COG-16 evidence type plus explicit timestamp;
- no timestamp is invented because StateEvent has no timestamp field;
- StateEvent source/provenance/realism/claim/evidence/correlation metadata is preserved inside bounded diagnostic evidence;
- reviewed DiagnosticEvidenceItem, DiagnosticEvidenceBundle, DiagnosticExecutionRequest, DiagnosticExecutionResult and DiagnosticExecutor contracts are reused;
- adapter input/executor failures are isolated into bounded non-authoritative result statuses;
- AUTHORITY=NONE and operational_authority=[] remain fixed;
- no model, COG-18, COG-19, Experience, runtime mutation, command or Pi surface was added.

## Executed qualification

GitHub Actions run: 36259985861
Executed head: 30a9d57f57c6cc53a414abaabc40f0d472a066ff

PASS:
- Cognitive Bridge qualification: 17/17
- DIAG-01 adapter tests: 15/15
- reviewed original COG-16 source tests against packaged implementation: 29/29

Total bounded executed assertions: 61 PASS, 0 FAIL.

The final implementation/test blobs are identical to those exercised at the passing run. The later candidate commit only restored the pre-existing workflow byte-for-byte.

## Rework history

Two bounded validation-methodology defects were found and corrected:
1. Initial adapter draft attempted to substitute event_id for a missing StateEvent timestamp. This was rejected as semantically invalid; the final binding requires an explicit timestamp.
2. An adapter test expected UNKNOWN for TRACK_HISTORY containing one empty sample. Reviewed COG-16 correctly classifies that sample as an executed FAIL. The test was corrected to exercise the genuine UNKNOWN contract using incomplete DETECTION_EVENTS data.

An earlier package-wide pytest attempt also failed during collection because the historical package-wide workflow lacks required PYTHONPATH package roots. This was a harness/environment defect and was not treated as DIAG-01 implementation failure. Qualification therefore used the bounded acceptance surface above.

## Scope / authority

COG-18, COG-19, COG-20, COG-21, COG-22, COG-26, COG-27, COG-30: NOT MODIFIED.
Production TANGRA / Raspberry Pi: NOT TOUCHED.
Codex: NOT USED.
Historical Bridge cumulative 317-test regression: NOT EXECUTED / NOT CLAIMED.

## Rollback

Exact rollback is the base checkpoint:
cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420

Reverting/removing the two added DIAG-01 files returns the candidate tree to the base implementation state.
