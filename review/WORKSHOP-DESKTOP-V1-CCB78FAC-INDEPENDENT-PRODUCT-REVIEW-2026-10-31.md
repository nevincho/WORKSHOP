# WORKSHOP Desktop V1 — independent product feature review

**VERDICT: FAIL — bounded source corrections required; release acceptance NOT VERIFIED.**

Reviewer role: distinct independent source reviewer; **no implementation edits, merge, or release promotion**.
Frozen source: `ccb78fac75c089a13b39338556fffa497992c836` on `feature/desktop-v1-completion-20261031`.
PR #3 head inspected: `e2b8f87f7aca993c2fc1f947b70ab8f306778860` (two commits after frozen SHA, documentation-only change to the completion matrix; executable source unchanged).
Contract: `planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md`, especially sections 2–7 and 10–11.
Windows CI: [run 41226680018](https://github.com/nevincho/WORKSHOP/actions/runs/41226680018), job `124612176012`.

## Independent evidence

- Read the frozen `engine.py`, `github_api.py`, `gui.py`, `reviewer.py`, `worker.py`, both Desktop test modules, G1 source tree manifest and the V1 contract. Compared PR #3 changes and frozen SHA to the feature base. No changes in the reviewed diff to `apps/workshop_g1/`, `agents/`, `policies/`, `main`, or `windows` were identified; PR remains draft/unmerged. The candidate does modify its isolated Windows CI workflow.
- **Raw Windows CI logs**, not the Worker summary: checkout and `SOURCE_COMMIT=ccb78fac75c089a13b39338556fffa497992c836`; 52 Desktop integration/product tests **OK**, 31 G1 tests **OK**, 6 NTFS tests **OK**, 5 G1 qualification tests **OK** = **94 PASS**. Windows Server 2022 PyInstaller build, frozen-process smoke, Inno installer/uninstall smoke and G1 trust checks completed. The 12-tab test checks tab names/initial state, not user-interactive wizard completion.
- Confirmed bounded positive implementation: 12 named Tkinter tabs; G1 discovery is read-only; plan eligibility checks target HEAD/path; Git-backed bounded settings; plan-hash/HMAC local approval; fixed Markdown-only worker with timeout; separate deterministic preflight; GitHub PR commit/reviewer checks; local `COMPLETE` checkpoint explicitly means **proposal accepted, PR unmerged**.

## Source defects (FAIL)

**D1 — reviewer failure can strand an active task with no supported recovery.** In `engine.py:600–634`, `review()` starts while task is `REVIEW`; a reviewer subprocess timeout/exception, missing `review.json`, malformed JSON or invalid report can raise before persisting any verdict/state transition. `rework()` (`636–659`) requires `REWORK`, while `reject_review()` (`437–455`) requires an existing review record. A partial `review.json` also blocks retry via `REVIEW_REPORT_ALREADY_EXISTS`. This is a concrete error-handling/state-machine dead end, not covered by the 94 passing tests. **Smallest correction:** on all reviewer failure paths persist bounded failure evidence and atomically transition to a recoverable `REWORK` or `BLOCKED` state; handle orphaned partial report safely. Add no-report, malformed-report, timeout and retry/recovery negative tests.

**D2 — human final acceptance is not bound to the exact review receipt displayed.** `gui.py:669–682` fetches a GitHub review receipt and displays its reviewer/commit to the user; after confirmation, `Controller.accept_review()` in `engine.py:717–763` independently fetches another receipt at line 744 without accepting/validating the originally displayed review identity. A different valid reviewer approval can become the selected receipt while the confirmation dialog is open; the persisted checkpoint may then attest a reviewer/review ID the user never approved. This is a final-acceptance TOCTOU defect, even if the PR commit stays unchanged. **Smallest correction:** bind final confirmation to an expected immutable review receipt identity (review ID, reviewer, exact commit, PR, relevant plan/proposal digest) and reject with a re-review-required error if it changes. Add an interleaving test where a new approval arrives during the dialog.

**D3 — conflicting outstanding review requests are not a fail-closed condition.** `github_api.py:186–198` selects the latest state **per reviewer**, then accepts if *any* distinct reviewer has an `APPROVED` entry on the commit. A separate reviewer can have an unresolved `CHANGES_REQUESTED` entry on the same commit and `eligible` remains nonempty. `test_product_completion.py` tests a later change request by the **same** reviewer, not the cross-reviewer conflict. **Smallest correction:** define the explicit multi-reviewer acceptance policy and fail closed on outstanding `CHANGES_REQUESTED` (or verify authoritative GitHub review-decision policy) before local COMPLETE. Add cross-reviewer conflict and resolution tests.

## Release gates (separate from source defects)

**NOT VERIFIED:** real scoped PAT + draft PR + distinct customer reviewer flow; interactive clean Windows 10/11 install, UI, accessibility, credential revocation/uninstall; crash journal and restart at each write boundary; genuine live log streaming; guided first-run wizard; independently verified rollback drill; hostile concurrent NTFS reparse races; commercial security/licensing/customer acceptance. Current GUI Welcome is guided instructions, not a stateful wizard; Run logs are appended after background action completion. Do not conflate 94 automated Windows Server tests with these release gates.

**Disposition:** FAIL for the frozen feature slice and unchanged executable code at PR #3 head. Repair D1–D3 only, rerun bounded negative/integration tests and distinct independent re-review. Keep PR #3 draft; do not merge or claim Desktop V1 COMPLETE. This review branch contains this Markdown assessment only.
