# WORKSHOP-COMM-G1-QUALIFICATION-01 — Worker execution evidence

DATE: 2026-10-30
ROLE: WORKER / repository-safe Windows qualification
TASK: tasks/WORKSHOP-COMM-G1-QUALIFICATION-01.md
STATE: WINDOWS_BASELINE_31_PASS / ADDITIONAL_CONTRACT_NEGATIVE_FAIL / G1_REWORK_REQUIRED
REPOSITORY: nevincho/WORKSHOP
BRANCH: windows
FROZEN_G1_IMPLEMENTATION: d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23
QUALIFICATION_WORKFLOW: .github/workflows/workshop-g1-windows-qualification.yml
FINAL_RUN: https://github.com/nevincho/WORKSHOP/actions/runs/41135365108
FINAL_RUN_ID: 41135365108
FINAL_JOB_ID: 124336369519
FINAL_RUN_HEAD: 02b572aca57300afa9638570ffb281373728a529
FINAL_RESULT: Baseline run 41135365108 GitHub Actions SUCCESS; 25/25 G1 unit tests PASS; 6/6 Windows qualification fixtures PASS; 0 SKIP/FAIL; GUI process smoke PASS. New adversarial contract test at run 41136200148 FAILED, while both original suites remained PASS.
EXECUTION_PLATFORM: GitHub-hosted Windows Server 2022 (win22, image 20261026.347.1), Windows NT 10.0 build 20348; CPython 3.11.9. Actual Windows NTFS runner; NOT a Windows 10 client workstation.
SOURCE_TREE_MUTATION: Git status before/after tests empty; PYTHONDONTWRITEBYTECODE=1; fixture writes confined to disposable temporary paths.
SOURCE_PROVENANCE: GitHub compare frozen G1 d5369ec... to final run 02b572ac... includes only CI workflow and the registered task; no apps/workshop_g1/ changes. CI logs list exact per-file SHA-256 including trusted TASK_SCHEMA.md d0333fdf...9610 and STATE_MACHINE.md c2153030...f358.
COMMANDS: python -B -m unittest discover -s tests -v; python -B windows_validation.py; python -B main.py launched for two-second smoke. Full commands, output, exit codes and source hashes in raw linked Actions job logs.
WINDOWS_NEGATIVE_COVERAGE: real directory junction denial, file symlink denial (not skipped), UNC/device path denial, simulated root-swap denial, CREATE failure rollback and repeat-denial, OPEN and individual-file IMPORT before/after file-content and metadata snapshots including hidden .git/config fixture; trust tamper, schema mismatch, duplicate IDs, malformed text and inert injection. Fixture-specific, not a general adversarial security proof.
GUI_SCOPE: Tkinter entrypoint alive after two seconds; no real GUI interaction/visual correctness assertion or customer installer test.

## Execution methodology incident, corrected

Initial run 41134868930 failed before tests because shallow checkout lacked historic commit object for a diagnostic git diff command. Removed the invalid diagnostic; G1 source unchanged.
Run 41134947286 reached 25 tests and failed 3 assertions + 14 errors because runner default TEMP used Windows 8.3 short alias C:\Users\RUNNER~1\AppData\Local\Temp while G1 rejects path aliases whose opened-handle canonical name differs. Read-only diagnostic run 41135038945 confirmed final path C:\Users\runneradmin\AppData\Local\Temp. This is a test environment/path-alias mismatch, not evidence of unsafe traversal. A job-level runner.temp expression caused workflow validation failure before jobs at 41135149491; fixed by setting TMP/TEMP within test steps. Canonical D:\a\_temp then passed 31 tests at run 41135235852. Final run 41135365108 added GUI process smoke and passed. Earlier CI attempts remain in GitHub Actions history, not duplicated as repository log files.

## New confirmed contract failure (2026-10-30)

A further read-only Windows CI negative fixture tested a Markdown document with a fenced code example containing a line TASK_ID: DEMO. Expected: inert documentation. Actual from frozen G1 code: FENCED_TASK_FIELD_CLASSIFICATION=task_candidate. Run https://github.com/nevincho/WORKSHOP/actions/runs/41136200148 (job 124339154766), assertion failed with explicit G1 contract violation; 25 original tests and 6 Windows fixtures still passed. The preceding run 41136059404 used incorrectly escaped newline literals and was not a valid negative test; corrected fixture in run 41136200148 is authoritative. This is an IMPLEMENTATION/PARSER contract defect, not a Windows environment failure. Frozen source has not been changed. Repair must ignore fenced Markdown code blocks in task classification and field extraction, with bounded regression tests and a new source checkpoint.

## Unresolved acceptance / next role

1. Independent Reviewer must inspect frozen source, raw Windows CI logs and G1 contract. Earlier independent review from 2026-10-29 was of older commit 99723c...; re-evaluate code findings against five later G1 commits through d5369ec, not blindly reuse old verdict.
2. Windows Server CI verifies actual NTFS fixtures and process launch; clean Windows 10/11 customer GUI interaction and release packaging are NOT VERIFIED. Owner-reported Windows ZIP launch is not an independent CI result.
3. Raw SHA-256 identity of owner-local delivered ZIP is not independently verified here.
4. Adversarial simultaneous pathname races and full reference semantics beyond the negative fixtures remain subject to independent review.
5. No independent G1 PASS or validated checkpoint; do not promote G1 to COMPLETE or authorize G2 implementation on this record alone.

ROUTING: Actual WORKER qualification executed using GitHub-hosted Windows runner without Codex. Forward to independent Reviewer. Any local Windows customer acceptance must use a verified host/Codex Gate, not inferred from Actions.
ROLLBACK: Isolated CI workflow can be reverted; frozen G1 source intact.
HYGIENE: One reusable CI workflow and this concise evidence; no generated caches or log dumps committed.
