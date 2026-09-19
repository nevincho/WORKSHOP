# SELF-MODEL-02 — Persistent Identity Continuity Record / Validator

TASK_ID: SELF-MODEL-02
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: READY
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

## Objective

Implement the minimum deterministic PersistentIdentityContinuity record/validator accepted by SELF-MODEL-01. This is a standalone Phase-A repository engineering unit only; no runtime/startup integration.

## Authoritative target / base

- Cognitive Layer authority: `nevincho/TANGRA-CL:main`
- Accepted base: `32280d296a3926cf8db2f579400c45d2b4d6a7b6`
- Engineering implementation/provenance: `nevincho/TANGRA-2.0`, branch `tai-cog-32-package`
- Referenced engineering tree: `9629a624358b8ae539ac1af54af72b9828ba5632`
- Architecture prerequisite: SELF-MODEL-01 Persistent Identity Continuity Contract = PASS
- Before mutation, Worker MUST re-verify current target heads/state and stop on contradiction rather than silently rebasing architecture.

## Required implementation

Implement a bounded record and deterministic validator/codec corresponding logically to PersistentIdentityContinuityRecord / PersistentIdentityContinuityValidator, following existing repository naming/style.

Represent only:
- schema_type
- schema_version
- continuity_id
- system_id
- experience_refs[]
- provenance.source
- provenance.accepted_at
- provenance.acceptance_basis_refs[]
- integrity.integrity_scheme
- integrity.integrity_value

Provide:
- deterministic canonical serialization/deserialization;
- schema/type/version/required-field validation;
- deterministic integrity generation and verification;
- explicit machine-readable outcomes including VALID and bounded classifications for missing field, invalid type/value, wrong schema, unsupported version/scheme, malformed integrity, integrity mismatch, malformed record;
- fail-closed loading.

Integrity covers all accepted semantic fields except integrity.integrity_value itself. Serialization/integrity must not depend on dictionary insertion order, runtime address, backend formatting, locale, or serialization-generated timestamps.

Use the smallest suitable deterministic integrity mechanism already present in the engineering environment; no signatures, PKI, encryption, key management, secrets, or hardware identity.

## Pre-implementation discovery / reuse

Worker MUST inspect current engineering implementation for reusable:
- frozen/immutable contracts;
- deterministic IDs;
- canonical JSON;
- schema/version handling;
- integrity/hash utilities;
- provenance;
- validation-result conventions;
- fixture serialization;
- COG-22 ExperienceStore export/import;
- cognitive substrate contract style.

Reuse existing conventions where cleanly applicable. Do not create a parallel serialization/validation framework.

## Protected / excluded

Smallest additive change only.

Do NOT:
- integrate into cognitive startup/runtime, production, Pi5, mission runtime, backend context, or COG-26 assembly;
- redesign/duplicate COG-21, COG-22, COG-26, State/Evidence, Digital Twin, Diagnostics, Assurance, Cognitive Backend, orchestration, or COG-00..COG-28;
- persist ExperienceRecord payloads, OSM snapshots, Cognitive Signals, backend identity/state/native memory, runtime identity, embodiment snapshot, hardware/config, mission, health, capabilities, diagnostics, hypotheses/inferences, Digital Twin state, or current authority;
- create a generic backend_output -> continuity.write() path;
- promote epistemic state;
- grant authority.

Component contract:
- authority=NONE
- operational_authority=[]

Quarantined `tangra-cl-ssm-*` branches are non-authoritative and MUST NOT be used as implementation base, merged, continued, or repaired.

## Primary validation

Create a valid record and prove:
1. record -> canonical serialize -> deserialize -> validate -> VALID;
2. equivalent accepted input -> identical canonical serialization;
3. mutate an integrity-covered field (e.g. system_id) without recomputing integrity -> INTEGRITY_MISMATCH.

## Confirmation validation

Deterministically reject at minimum:
1. missing system_id;
2. missing continuity_id;
3. wrong schema_type;
4. unsupported schema_version;
5. unsupported integrity_scheme;
6. malformed integrity_value;
7. modified experience_refs without integrity recomputation;
8. malformed provenance;
9. malformed root record.

Experience refs are structural references only; this task does not resolve or validate COG-22 existence/truth.

## Regression

Run the smallest applicable existing regression required to show the additive component did not break existing cognitive contracts. If a cheap complete unit suite exists, run it. Do not claim runtime validation from repository unit tests.

## Acceptance criteria

PASS requires evidence that:
- SELF-MODEL-01 field boundary is preserved;
- canonical serialization is deterministic;
- valid round-trip is VALID;
- unchanged integrity verifies and covered mutation is detected;
- malformed/unsupported records fail closed with explicit classifications;
- Experience payloads, COG-26 state, Cognitive Signals and backend identity/state are not persisted;
- no backend-to-continuity authority path exists;
- authority remains NONE / operational_authority=[];
- applicable regression passes;
- task-local repository hygiene passes;
- independent Reviewer returns PASS;
- exact post-change validated checkpoint is recorded.

## Checkpoint / rollback

PRE_CHANGE_CHECKPOINT: `nevincho/TANGRA-CL:main @ 32280d296a3926cf8db2f579400c45d2b4d6a7b6` is the accepted architecture base. Worker MUST additionally record the exact current engineering-repository pre-change commit before mutation.

ROLLBACK_METHOD: revert/reset only the SELF-MODEL-02 additive engineering commit(s) to the recorded engineering pre-change checkpoint; do not alter protected production/runtime.

POST_CHANGE_CHECKPOINT: exact engineering repository commit only after validation and independent Reviewer PASS.

## Evidence / review route

Worker persists substantive execution/test evidence under `evidence/SELF-MODEL-02/`, then routes actual diff/test evidence to independent Reviewer. COMPLETE requires Reviewer PASS plus checkpoint evidence.

STOP after SELF-MODEL-02. Do not create or execute SELF-MODEL-03.
