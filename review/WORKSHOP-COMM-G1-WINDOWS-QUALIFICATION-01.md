# WORKSHOP-COMM-G1-QUALIFICATION-01 — Independent G1 acceptance review

DATE: 2026-10-30
ROLE: INDEPENDENT REVIEWER — read-only source/contract/actual GitHub Actions logs; not Worker, not Control Room
VERDICT: FAIL — canonical G1 acceptance NOT MET
G1_STATUS: NOT COMPLETE; NO G1 checkpoint; G2 NOT AUTHORIZED
FROZEN_IMPLEMENTATION: d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23
BASELINE_PASS_RUN: https://github.com/nevincho/WORKSHOP/actions/runs/41135365108
CONTRACT_NEGATIVE_FAIL_RUN: https://github.com/nevincho/WORKSHOP/actions/runs/41136200148
CONTRACT: planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md
SOURCE: apps/workshop_g1/{workshop_g1/core.py,workshop_g1/app.py,tests/test_g1.py,windows_validation.py} at frozen implementation

## Independently verified evidence

1. GitHub compare frozen `d5369ec` to baseline CI head `02b572a` is ancestor/ahead by seven commits and lists ONLY the CI workflow and task file as added. Nine application, trust, test and Windows qualification files were individually fetched at both refs; their Git blob identities match exactly. This verifies repository source identity at the baseline CI run; it is not a raw SHA-256 of an owner-local ZIP.
2. Retrieved actual raw job logs for Windows Actions run 41135365108, job 124336369519. Workflow run conclusion SUCCESS. The log identifies `SOURCE_COMMIT=02b572aca57300afa9638570ffb281373728a529`, runner image `win22 20261026.347.1`, CPython 3.11.9, `Windows-10-10.0.20348-SP0` (Windows Server 2022, not Windows 10 client). Logs include per-source SHA-256, exact commands, per-test output, step success and before/after fixture metadata. Source tree `git status --porcelain` before and after tests was empty.
3. The baseline run genuinely executed **25/25 unit tests PASS** and **6/6 Windows qualification tests PASS**, **0 SKIP/FAIL/ERROR**. The Windows suite exercised actual NTFS directory junction and file-symlink refusal, UNC/device denial, controlled directory replacement during enumeration, CREATE repeat refusal and injected pre-open rollback, and OPEN/individual-file IMPORT before/after content/metadata snapshots including `.git/config`. These are real, bounded fixture results, not simulated Windows filesystem claims. They do NOT prove comprehensive concurrent race safety.
4. GUI evidence is only a Tkinter `main.py` process surviving two seconds on the hosted Windows Server runner. No UI button interaction, clean Windows 10/11 client run, installer, or owner-local ZIP hash was independently qualified. Packaging is not intrinsically part of the first G1 gate; do not conflate it with the required clean-client acceptance specified by this qualification task.
5. Independently retrieved raw job logs for Actions run 41136200148, job 124339154766, at head `eefd421d77936f1c93f86d0c9833e06e2c136590`: the same 25+6 tests still PASS, but the newly added *fenced Markdown task field remains inert* negative step **FAILS** with `FENCED_TASK_FIELD_CLASSIFICATION=task_candidate` and `AssertionError: G1 contract violation`. This is an actual reproducible implementation/contract failure, not an environment issue. The negative step did not exist at the earlier green CI run.

## Findings and acceptance gaps

**F1 — CONFIRMED FAIL, parser inertness.** Frozen `core.py` `document_kind()` scans for `TASK_ID:` anywhere in text; `parse_task()` accepts machine-like fields inside fenced Markdown. A documentation-only code example such as `README.md` with a fenced `TASK_ID: DEMO` becomes a task candidate. The added Windows negative fixture confirms this. Violates contract C.8 / G1 negative fixture intent. The later branch includes a proposed fenced-block correction; that change is **outside the frozen implementation** and must receive fresh tests/review before acceptance.

**F2 — SOURCE-LEVEL DEFECT, CREATE rollback after file creation.** Frozen `create_workspace()` appends `workspace.json` to the `created` rollback list only *after* writing, flushing and `os.fsync()`. If a write/flush/fsync operation fails after `os.open(...O_EXCL)` creates the file, the exception handler attempts to remove `tasks/` and root but never unlinks the newly created `workspace.json`. The root can remain partially created, contrary to contract B atomic failure rollback. Existing tests inject failure *before* `os.open`, not after file creation. This is an inspection-derived deterministic failure path; an exact injected-fsync Windows test is still NOT VERIFIED.

**F3 — SOURCE-LEVEL GAP, OPEN workspace version/manifest diagnostics.** `inspect_workspace()` verifies the application-bundled trust files but does not read or validate the selected root's `workspace.json`, its `workspace_version` or `trusted_commit`. OPEN and IMPORT FOLDER share this function. An existing `tasks/` directory is sufficient to display rows even if workspace metadata is missing/incompatible. Contract B requires diagnostics for unknown workspace versions/invalid workspace manifest/missing data. Distinguish strict OPEN from untrusted folder IMPORT; do not make IMPORT write or trust external metadata.

**F4 — SOURCE-LEVEL GAP, UTF-8 line byte bound.** `read_limited()` checks `len(line) > MAX_LINE` on decoded Unicode characters, not encoded UTF-8 byte count. A line with >16 KiB of multibyte UTF-8 but fewer than 16,384 code points passes this check. Contract C.1 defines a 16 KiB line limit. A direct multibyte negative test is missing.

**F5 — SOURCE-LEVEL GAP, trusted provenance presentation.** `verified_trust()` strictly checks expected manifest keys, profile, repository, pinned commit, source paths and SHA-256 of both bundled schema documents, and tests cover missing/tampered files. However `app.py` does not display the verified commit and file hashes in the GUI; contract G1 acceptance requires the verification to *report* exact commit + hashes. The hashes are available in the manifest/CI logs, but a user-visible G1 provenance report is NOT VERIFIED.

**F6 — VALIDATION GAPS, not automatic implementation failures.** The 31 green tests do not demonstrate an after-create failure rollback, actual clean Windows 10/11 GUI interaction, adversarial simultaneous parent/root swap during CREATE, unreadable-file Windows ACL denial, or complete project/context reference resolution. Windows `test_root_swap_during_enumeration_fails_closed` injects a controlled directory rename using a patched `Path.iterdir`, not an uncontrolled concurrent attacker. These untested acceptance areas remain NOT VERIFIED; do not claim the code is exploitable solely from missing coverage. Contract B/C require fail-closed identity and meaningful negative coverage. The later green-run source snapshot does not replace these missing tests.

## Decision and smallest legitimate next action

**FAIL** for frozen G1, not a generic execution-access blocker. Preserve successful Windows NTFS evidence; do not rerun the 31 tests merely to reproduce already established PASS. Worker may correct the demonstrated parser defect and add focused negative tests; separate targeted bounded corrections are needed for F2–F5 and any contract-required F6 qualification. Verify each correction against the new candidate commit, raw Windows CI logs and the exact G1 contract, then conduct a fresh independent acceptance review. No G1 COMPLETE, checkpoint, G2 execution or protected-scope changes are authorized by this review.

REVIEW_METHOD: Independent direct GitHub blob comparison, code/contract inspection, raw Windows CI job-log inspection; no local Windows GUI runtime, no Codex, no paid API, no Work. Confidence HIGH in F1 and baseline test counts/source identity; HIGH in static F2–F5 code gaps; confidence LIMITED for broader TOCTOU behavior until adversarial Windows execution.

---

## Earlier Control Room REWORK record (retained for provenance; not the independent verdict)

# WORKSHOP-COMM-G1-QUALIFICATION-01 — Evidence review and bounded REWORK decision

DATE: 2026-10-30
ROLE: Control Room technical review of actual Worker/CI evidence (NOT final independent acceptance)
VERDICT: REWORK
SOURCE_FROZEN: windows@d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23
EVIDENCE: evidence/WORKSHOP-COMM-G1-WINDOWS-QUALIFICATION-01/WORKER.md
BASELINE_CI_PASS: https://github.com/nevincho/WORKSHOP/actions/runs/41135365108 (25 unit PASS + 6 Windows NTFS PASS; Tkinter process smoke PASS)
NEGATIVE_CI_FAIL: https://github.com/nevincho/WORKSHOP/actions/runs/41136200148 (fenced Markdown field classified as task_candidate, expected inert document)
CODE_SCOPE: apps/workshop_g1/workshop_g1/core.py document_kind() and parse_task(); add focused tests in apps/workshop_g1/tests/test_g1.py.
CLASSIFICATION: IMPLEMENTATION DEFECT / CONTRACT NEGATIVE FIXTURE. Original 31 PASS are genuine but insufficient to prove inert parsing for fenced Markdown. No Windows harness issue in this failure.
CONTRACT: planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md section C requires inert Markdown code samples and no interpretation of task-like content in untrusted documents as machine instruction.
SMALLEST_CORRECTION: deterministic, bounded skip of fenced Markdown code blocks for task-candidate detection and field parsing; support standard backtick and tilde fences, preserve existing canonical plain-text field parsing. Add explicit negative tests for documentation-only fenced TASK_ID, fenced duplicate TASK_ID in otherwise valid task, and tilde fence. No parser redesign, no executor/Git/G2.
PRE_CHANGE_CHECKPOINT: d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23 frozen G1 source. Implementation repair must record exact source commit and rollback method; keep main and other project paths untouched.
VALIDATION: rerun existing 25 unit and 6 Windows fixtures plus new contract negatives on GitHub-hosted Windows runner; record raw logs and source SHA-256. Reviewer must assess updated code/acceptance independently before any COMPLETE.
INDEPENDENCE_LIMIT: This is a negative evidence-based Control Room correction decision, NOT an independent final Reviewer PASS; no G1 promotion authorized.
STOP: return to bounded Worker correction, then fresh independent acceptance review.
