# SELF-MODEL-02 — SCOUT / WORKER HANDOFF

STATUS: READY_FOR_WORKER
DATE: 2026-09-19
TASK: `tasks/SELF-MODEL-02.md`

## Routing decision

Current TANGRA project profile authorizes bounded Phase-A repository engineering and deterministic repository tests. SELF-MODEL-02 is explicitly human-authorized by Control Room, additive, independently testable, and does not require Pi5/production/runtime access.

Execution route: WORKER.
Codex: NOT AUTHORIZED for this phase.
Runtime integration: NOT AUTHORIZED.

## Verified prerequisite / duplication state

- Accepted Cognitive Layer base supplied for this gate: `nevincho/TANGRA-CL:main @ 32280d296a3926cf8db2f579400c45d2b4d6a7b6`.
- SELF-MODEL-01 contract is the architectural prerequisite supplied by Control Room.
- No canonical `tasks/SELF-MODEL-02.md`, handoff, or SELF-MODEL-02 Scout artifact existed in WORKSHOP before this routing recovery.
- Quarantined `tangra-cl-ssm-*` branches remain excluded.
- Worker must re-verify current target repository state and existing mechanisms before implementation and must not duplicate an already-existing equivalent component.

## Worker objective

Implement the minimum deterministic PersistentIdentityContinuity record/validator defined in `tasks/SELF-MODEL-02.md`, using only the accepted SELF-MODEL-01 fields and existing TANGRA conventions where suitable.

## Target

Engineering implementation repository: `nevincho/TANGRA-2.0`, branch `tai-cog-32-package`.
Referenced engineering tree: `9629a624358b8ae539ac1af54af72b9828ba5632`.

Worker must record exact current pre-change engineering commit before mutation. Repository/runtime evidence overrides stale coordination state.

## Validation required

Primary:
- valid record -> canonical serialization -> deserialize -> validate -> VALID;
- equivalent accepted records serialize identically;
- integrity-covered mutation without recomputation -> INTEGRITY_MISMATCH.

Confirmation:
- reject missing system_id;
- reject missing continuity_id;
- reject wrong schema_type;
- reject unsupported schema_version;
- reject unsupported integrity scheme;
- reject malformed integrity;
- reject modified experience_refs without integrity recomputation;
- reject malformed provenance;
- reject malformed root.

Regression: applicable existing cognitive contract/unit regression per current validation policy.

## Protection

No startup/runtime integration, production/Pi5 action, COG-21/22/26 redesign, Experience payload persistence, OSM persistence, backend state/identity persistence, authority change, or quarantined-branch reuse.

`authority=NONE`
`operational_authority=[]`

## Completion route

Worker -> persist exact implementation/test evidence in `evidence/SELF-MODEL-02/` -> state REVIEW -> independent Reviewer -> PASS -> validated checkpoint record.

Reviewer must inspect actual diff/tests and repository hygiene. Worker report alone cannot establish PASS.

STOP after SELF-MODEL-02.
