# SELF-MODEL-02 — CODEX HANDOFF

TASK_ID: SELF-MODEL-02
PROJECT: TANGRA
STATUS: READY_FOR_CODEX_EXECUTION
EXECUTOR: CODEX
AUTHORIZATION: evidence/SELF-MODEL-02/CODEX_AUTHORIZATION.md

## Objective
Implement and executable-test exactly the minimum Persistent Identity Continuity record/validator defined by `tasks/SELF-MODEL-02.md` and accepted SELF-MODEL-01.

## Target
- Repository: `nevincho/TANGRA-2.0`
- Branch: `tai-cog-32-package`
- Verified pre-change checkpoint: `9629a624358b8ae539ac1af54af72b9828ba5632`
- Architecture authority: `nevincho/TANGRA-CL:main @ 32280d296a3926cf8db2f579400c45d2b4d6a7b6`

Before mutation verify target remains compatible; stop on contradiction.

## Existing preparation
Read `tasks/SELF-MODEL-02.md`, `evidence/SELF-MODEL-02/SCOUT.md`, `evidence/SELF-MODEL-02/WORKER.md`, and accepted SELF-MODEL-01 contract.
Reuse verified repository conventions: frozen dataclasses; canonical JSON; SHA-256 deterministic semantic hashing; explicit enum validation outcomes; fixture/contract style. Do not create a parallel framework.

## Exact implementation
Implement only the accepted fields and validator/codec required by canonical task. Integrity covers all accepted semantic fields except integrity.integrity_value. Fail closed. Experience refs are refs only.

authority=NONE
operational_authority=[]

## Required execution
Run all primary validation and all nine confirmation cases from `tasks/SELF-MODEL-02.md`.
Run smallest applicable existing cognitive regression; if cheap complete unit suite exists, run it.
Perform task-local repository hygiene.

## Protected / non-goals
No startup/runtime/Pi5/production/mission/backend-context/COG-26 integration.
No redesign/duplication of COG-21/22/23/24/26, State/Evidence, Digital Twin, Diagnostics, Assurance, backend, orchestration, COG-00..28.
No prohibited payload/state persistence, backend_output -> continuity.write(), epistemic promotion, quarantined tangra-cl-ssm-* base/reuse, or SELF-MODEL-03.

## Evidence / checkpoint
Return exact changed files, commands/tests/results, pre/post engineering refs, rollback method, hygiene result, and any failure.
Persist substantive Codex execution evidence under `evidence/SELF-MODEL-02/`.
Successful implementation routes to independent Reviewer; do not mark COMPLETE from Codex result alone.
