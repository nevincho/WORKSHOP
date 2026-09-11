# HB-04 — Independent Review Result

Date: 2026-09-11
Scope: review only `handoffs/HB-04_SYSTEM_HEALTH_V1_ENGINE_PACKAGE/` at package commit `d0763c7722c25fce68480a61e53f2de7d7cd6677` against the accepted HB-02/HB-03 contracts and `review/HB-04_SYSTEM_HEALTH_V1_REVIEW_REQUEST_20260911.md`.

## RESULT

**FAIL — one bounded contract defect.**

## Verified facts

- Exactly 12 canonical concepts: PASS.
- Standalone package structure and integration manifest: PASS.
- Existing test suite: 15/15 PASS when executed independently.
- No production Dashboard/Pi/runtime integration performed by the package: PASS.
- No invented numeric threshold found; WIDE uses source-provided `max_age_s`: PASS.
- STALE/UNAVAILABLE/NOT_VERIFIED protections are present across tested cases: PASS, except for the defect below affecting current WIDE failure semantics.

## Defect

`system_health_v1/engine.py` derives `WIDE_PIPELINE_HEALTH=FAULT` whenever cumulative `wide_worker.failures > 0`, even when:
- `running=true`;
- `last_fresh=true`;
- `last_age_s <= max_age_s`;
- `last_error=null`;
- `environment_last_error=null`.

Minimal independent simulation result:

```text
input wide_worker: running=true, last_fresh=true, last_age_s=0.1, max_age_s=0.5, failures=1, no current errors
actual state: FAULT
actual reason_codes: [WIDE_FAILURE]
```

This violates accepted HB-02/HB-03 semantics: cumulative/nonzero historical counters are diagnostic context and must not independently establish current `FAULT`; only a direct current failure/error semantic may do so. Counter deltas may be diagnostic but are not an authorized standalone fault rule.

## Required bounded correction

Remove the rule that treats a nonzero cumulative `failures` counter by itself as current `FAULT`. Preserve the counter as supporting diagnostic context. Add a regression test proving a healthy/fresh/running WIDE worker with historical nonzero cumulative failures and no current error does not become `FAULT` solely from that counter.

No other defect is asserted by this review.

## Verdict fields

- CONTRACT_FIDELITY: FAIL
- TEST_EVIDENCE: existing suite 15/15 PASS; added independent simulation exposes uncovered contract defect
- BOUNDARY_EVIDENCE: PASS
- FALSE_GREEN_PROTECTION: PASS for reviewed false-green cases; defect is false-fault/current-state semantics, not false-green
- INTEGRATION_READINESS: FAIL pending bounded WIDE correction and regression test
- DEFECTS: one, as above

STOP.
