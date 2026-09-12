# TAI-COG-00 — WORKER EVIDENCE

TASK_ID: TAI-COG-00
PROJECT: TANGRA / TAI
DATE: 2026-09-12
EXECUTION_CLASS: WORKER / repository-side Phase A engineering

## Implementation location

Repository: `nevincho/TANGRA-2.0`
Branch: `tai-cog-00`
Path: `TANGRA_2_0/00_FOUNDATION/TAI_COG_00/`
Base main commit: `2e218cb0124ad659d2cb41a87cdf9bfef7e8e6ec`
Observed branch head after final test expansion: `7036cb78580d446ba700e318daf0bbe8c60d4afc`

## Files in branch diff

- `README.md`
- `fixtures/sample_state_event.json`
- `tangra_cognitive_substrate/__init__.py`
- `tangra_cognitive_substrate/contracts.py`
- `tests/test_contracts.py`

The branch is ahead of main only; no existing TANGRA-2.0 files were modified.

## Implemented contracts

- `StateEvent`
- `SystemIdentity`
- `NodeIdentity`
- `RuntimeIdentity`
- `EmbodimentIdentity`
- `Provenance`
- `StateDomain`
- `RealismClass`
- `ClaimClass`
- `ValidationState`
- `MissionState`
- `MissionContext`
- `CapabilityDescriptor`
- `ScenarioDescriptor`
- `ValidatedConfigurationDescriptor`
- `HumanIdentityDescriptor`
- `ReportClaim`
- `StructuredReport`
- canonical `VLADIMIR_KRUMOV` descriptor + alias resolver
- generic deterministic JSON serialization/deserialization/validation

## Hard invariants evidenced

- relationship/authentication/operational authority are separate fields; canonical human fixture has `authenticated=False` and empty `operational_authority` despite CREATOR/FOUNDER/CHIEF_ARCHITECT relationships;
- defaults preserve `UNKNOWN`/`SOURCE_GAP`;
- provenance includes direct/received/deterministic-derived/cognitive-inferred/experience/simulated/operator/unknown/source-gap classes;
- realism classes preserve LIVE/REPLAY/SHADOW/SYNTHETIC/HISTORICAL distinction;
- arbitrary enum values are rejected;
- configuration default/fallback values are rejected when outside an explicit allow-list;
- `T.A.N.G.R.A.` acronym expansion defaults to `SOURCE_GAP` and a non-authoritative expansion is rejected;
- no model/provider-specific dependency or field is required;
- Python standard library only.

## Validation runs

Initial test run exposed two decoder defects caused by postponed annotations:
- invalid provenance was not rejected;
- nested `ReportClaim` deserialized as a raw dict.

Correction: generic decoder now resolves runtime type hints with `get_type_hints()` before nested enum/model decoding.

Final validation:

`python -m py_compile tangra_cognitive_substrate/contracts.py tangra_cognitive_substrate/__init__.py tests/test_contracts.py` -> PASS

`python -m unittest discover -s tests -v` -> `12 tests / 12 PASS / 0 FAIL / 0 ERROR`

Coverage includes:
- round-trip serialization for all primary requested contract classes;
- StateEvent round-trip;
- invalid provenance/state-domain rejection;
- UNKNOWN/SOURCE_GAP defaults;
- provenance/realism class distinction;
- all required human aliases resolving to `VLADIMIR_KRUMOV`;
- relationship does not grant authentication/operational authority;
- StructuredReport preservation of claim class/provenance/realism/evidence/freshness;
- Scenario validation state preservation;
- ValidatedConfiguration validation state and allow-list rejection;
- acronym expansion SOURCE_GAP guard;
- static synthetic StateEvent fixture validation.

## Runtime/production impact

NONE. No Pi5 access. No runtime integration. No production modification. No protected HQ/Hailo/NanoTracker/CA Kalman/CURRENT_TARGET/HOROS change. No FC/carrier/actuation. No Codex. No COG-01.

## Duplication check

No duplicate cognitive runtime mechanism was added. The package is a standalone contract substrate. Existing accepted semantics (provenance, authority separation, scenario validation, UNKNOWN/SOURCE_GAP) are represented as contracts rather than reimplemented as competing runtime services.
