# WORKSHOP Desktop V1 — Final independent product/security review

TASK_ID: WORKSHOP-DESKTOP-V1-FINAL-INDEPENDENT-REVIEW
DATE: 2026-11-01
ROLE: INDEPENDENT_REVIEWER (read-only product source)
VERDICT: BLOCKED
REPOSITORY: nevincho/WORKSHOP
FROZEN_HEAD: `128936aff778f42b750c5039251ca431bee473ea`
BRANCH: feature/desktop-v1-d1-d3-repair-20261101
PR: https://github.com/nevincho/WORKSHOP/pull/4 (OPEN, DRAFT, UNMERGED)
CI: https://github.com/nevincho/WORKSHOP/actions/runs/41314058862 (SUCCESS, but checkout 466552574b09a47a124003320eb4caaa0c399d4e)
RELEASE: NOT VERIFIED / NOT AUTHORIZED

## Scope and provenance
Directly fetched AGENTS.md, README.md, Desktop V1 specification, integrated build task, frozen engine.py, github_api.py, gui.py, product negative tests, original FAIL report at commit 5a5d33c7, PR #4 changed-file list and patches, and raw CI job log 124870267609. Consulted VALIDATION_POLICY.md. This assessment is not a Windows client-acceptance test or live separate-account test. No implementation file changed.

PR #4 metadata reports head `128936aff778f42b750c5039251ca431bee473ea`, base e2b8f87f7aca993c2fc1f947b70ab8f306778860; 8 changed files, 639 additions and 35 deletions. The frozen commit itself alters evidence/WORKSHOP-DESKTOP-V1-D1-D3-20261101/CONTROL_ROOM_2026-11-01.md only. Raw CI checked out commit 466552574b09a47a124003320eb4caaa0c399d4e, earlier than the frozen commit. Source-equivalence of the final documentation-only commit is supported by the frozen commit file list, but exact-SHA CI execution is not established.

## Prior D1–D3 independent recheck
- D1: engine.py Controller.review() converts missing report, malformed report, subprocess failure and preexisting orphan report into persisted REWORK with review evidence; test_product_completion.py contains corresponding injected failure tests. Code-path correction VERIFIED by inspection; independently executing tests outside CI NOT VERIFIED.
- D2: gui.py accept_review supplies displayed receipt ID, reviewer, reviewed commit and PR URL to Controller.accept_review(); prior UI-to-controller receipt omission corrected in source. Full interleaving GUI acceptance NOT VERIFIED.
- D3: github_api.py verified_independent_review() builds latest per-user decision, refuses unresolved CHANGES_REQUESTED from another reviewer, and requires a different approving identity on exact PR head. Correction verified in source and corresponding negative fixtures; real GitHub multi-account policy behavior NOT VERIFIED.

## Additional bounded implementation observations
- GUI defines 12 tabs: Welcome, Tasks, Projects, Detail, Approvals, Plan, Run, Review, Recovery, GitHub, Evidence, Settings. Presence/function wiring is source-supported; full hands-on usability and interactive workflow are NOT VERIFIED.
- engine.py:97-121 deliberately strips inherited GIT_* control variables, disables hooks and supplies fixed Git settings. 
- engine.py:186-249 journals a limited set of files with pre/post digests and expected HEAD; unknown edits or changed commits fail closed. Tests cover partial commit, foreign content and post-commit journal cleanup. Full crash-boundary matrix / hostile NTFS races NOT VERIFIED.
- engine.py:296-323 journals local transactions before write+commit. engine.py:817 onward journals remote intent before an external proposal and blocks ambiguous remote outcomes; remote cleanup is manual.
- Local COMPLETE is a Git-backed checkpoint recording accepted *unmerged* draft PR, not deployment.
- Scope remains Markdown-only deterministic worker, no arbitrary coding agent or paid inference. Do not advertise a generic autonomous coder as validated.

## Windows CI methodology: verified facts
Raw job log: Windows Server 2022, CPython 3.11.9, checked-out source 466552574b09a47a124003320eb4caaa0c399d4e. GitHub job status SUCCESS. Desktop test suite 70 PASS, G1 tests 31 PASS, NTFS validation 6 PASS and G1 qualification 5 PASS: 112 passing checks according to raw log / recorded suite totals. Compile, PyInstaller onedir, frozen GUI 3-second process-alive smoke, G1 trust selftest, frozen worker/reviewer fixture smoke, installer and silent uninstall with test vault credential cleanup completed. GUI 3-second process alive is *not* interactive GUI acceptance. Simulated GitHub transport is *not* live account approval validation. Windows Server 2022 is *not* clean Windows 10/11 client evidence.

## Indispensable gates preventing unconditional final acceptance
1. Clean Windows 10/11 separate-user install, interactive 12-screen wizard/task lifecycle, credential cleanup and uninstall acceptance: NOT VERIFIED.
2. Live fine-grained PAT scope and revocation; separate GitHub identities; real draft PR + cross-account approval/CHANGES_REQUESTED conflict/rejection and receipt-bound acceptance: NOT VERIFIED.
3. Full process-crash/restart matrix at persistent state boundaries, especially before/after remote side effects; verified rollback drill and hostile concurrent NTFS reparse/path race: NOT VERIFIED.
4. Customer-facing usability/accessibility, legal/license/signing/distribution decisions and independent release approval: NOT VERIFIED.
5. Final frozen SHA exact-run CI: NOT VERIFIED (CI belongs to previous executable-source-equivalent SHA).

## Classification and verdict
BLOCKED — indispensable contractual release acceptance checks require a clean Windows 10/11 client environment and live separate GitHub customer/reviewer accounts, not supplied by this review environment. No independently proven new D1–D3 regression from inspected code. This is *not* PASS, not an implementation-defect FAIL, and not COMMERCIAL RELEASE COMPLETE. Do not merge PR #4. The next bounded action is client and live-account acceptance against the frozen artifact and source identity, then independent review of resulting evidence. No speculative source modifications authorized.
