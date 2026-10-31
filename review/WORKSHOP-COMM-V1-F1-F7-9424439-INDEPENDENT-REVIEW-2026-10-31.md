# WORKSHOP Desktop V1 F1–F7 — Independent REWORK Review

DATE: 2026-10-31
ROLE: INDEPENDENT REVIEWER — source, test, architecture and security assessment; no implementation
REPOSITORY: nevincho/WORKSHOP
BRANCH: feature/workshop-desktop-v1-integrated-20261030
FROZEN_SOURCE: 94244394981bab26a6ce3f24f057abdd21869796
WORKER_HANDOFF: 8be4a72cc440da2866d68a95e0af80e1dacaff66
PR: https://github.com/nevincho/WORKSHOP/pull/2 (DRAFT)
PRIOR_REVIEW: review/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01.md (FAIL/REWORK)
TASK: tasks/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01.md
WORKER_EVIDENCE: evidence/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01/REWORK_F1_F7_2026-10-31.md
WINDOWS_CI: https://github.com/nevincho/WORKSHOP/actions/runs/41150351069
WINDOWS_JOB: 124385145828
VERDICT: **FAIL / BOUNDED REWORK** — F7 remains incompletely enforced; F1–F6 bounded source corrections materially verified.
PRODUCT_ACCEPTANCE: NOT AUTHORIZED
RELEASE: NOT AUTHORIZED
CHECKPOINT: NOT CREATED

## Evidence and protection

- Independently inspected the corrected `engine.py`, `github_api.py`, `reviewer.py`, `gui.py`, `tests/test_integrated.py`, the prior FAIL review, task, Worker handoff, G1 review, design and bootstrap. GitHub compare `1e2b93a...9424439`: exactly five modified files, all under `apps/workshop_desktop_v1/`; no G1 source, agents, policies, schemas, Control Room or target project edits. `main` remains `484240cddc47c489bc2787c433963e37079589c5`; `windows` remains `d78976812315448973b9d59fe96d2196dbe89c8e`. PR #2 is open and Draft, not merged.
- Independently fetched the GitHub Actions run, job steps and **decoded raw Windows job log**, not only the Worker summary. Exact CI source SHA `94244394981bab26a6ce3f24f057abdd21869796`; event `push`, attempt 1, `success`; Microsoft Windows Server 2022, Python 3.11.9. Log records **30/30 tests PASS, 0 FAIL/SKIP** in 23.856 seconds, Python compile, PyInstaller onedir build, frozen GUI process-alive smoke, frozen G1 trust and worker/reviewer subprocess smoke, Inno Setup installer, Windows Server silent install/uninstall and credential cleanup.
- GitHub artifact metadata independently confirms `WORKSHOPDesktopV1-Windows-onedir` ID `13023150171`, ZIP SHA-256 `b71c650818e7fce15255886344bdc9c3fe3c679ef53ca8c7835f0249c2a4a51a`; `WORKSHOPDesktopV1-Installer` ID `13023095355`, ZIP SHA-256 `948480da93f1687edec2c206b07ed72e623cac5e4f8f583e634a399d8b853df6`. These are runner-upload artifact digests, not independent owner-client binary verification.

## F1–F7 disposition

| Finding | Disposition | Source-level evidence and limitations |
|---|---|---|
| **F1 / lost updates** | **CLOSED for bounded defect** | `CoordinationRepo.transaction(..., *, expected_head)` requires a 40-character HEAD and compares it under the transaction lock before writing (`engine.py:207-225`); plan, approve, run, review, rework, publish and recovery use captured HEAD. Two-controller stale-snapshot negative test passes. Genuine hostile multi-process race not stress-tested. |
| **F2 / ambiguous remote branch POST** | **CLOSED for bounded defect** | `publish()` commits `REMOTE_INTENT` and `PUBLISHING` before remote mutation (`engine.py:478-499`); `propose()` catches ambiguous POST, queries the branch ref, records `PartialProposal`, and checks exact base SHA before file PUT (`github_api.py:90-147`). Error moves task to `BLOCKED`; recovery does not blindly retry. Fake transport timeout/wrong-SHA tests pass; live GitHub failure injection NOT VERIFIED. |
| **F3 / reviewer report link** | **CLOSED for demonstrated pre-existing link overwrite; residual race NOT VERIFIED** | `reviewer.py:11-36` checks stage ancestry/reparse points and uses exclusive `O_EXCL` creation with no-follow where available plus identity checks. Actual Windows file-symlink and junction negatives passed. Concurrent malicious NTFS directory replacement between check/open is not proven safe; do not claim an OS sandbox or hostile-race qualification. |
| **F4 / G1 OPEN writes** | **CLOSED for bounded Desktop sequencing defect** | `gui.py:145-158,160-175,217-223` inspects G1 metadata before attaching, never initializes on OPEN, and exposes separate explicit INITIALIZE. Tests check malformed metadata and interrupted coordination without creation/HEAD mutation. Full byte/metadata snapshots and interactive client OPEN remain release qualification gaps; G1's earlier independent REWORK remains open. |
| **F5 / reviewer authority** | **CLOSED as truthful preflight labeling; product acceptance OPEN** | `engine.py:422-431,459-513` labels deterministic reviewer as `DETERMINISTIC_PREFLIGHT_NOT_INDEPENDENT_ACCEPTANCE`; binds stored report to plan/run/evidence identifiers; draft PR remains canonical `REVIEW`, not `COMPLETE`, and duplicate publish is rejected. Same-user subprocess is NOT an independently authenticated security reviewer; external human acceptance/checkpoint is not implemented/verified. |
| **F6 / REWORK dead end** | **CLOSED for bounded defect** | `engine.py:434-457` allows explicit `REWORK` replan with fresh content hash, clears approval/run/review, and requires a new approval before run. Negative-to-rework-to-PASS test passes. Other `BLOCKED` recovery workflows remain outside this specific closure. |
| **F7 / approval scope** | **FAIL — authorization TOCTOU remains** | `gui.approval_scope()` now shows full bounded Markdown, SHA-256, plan hash and immutable target, and scrollable dialog is present (`gui.py:12-24,265-294`). **But** `gui.py:296-304` displays plan A from `ctrl._plan()`, then calls `ctrl.approve(identifier)` **without passing the displayed plan hash**. `engine.py:335-352` rereads the current plan B and signs it without comparing to what the user saw. A second controller can approve/run/review REWORK/replan the same task while dialog A is open; after user clicks approve, the GUI signs B's new bytes even though A's bytes were displayed. Existing `test_approval_scope_full_payload_and_identity` only checks summary text, not binding between displayed and signed plan. This violates exact-content human authorization and is a source-established interleaving; live GUI reproduction NOT VERIFIED. |

## Smallest correction contract — only F7

1. Capture `displayed_plan_hash = sha256(canonical(displayed_plan))` immediately before presenting the approval dialog. Pass that hash to a mandatory `Controller.approve(identifier, expected_plan_hash=...)` argument (or equivalent immutable approval request object); refuse absent/mismatched hash. The controller must compare the supplied hash against the freshly read current canonical plan **before** creating or signing any approval, then preserve existing `expected_head` optimistic concurrency at commit. Fail closed with `PLAN_CHANGED_REVIEW_AGAIN` on mismatch.
2. Add a deterministic two-controller interleaving test: A displays plan A; B legitimately approves/runs, receives REWORK and replans content B to READY; A confirms old dialog. Assert A cannot sign B and must reopen review. Then assert a newly displayed B can be approved. Also test that unchanged plan approval still works. Prefer a narrow test with a mocked dialog over a broad UI rewrite.
3. Change only `apps/workshop_desktop_v1/workshop_desktop/gui.py`, `engine.py` and targeted tests; retain current F1–F6, G1, policies, agent parameters, main/windows and Draft PR state. Run exact-source consolidated Windows CI and request a distinct independent re-review. No merge or release on green tests alone.

## Release and integration gates (not substitutes for F7)

- G1 canonical independent acceptance remains **REWORK**, including previous source authorization/rollback and clean-client OPEN/CREATE/IMPORT gaps; do not infer G1 COMPLETE from bundled trust smoke.
- Clean Windows 10/11 interactive installer, CREATE/OPEN/IMPORT, plan/approval, run/review, cancellation/recovery and uninstall are **NOT VERIFIED**; hosted Windows Server process-alive checks do not exercise widgets.
- Live fine-grained GitHub PAT permission scope, real draft PR, readback, revocation, remote partial failure and recovery are **NOT VERIFIED**; CI GitHub mutations are fake transport/mocks.
- Adversarial NTFS race testing, durable external-side-effect recovery, commercial distribution/signing and independently authenticated final acceptance/checkpoint remain **NOT VERIFIED**.
- The Worker is a fixed Markdown writer, not a general-purpose coding AI; separate deterministic preflight is not independent engineering review.

**Decision:** FAIL / BOUNDED REWORK, not BLOCKED. Six specific source-level corrections are materially closed, but the user approval still does not cryptographically bind the bytes displayed to the bytes signed. Correct this one authorization gap and re-review the new exact source; keep PR #2 Draft and existing WORKSHOP coordination unchanged. Confidence HIGH for source-level F7 path and CI identity; LIMITED for client UX, live GitHub and hostile filesystem races.
