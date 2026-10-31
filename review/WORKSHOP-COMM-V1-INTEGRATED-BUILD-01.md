# WORKSHOP-COMM-V1-INTEGRATED-BUILD-01 — Independent architecture, code and security review

DATE: 2026-10-30
ROLE: INDEPENDENT REVIEWER (read-only source/evidence assessment; no Worker implementation)
REPOSITORY: nevincho/WORKSHOP
BASE: windows@d78976812315448973b9d59fe96d2196dbe89c8e
FROZEN_SOURCE: 01ae7a73254566b05a03d428ac16e673f7a4e9e8
HANDOFF: f7ec11d3148ebd1e34304b37b005a6628ca0911b
BRANCH: feature/workshop-desktop-v1-integrated-20261030
PR: https://github.com/nevincho/WORKSHOP/pull/2 (DRAFT)
TASK: tasks/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01.md
WORKER_EVIDENCE: evidence/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01/WORKER.md
CI: https://github.com/nevincho/WORKSHOP/actions/runs/41140820256
CI_JOB: 124354353698
VERDICT: FAIL / REWORK — INTEGRATED CANDIDATE NOT QUALIFIED
RELEASE: NOT AUTHORIZED
CHECKPOINT: NOT CREATED

## Verified implementation and validation

- Compared exact source commit to the specified baseline: **one commit, 14 added files** (13 in `apps/workshop_desktop_v1/`, one CI workflow); **no changes to G1 source, policies, schemas, Control Room state, main or windows** in this source commit. PR #2 remains open and Draft, not merged. Repository hygiene of the added source is satisfactory: no generated binary/cache/report dump committed.
- Inspected the entire new Python controller, GUI, G1 adapter, worker, reviewer, GitHub client, vault, tests, build script, installer and workflow, plus bootstrap/policies, Desktop V1 design, task and prior G1 independent review.
- Independently fetched GitHub Actions run metadata, job steps and **decoded raw job log**, not only the Worker summary. Exact CI source SHA is `01ae7a7...`, event `push`, run attempt 1, result `success`, runner **Windows Server 2022**, Python 3.11.9. Raw log shows **19/19 PASS, 0 SKIP/FAIL**, PyInstaller onedir build, 3-second frozen process smoke, bundled G1 trust self-test, frozen worker/reviewer smoke, Inno Setup 6.7.1 build and silent install/uninstall with credential cleanup on the hosted runner.
- CI artifacts: onedir ID `13018688583`, runner-upload ZIP SHA-256 `9997dc1ff06192a40251cd72ef6762ad177cd2fd56c0991c4590b65dad8c167a`; installer ID `13018453781`, runner-upload ZIP SHA-256 `8e11dd3556581831d24fa32c0e3212f55aebeb5ce85fe3187555005f684fed15`. These are runner-produced digests, not independently downloaded client binaries.
- G2 local Git coordination, HMAC approval, G3 fixed Markdown subprocess, G4 deterministic subprocess checker, G5 scoped draft-PR adapter, G6 Tkinter GUI and G7 installer are **present in source**. The fixed worker is **not** a general-purpose coding agent or OS sandbox. G4 subprocess is **not** the independent engineering/security Reviewer required for product acceptance.

## Defects requiring bounded rework

**F1 — HIGH / INTEGRITY: lost-update race in canonical local state.** `engine.py:204-223` accepts `expected_head=None` in `CoordinationRepo.transaction()`; the Controller's plan, approve, run, review, publish and recovery call sites do not pass an expected HEAD captured with the state snapshot. The lock serializes only the write, not read/modify/write. Two controllers can both read the same clean state and commit sequentially; the second can silently overwrite the first controller's task/status. This violates the design's optimistic-concurrency requirement. **Required:** bind every state mutation to the previously read Git HEAD, reject stale updates, and test two independently instantiated controllers interleaved at the read/commit boundary. Static path VERIFIED; concurrent exploit not run on a Windows client.

**F2 — HIGH / REMOTE SIDE EFFECT: uncertain branch creation is not journaled.** `github_api.py:90-105` performs POST `/git/refs` **outside** the `try` that converts later failures into `PartialProposal`. A timeout/connection loss after GitHub creates the branch can escape as `GitHubError`; `engine.py:424-434` catches only `PartialProposal`. The task remains REVIEW, with no persisted partial-remote record and a potentially orphaned branch. This contradicts the required external-side-effect reconciliation and safe retry semantics. **Required:** record intent/branch identity before the first remote write, handle ambiguous POST outcomes, inspect remote ref after error, persist BLOCKED/uncertain state and never blindly retry. Test server-success/client-timeout at branch creation; verify exact proposal branch SHA before PR creation. Static path VERIFIED; live GitHub failure not reproduced.

**F3 — HIGH / FILESYSTEM: reviewer report follows an untrusted link.** `engine.py:376-402` passes `staging/<run>/review.json` to `reviewer.py:10-25`; the reviewer uses `Path(report_file).write_text(...)` without exclusive creation or link/reparse validation. If another process plants a symlink/reparse target at that path, the reviewer can overwrite an out-of-stage file under the user's rights. The existing symlink test covers only the workspace root, not staging/report output. **Required:** exclusive no-follow/identity-checked creation of review output inside a verified stage root, reject pre-existing or reparse-point paths, and add Windows symlink/junction negative tests. This is a source-established path-following defect; hostile Windows race exploit NOT VERIFIED.

**F4 — HIGH / G1 BOUNDARY: OPEN may write before strict G1 validation.** `gui.py:127-151,170-177` calls `ctrl.initialize()` (creates `.workshop_v1/coordination` and Git commits) during **OPEN WORKSPACE** when coordination does not yet exist, after a consent dialog but **before** `inspect_workspace(...,require_metadata=True)` in `refresh()`. Thus OPEN can modify even a malformed/untrusted selected directory, contradicting G1 strict read-only OPEN semantics. **Required:** perform strict G1 validation before any coordination mutation; separate read-only OPEN from an explicitly named coordination INITIALIZE action; assert byte/metadata snapshots unchanged for OPEN, including invalid metadata and refusal. Do not alter protected G1 code to solve a Desktop UI sequencing defect.

**F5 — MEDIUM / REVIEW AUTHORITY: process separation is not independent authenticated review.** `reviewer.py:10-27` is deterministic and executes as the same local OS user/package; `engine.py:389-395` treats a reported PID different from the worker PID as identity separation. PID inequality does not authenticate the reviewer or independently attest source/evidence. `engine.py:439-445` marks task COMPLETE on draft-PR creation, which must not be presented as canonical engineering acceptance. **Required:** label this as deterministic preflight only; bind review result to immutable plan/run/evidence and authenticated reviewer identity or explicitly retain HUMAN/independent review as the acceptance gate. Clarify status semantics: submitted draft PR is not a merged/accepted target change. No assertion that the current subprocess provides a security boundary.

**F6 — MEDIUM / WORKFLOW: REWORK is a terminal trap.** `engine.py:397-403` can set status `REWORK`, but `run()` accepts only `READY` (`engine.py:335-338`), while `plan()` refuses a new task if any task is `REWORK` (`engine.py:262-265`). No correction/replan/abandon transition exists. **Required:** implement a bounded, explicitly approved REVIEW→REWORK→IN_PROGRESS repair route or safe close/replan path with evidence; add a test that reaches REWORK and subsequently proceeds without rewriting Git state by hand.

**F7 — MEDIUM / APPROVAL UX: exact proposed bytes are not displayed for human approval.** `gui.py:217-232` displays task/repo/ref/path/executor/byte count, but neither content nor its hash/diff. HMAC binds the plan technically, but the human cannot inspect the exact payload being authorized from this confirmation. **Required:** show full bounded Markdown content (≤16 KiB), SHA-256 and immutable target identity in a reviewable confirmation before signing, with a test of the displayed approval scope.

## Scope, evidence gaps and release gates

- **G1 remains unaccepted:** prior independent review `review/WORKSHOP-COMM-G1-CANDIDATE-660d7edf-INDEPENDENT-REVIEW-2026-10-30.md` found G1 REWORK. Reusing its source and passing a frozen trust self-test does not close its earlier F2/F3/F5/Windows-client acceptance gaps.
- **Windows client:** Windows Server 2022 CI is real and valuable, but clean Windows 10/11 interactive CREATE/OPEN/IMPORT, plan/approve/run/review, install/uninstall, cancellation and recovery are **NOT VERIFIED**. A 3-second GUI process-alive check is not a UI interaction test.
- **GitHub:** adapter tests use fake transport/FakeGitHub; real fine-grained PAT scope, private/public repository access, draft PR creation/readback, permissions failure, revocation and external rollback are **NOT VERIFIED**.
- **Security:** HMAC tampering, path allowlist and one symlink-root test passed, but adversarial NTFS reparse races, local coordination history rewrite resistance, crash between atomic file writes and Git commit, and remote partial-failure reconciliation are **NOT VERIFIED**. Local Git SHA-chain is not a tamper-proof audit store.
- **Release/distribution:** no clean-client installer identity, code signing or commercial release qualification. No general-purpose AI coding agent is implemented; this is a task-scoped deterministic writer, consistent with the task's permitted bounded executor, not a substitute for the eventual broader product vision.

## Decision and smallest correction contract

**FAIL / REWORK**, not BLOCKED: F1–F4 are specific source-level design/implementation defects, independent of unavailable Windows client hardware; F5–F7 are scope/authority/workflow gaps. Correct **only** the new `apps/workshop_desktop_v1/` candidate and its targeted tests in the isolated branch, with one consolidated Windows CI run; preserve existing G1, main/windows, canonical policies, agent parameters and unrelated projects. Prioritize F1 (state concurrency), F2 (remote uncertainty), F3 (staging link safety), F4 (read-only OPEN), then F5–F7. Re-review the new exact source commit and raw logs; separately qualify G1 and clean Windows 10/11 + live test GitHub before release acceptance. Do not merge PR #2, create a validated product checkpoint or promote G1–G7 COMPLETE on this evidence.

ROLLBACK: close unmerged Draft PR #2 / discard isolated candidate branch after preserving this review; baseline `windows@d789768...` is untouched by the candidate. Git rollback cannot undo remote side effects; the reviewed CI used mocks and performed no live GitHub proposal mutation.

METHOD: direct GitHub source/blob comparison, all new source/tests/build/installer/workflow inspection, applicable policies and prior G1 review, CI run/job metadata and raw decoded job logs. No local Windows client execution, no live GitHub PAT write, no implementation modifications. Confidence HIGH for source defects, exact CI identity and test outcomes; LIMITED for exploitability under hostile Windows races and client UX.
