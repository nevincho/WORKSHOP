# TAI-COG-00

TASK_ID: TAI-COG-00
PROJECT: TANGRA / TAI
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Build the first standalone implementation-ready substrate for the accepted TANGRA Cognitive Architecture.
SOURCE_PLAN_OR_REQUEST: Vlad explicit Control Room task, 2026-09-12; authoritative design `nevincho/TANGRA-DOCS` branch `TAI`.
CURRENT_STATE: VERIFIED repository-side Phase A engineering package on `nevincho/TANGRA-2.0` branch `tai-cog-00`; no runtime integration.
PREREQUISITES: TAI campaign authorized for bounded Phase A WORKSHOP engineering; production/Codex authority remain NONE.
DEPENDENCIES: Accepted Task-01 + Addendum-02 + Addendum-03 architecture package.
AFFECTED_COMPONENTS: standalone cognitive substrate contracts/tests/fixtures only.
PROTECTED_COMPONENTS: production runtime; HQ/Hailo/NanoTracker/CA Kalman/CURRENT_TARGET/HOROS authority; Pi5; FC/carrier/actuation; WIDE-EW campaign state/history.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

## Acceptance criteria
- State/Event schema implemented.
- System/Node/Runtime/Embodiment identity models implemented.
- Provenance + StateDomain semantics implemented.
- MissionContext implemented.
- CapabilityDescriptor implemented.
- ScenarioDescriptor implemented.
- ValidatedConfigurationDescriptor implemented.
- HumanIdentityDescriptor implemented with required canonical identity/aliases/relationships.
- StructuredReport implemented.
- Deterministic serialization/deserialization and validation implemented.
- Missing state remains UNKNOWN/SOURCE_GAP.
- LIVE/REPLAY/SHADOW/SYNTHETIC/HISTORICAL remain distinct.
- Relationship grants no authentication or operational authority.
- Scenario/configuration validation state preserved.
- Deterministic tests PASS.
- No runtime/production/Codex/COG-01 work.

VALIDATION_METHOD: Python standard-library `py_compile`; deterministic `unittest`; branch diff against `main`; independent review of actual package/test evidence.
PRE_CHANGE_CHECKPOINT: `nevincho/TANGRA-2.0` main at `2e218cb0124ad659d2cb41a87cdf9bfef7e8e6ec`.
ROLLBACK_METHOD: discard/delete branch `tai-cog-00`; main/production/runtime are unchanged.
EVIDENCE_PATHS:
- `evidence/TAI-COG-00/WORKER.md`
- `review/TAI-COG-00.md`
- `checkpoints/TAI-COG-00.md`

## Target engineering artifact
Repository: `nevincho/TANGRA-2.0`
Branch: `tai-cog-00`
Path: `TANGRA_2_0/00_FOUNDATION/TAI_COG_00/`

COG-01: NOT STARTED.
