# WORKSHOP-COMM-V1-INTEGRATED-BUILD-01 — Consolidated Worker evidence

DATE: 2026-10-30
ROLE: WORKSHOP Worker / repository-side implementation
RESULT: INTEGRATED_CANDIDATE_BUILT — REVIEW_REQUIRED, NOT PRODUCT_ACCEPTANCE
TASK: tasks/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01.md
REPOSITORY: nevincho/WORKSHOP
BASELINE: windows@d78976812315448973b9d59fe96d2196dbe89c8e
ISOLATED_BRANCH: feature/workshop-desktop-v1-integrated-20261030
SOURCE_COMMIT: 01ae7a73254566b05a03d428ac16e673f7a4e9e8
SOURCE_TREE: 92426c9f33ad30a004139d986b681d5eac7548fa
SOURCE_PATH: apps/workshop_desktop_v1/
WINDOWS_CI: https://github.com/nevincho/WORKSHOP/actions/runs/41140820256
WINDOWS_CI_JOB: 124354353698
WORKFLOW: .github/workflows/workshop-v1-integrated-candidate.yml

## Delivered integrated candidate

- G1 reuse: existing trusted G1 CREATE and strict OPEN imported without modifying G1 source, schemas or trust manifest.
- G2: local Git-backed coordination state, bounded immutable plans, exact remote SHA, HMAC approvals using Windows Credential Manager, fixed state transitions, audit chain and explicit interrupted-run recovery.
- G3: supervised fixed Markdown writer in a separate process with timeout/cancel and staged output. No arbitrary code, shell, local model or paid API executor.
- G4: distinct deterministic reviewer subprocess checking bytes, SHA-256, path and operation; evidence/checkpoints and separate human draft-PR acceptance. This is NOT an independent human/security review.
- G5: GitHub read-only discovery and optional PAT-backed scoped creation of an isolated proposal branch and draft PR; exact remote content readback before PR; never writes to base branch or merges. Live external account/PAT PR creation NOT VERIFIED.
- G6: integrated Tkinter GUI, G1 task browser, plan/approval, run/review, GitHub credential controls, evidence view; PyInstaller Windows onedir.
- G7: Inno Setup per-user installer and uninstall credential cleanup; local Git for Windows remains a runtime dependency.

## Actual consolidated validation

Windows-hosted GitHub Actions run 41140820256 at exact source commit 01ae7a7; Windows Server 2022, CPython 3.11.9. Raw job logs independently accessible at the run URL. Tests are actual hosted Windows operations, not owner-client execution.

- Python compile: PASS.
- 19/19 consolidated unit/integration/negative tests: PASS, 0 SKIP/FAIL/ERROR. Includes G1 workspace initialization, local Git lifecycle, approval tampering, target SHA changes, path restrictions, staged artifact tampering, interrupted-run recovery, remote content mismatch, real Windows Credential Manager isolated roundtrip and deterministic end-to-end fake-remote draft PR.
- Windows PyInstaller onedir build: PASS.
- Frozen GUI entrypoint alive after 3 seconds: PASS (process smoke, NOT interactive UI acceptance).
- Frozen bundled G1 trust verification: PASS.
- Frozen separate worker and reviewer processes: PASS; FROZEN_REVIEW_VERDICT=PASS.
- Real Inno Setup installer build: PASS.
- Windows Server silent install/uninstall and credential removal: PASS.
- CI artifact WORKSHOPDesktopV1-Windows-onedir: 13018688583, ZIP SHA256 9997dc1ff06192a40251cd72ef6762ad177cd2fd56c0991c4590b65dad8c167a.
- CI artifact WORKSHOPDesktopV1-Installer: 13018453781, ZIP SHA256 8e11dd3556581831d24fa32c0e3212f55aebeb5ce85fe3187555005f684fed15.

## Protection and repository hygiene

GitHub compare baseline to source commit: exactly 14 ADDED files (13 under apps/workshop_desktop_v1/ and one new workflow); no G1 source, trusted schema/manifest, WORKSHOP policies, main branch, target repositories or user workspace modifications. Development commits were consolidated into ONE source commit. Generated caches, installer binaries and transient test outputs are not committed; they are downloadable CI artifacts.

## Exact remaining acceptance gates

1. Independent architecture/security Reviewer of source and raw CI evidence: NOT VERIFIED. No independent Reviewer PASS or validated commercial checkpoint is claimed.
2. G1 canonical independent acceptance remains REWORK from prior review. Owner explicitly authorized integrated candidate work despite the old sequential gate; this does NOT waive G1 release acceptance.
3. Clean Windows 10/11 client interactive GUI and installer/uninstall validation: NOT VERIFIED. Hosted Windows Server is not a client substitute.
4. Live scoped PAT authentication, real separate customer GitHub test repository, draft PR readback and credential revocation: NOT VERIFIED; CI GitHub mutations are mocked.
5. General-purpose coding-agent isolation, AI provider integration, remote rollback of partial API side effects, signing/distribution support and full commercial threat model: NOT IMPLEMENTED / NOT VERIFIED as appropriate. The V1 fixed writer is deliberately bounded.
6. G2–G7 final customer workflow and release acceptance: NOT VERIFIED. No G1–G7 COMPLETE promotion.

## Rollback and next gate

Source baseline is preserved on windows@d789768. The integrated source is isolated in feature/workshop-desktop-v1-integrated-20261030; deleting that branch or closing an unmerged draft PR removes the candidate without touching windows/main. Git rollback does not reverse remote GitHub side effects; this run performed NO live remote proposal write. Next: independent review and Windows 10/11 + customer test-account qualification against the frozen candidate, then explicit human acceptance. No Codex, paid API or Work environment was used.
