# TANGRA-COG-BRIDGE-01 — cumulative regression payload progress

DATE: 2026-09-20
TARGET_HEAD: bd11d92f396b68de00a0f3636ae49ed8310ce420
WORKSPACE: /tmp/tangra_bridge

FILES_REQUIRED_TOTAL: 54
FILES_ALREADY_VERIFIED_BEFORE_THIS_BATCH: 2
FILES_ADDED_THIS_BATCH: 6
FILES_VERIFIED_TOTAL: 8
FILES_REMAINING: 46
FAILED_OR_TRUNCATED_RETRIEVAL: NONE

## Required-payload accounting

The 54-file bounded regression payload is the 15 allowlisted tests, 7 test fixtures, 2 regression-control files, 26 Cognitive implementation/package files required by those tests, and 4 phase_b implementation/fixture files. The existing bridge-only implementation/test files are not counted unless required by the cumulative runner.

Verified before batch:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/foundation/tangra_cognitive_substrate/__init__.py — b5e32726db671d8dd666c85b9568eeeb2ef7f524
- TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/foundation/tangra_cognitive_substrate/contracts.py — 228d33108bd7b5494a5814653dd4ee38ab26869c

Added and identity-verified this batch:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/regression/run_units_1_10.py — authoritative/local b7c2cdfc791578174e4356086cc6c0e4b04af5b5 — PASS
- TAI_COGNITIVE_INTEGRATION_PACKAGE/regression/units_1_10_active_surface.json — authoritative/local 6e9ede9d5dd71083ca128fb2255d7fdd1a9b2f25 — PASS
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/fixtures/sample_state_event.json — authoritative/local e814306dd31afdd1abcd0bba77f6b4bf1ddf9c79 — PASS
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/fixtures/backend_response_valid.json — authoritative/local b5cb5d0d98b1fa5e4effa47c20cc7e6a4fbaf24c — PASS
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/fixtures/correlation_policy.json — authoritative/local d13b92d5f2aee3ce8db3ca806e23a4e025cb293f — PASS
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/fixtures/hypothesis_policy.json — authoritative/local 0fcaf8f9e24751c144adc36aa89ee93e7a0881e2 — PASS

All newly materialized files preserve repository-relative paths. Git blob identity was computed from local bytes as sha1("blob " + byte_length + NUL + bytes).

CUMULATIVE_REGRESSION: NOT RUN — payload intentionally incomplete.
BRIDGE_17_TEST_SUITE: NOT RERUN.
RESULT: INCREMENTAL MATERIALIZATION IN PROGRESS
