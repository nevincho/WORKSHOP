# WORKSHOP Desktop V1 — Independent F7 final bounded review

DATE: 2026-10-31
ROLE: DISTINCT INDEPENDENT REVIEWER (read-only source/CI inspection; no implementation)
REPOSITORY: nevincho/WORKSHOP
BRANCH: feature/workshop-desktop-v1-integrated-20261030
EXACT_SOURCE: 8370455cface8692b268c5ea3b41d93535658dee
EVIDENCE_HANDOFF: dad627fe3484191907b1ca715a184647f5f3b425
PR: https://github.com/nevincho/WORKSHOP/pull/2 (OPEN / DRAFT)
PRIOR_INDEPENDENT_FAIL: review/WORKSHOP-COMM-V1-F1-F7-9424439-INDEPENDENT-REVIEW-2026-10-31.md
CI: https://github.com/nevincho/WORKSHOP/actions/runs/41153896255
CI_JOB: 124396341096

**VERDICT: PASS — F7 BOUNDED AUTHORIZATION CORRECTION ONLY.**
**INTEGRATED RELEASE/PRODUCT ACCEPTANCE: NOT AUTHORIZED.**

## Independently inspected evidence

1. Read prior independent FAIL report and exact-source `engine.py`, `gui.py`, `tests/test_integrated.py` from GitHub at commit `8370455c`; compared source parent `f522fb4c` to `8370455c`: **one source commit, only three files modified**, all under `apps/workshop_desktop_v1/` (engine 7+/2-, GUI 5+/2-, tests 74+/11-). Compared source to evidence handoff `dad627fe`: **only one Markdown evidence file modified**, no subsequent implementation changes.
2. GUI `approval_scope(plan)` includes complete proposed Markdown, content SHA-256, canonical plan SHA-256, immutable target SHA, repository/ref/path, executor and maximum cost. `Desktop.approve()` captures **identifier and `digest(canonical(plan))` before opening** the modal approval dialog; after confirmation it passes both to `Controller.approve(identifier, expected_plan_hash=...)`.
3. Controller `approve` requires keyword-only `expected_plan_hash`, rereads the current plan with `_plan`, checks that the supplied digest is lowercase 64-hex and matches current canonical plan with `hmac.compare_digest`; mismatch rejects with `PLAN_CHANGED_REVIEW_AGAIN` **before signing or storing an approval**. It also preserves READY status, remote target SHA and `expected_head` optimistic-concurrency transaction checks. The digest binds the plan's ID, content and target fields; `_plan` checks stored state plan hash.
4. New `test_approval_requires_exact_displayed_plan_hash`: omitted hash raises TypeError; wrong hash is rejected without approval or signing secret; matching hash succeeds. New `test_approval_dialog_rejects_replan_during_display`: while A's GUI dialog is open, second controller approves/runs/reviews as REWORK and replans B; stale A confirmation raises `PLAN_CHANGED_REVIEW_AGAIN`, leaves coordination HEAD/state unchanged, stores no approval, blocks execution and creates no remote proposal; fresh B display is approved. This is a **deterministic mocked-dialog interleaving**, not an interactive GUI race/hostile multi-process stress test.
5. Independently retrieved GitHub Actions run **41153896255**, job **124396341096**, and **decoded raw Windows job log** (not just Worker handoff). Exact checkout/`SOURCE_COMMIT` = `8370455cface8692b268c5ea3b41d93535658dee`; event push, attempt 1, completed success; runner Windows Server 2022 / Python 3.11.9. Log shows both F7 tests `... ok`, **`Ran 32 tests in 20.919s` / `OK`**, no failure/skip. Compile, PyInstaller onedir, frozen GUI process-alive smoke, G1 trust check, frozen worker/reviewer smoke, Inno Setup build, and silent installer/uninstaller + credential cleanup succeeded. This does **not** constitute interactive Windows 10/11 client validation.
6. Workflow artifacts independently read: `WORKSHOPDesktopV1-Windows-onedir` ID 13024730891, ZIP digest `sha256:1459291be676e2cf564984fcf5372e1cdb37341348479bdf69a3ad7209dbb49f`; `WORKSHOPDesktopV1-Installer` ID 13024511425, ZIP digest `sha256:dfd41dd82f567750ff513e8f59b5d59069758f943a3e38588c86166d5651f70d`. Runner artifact metadata, not independently downloaded client-binary SHA verification.
7. F1–F6 previously assessed as bounded PASS in prior independent report; the final source diff changes no F1–F6 implementation paths except the approval API call contract and its tests. Raw CI includes passing stale-controller, ambiguous remote intent, reviewer symlink/junction, G1 OPEN, preflight/reviewer semantics and REWORK tests. No evidence of regression within this test scope. Protected G1 source, agents, policies, schemas, Control Room and `main`/`windows` are untouched by F7 source and handoff commits. Independently observed `main` at `484240cddc47c489bc2787c433963e37079589c5`, `windows` at `d78976812315448973b9d59fe96d2196dbe89c8e`; PR #2 remains Draft, unmerged.

## Finding and scope

The previously proven F7 TOCTOU defect (GUI displayed plan A but Controller could sign reworked plan B) is **closed at source level** by an explicit displayed-plan digest argument, fresh Controller comparison and HEAD-constrained commit. The specific negative interleaving and unchanged-plan positive path are demonstrated by exact-source Windows tests. **F7: PASS (HIGH confidence for bounded source/test path).** No broader refactor warranted.

This PASS is **not** an independent product/security acceptance, general-purpose coding agent approval, authenticated human reviewer implementation, or permission to merge or release.

## Remaining release gates — NOT VERIFIED / OPEN

- Canonical G1 independent acceptance remains separate (prior REWORK/BLOCKED evidence): validate G1 source authorization, rollback and clean-client CREATE/OPEN/IMPORT; do not infer acceptance from frozen trust smoke.
- Real clean Windows 10/11 interactive GUI, approval/replan race, CREATE/OPEN/IMPORT, cancellation/recovery, install/uninstall, accessibility and client artifact SHA verification.
- Live least-privilege GitHub PAT: branch/PR creation, readback, credential revocation, partial failure, recovery, duplicate suppression and remote idempotence. CI remote adapter tests use fakes.
- Adversarial NTFS directory-replacement/reparse races, genuine concurrent multi-process stress, durable external-side-effect recovery.
- Separately authenticated independent human security/product acceptance, final checkpoint, signing and commercial distribution.
- The fixed worker is a bounded Markdown writer; deterministic separate-process preflight is not independent acceptance.

**Decision:** Accept F7 bounded correction and preserve F1–F6 dispositions; keep PR #2 Draft and do not mark integrated Desktop V1 COMPLETE, merge, or release. Proceed to independent G1 gate and clean-client/live integration qualifications. No implementation files were modified by this review.
