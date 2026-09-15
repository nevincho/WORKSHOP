# VK-WIRE-02-CORRECTION-01 execution evidence

Status: BEHAVIORAL PASS for bounded correction/conformance suite.

Target repository: `nevincho/LIVE`
Branch: `vk-wire-02-codec`
Commit under test: `3bdba2ec80d8efa56e83a18ed2df39f79ef9ae87`
Rollback/base: `7ec4a6b291c127cf4d299a06b77fcaf2c5289cb1`
Runtime: GitHub hosted Ubuntu 24.04.5, CPython 3.12.14.
Command: `python -m unittest -v tests.test_distributed_wire_v1 tests.test_distributed_wire_v1_correction`
Workflow run: `35018667360`; job `104548454015`; conclusion SUCCESS.
Result: 11 tests PASS, 0 failures, 0 errors.

## Authoritative vector provenance
WORKSHOP authoritative golden path: `evidence/VK-WIRE-01/golden_vectors_v1.json`; Git blob SHA `be675835c4f32ea1ae6b24cc37575a2238572ce8`.
WORKSHOP authoritative rejection path: `evidence/VK-WIRE-01/rejection_vectors_v1.json`; Git blob SHA `ccf5f89100b307ceb67d422fe5096ae575a193f6`.

Exact-byte materializations in LIVE were fetched after write and have the identical Git blob SHAs:
- `tests/fixtures/vk_wire_01_golden_vectors_v1.json` -> `be675835c4f32ea1ae6b24cc37575a2238572ce8`
- `tests/fixtures/vk_wire_01_rejection_vectors_v1.json` -> `ccf5f89100b307ceb67d422fe5096ae575a193f6`

The correction test independently computes Git blob SHA-1 over fixture bytes and requires these exact authoritative blob IDs before vector execution. It then loads all 12 golden vectors and all 25 rejection vectors. Authoritative vector files were not modified.

## Timestamp correction
Calendar/date-time validation now rejects tested impossible month/day/leap-year/hour/minute/second values without normalization. Valid ordinary UTC, leap-day 2024-02-29, and 1/9-digit fractional examples pass. Timestamps remain metadata only; no causal code was introduced.

## Bounded ambiguity
Wire Profile v1 says RFC3339 but does not explicitly state leap-second (`:60`) policy. The task directed that this specific case not be invented. Acceptance tests therefore cover clearly invalid second `61` but make no conformance claim for `60`. Current reference implementation behavior for `:60` is outside this correction's accepted semantics pending explicit profile clarification if needed.

DIST-03 files/tests unchanged. DIST-04 absent. No Codex used.