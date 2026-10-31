# WORKSHOP Desktop V1 — product feature completion matrix

Date: 2026-10-31
Authority: `planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md` and current source.
Branch: `feature/desktop-v1-product-20261031` (isolated from `main` and `windows`).
Scope: bounded deterministic V1, **not** a general-purpose AI coding agent.
This matrix is source inspection, **not** release acceptance.

| V1 contract | Source-grounded implementation | Remaining acceptance/engineering |
| --- | --- | --- |
| Welcome / first-launch workspace wizard | G1 CREATE/OPEN and explicit Git coordination initialization in `gui.py`; strict G1 metadata in adapter | Guided first-launch wizard, configuration validation and client usability tests |
| Connections / GitHub credentials | GitHub tab, fine-grained PAT via Windows Credential Manager, local revoke | Dedicated connection UX; live separate-account auth/revoke test |
| Projects | New read-only project inventory derived from verified coordination Git | Windows GUI interaction and accessibility |
| Task Board | G1 read-only task tree and G2 coordination task tree | Canonical task discovery, prerequisites and project context evaluation beyond fixed plan |
| Task Detail / Scope | New read-only immutable plan, run, preflight review and proposal evidence viewer with identity checks | GUI interaction and long-content rendering |
| Approval Queue | New READY/unapproved queue, exact-plan dialog and SHA-bound approval | GUI interaction and concurrency/race acceptance |
| Executor selection | One fixed `markdown-writer-v1`, no paid network worker | Capability UI and additional safe deterministic executors if required by approved V1 scope; arbitrary coding executor deferred |
| Execution monitor | Run/review tab, subprocess timeout/cancel, log/status output | Live progress, persistent bounded log viewer, restart UX |
| Review and accept/reject | Distinct deterministic reviewer subprocess and new explicit human REJECT transition; remote PR rejection preserves external state and blocks for manual cleanup | Authenticated independent acceptance, explicit accept/COMPLETE gate and evidence/decision binding; deterministic preflight is **not** independent acceptance |
| Checkpoints / recovery | Git coordination history, proposal metadata and explicit interrupted-run recovery | Verified accepted checkpoint, restore UI and crash/restart client matrix |
| Settings | No dedicated settings screen | Explicit workspace/credential/executor/budget/protection settings with safe persistence |
| GitHub proposal | Explicit approval, immutable target SHA, new isolated branch and draft PR, never base merge | Live PAT + PR and remote failure recovery against test account |
| Windows distribution | PyInstaller onedir and Inno Setup, Windows Server CI installer/uninstall smoke | Clean Windows 10/11 user install, UI, credentials and uninstall qualification |

## Verified boundaries

- Existing Desktop integrated Windows CI previously reported 33 Desktop tests, 31 G1 unit tests, 6 NTFS tests and 5 additional G1 qualification tests PASS on Windows Server 2022. This does **not** validate new features on this branch until their own CI completes.
- The V1 worker creates a bounded Markdown artifact. It is **not** a sandbox or general-purpose autonomous programmer.
- A human APPROVE is bound to the exact displayed plan hash. No automatic merge or base-branch writes.
- The new read-only screens and explicit REJECT path must be independently reviewed and tested before acceptance.
- The complete product remains **NOT VERIFIED**; missing V1 features above are genuine product scope, not merely G1 regression issues.

## Windows qualification of the new product feature slice

- Source commit: `fc4dba0b65ead34312de003f4aae9b59220eaefe`.
- GitHub Actions: `41217799839` (Windows Server 2022), conclusion **SUCCESS**.
- Exact tests from raw CI log: 40 Desktop integration, 31 G1 unit, 6 NTFS, 5 G1 qualification = **82 PASS**, no reported FAIL/SKIP in these groups.
- Windows onedir and installer built; frozen GUI process smoke, trusted G1 selftest, frozen Worker/Reviewer, installer/uninstaller and credential cleanup smoke PASS.
- Installer artifact: `WORKSHOPDesktopV1-Installer` from run `41217799839`; **candidate only**.
- This qualifies the new read-only project/detail/approval views, bounded persisted logs and explicit REJECT behavior at unit/integration level. Interactive Windows 10/11 GUI and independent product/security acceptance remain **NOT VERIFIED**.

## Required completion order

Finish safe customer workflow (wizard, connections, project/task eligibility, approval and execution UX), implement an authenticated independent review and human accept/COMPLETE gate, then checkpoint/recovery/settings, integrated Windows security tests, live GitHub test account, clean Windows client acceptance and packaging. Preserve existing G1 and protected policies/agents. No premature release designation.
