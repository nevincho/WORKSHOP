# WORKSHOP Desktop V1 — bounded Worker evidence and independent Reviewer handoff

DATE: 2026-11-01
ROLE: WORKER / CONTROL ROOM IMPLEMENTATION (NOT INDEPENDENT REVIEW)
VERDICT: IMPLEMENTATION CANDIDATE — WINDOWS SERVER 2022 CI PASS; INDEPENDENT RELEASE REVIEW NOT VERIFIED
SOURCE_SHA: cd7da6223df495ed9300f65e8175a6e655d10d7b
SOURCE_BASE: feature/desktop-v1-completion-20261031@e2b8f87f7aca993c2fc1f947b70ab8f306778860
ISOLATED_BRANCH: feature/desktop-v1-d1-d3-repair-20261101
DRAFT_PR: https://github.com/nevincho/WORKSHOP/pull/4 (unmerged)
PREVIOUS_FAIL: review/WORKSHOP-DESKTOP-V1-CCB78FAC-INDEPENDENT-PRODUCT-REVIEW-2026-10-31.md @ 5a5d33c7a28ead919635f1809f3ce2a714ea3212

## Actual code changes
- D1: reviewer subprocess timeout/failure, absent or malformed report now produce durable REWORK evidence and permit explicit replan/reapproval. Missing report, malformed report and timeout negative tests added.
- D2: controller requires the exact displayed GitHub review ID, reviewer identity, reviewed commit and PR URL; mismatches fail closed without COMPLETE checkpoint. GUI passes the immutable receipt after explicit confirmation.
- D3: unresolved CHANGES_REQUESTED from any distinct reviewer vetoes acceptance despite a different reviewer's APPROVED. Resolution and conflict negative tests added.
- Recovery: local Git transaction journal with expected HEAD and before/after file digests; explicit bounded rollback or committed-state reconciliation, no replay of worker or remote writes; injected commit failure, foreign edit and post-commit cleanup tests.
- Execution Monitor: bounded progress/partial-output callback from supervised worker to GUI; no arbitrary command executor.
- First launch: step-gated workspace/coordination/settings/optional GitHub navigation without implicit writes; Windows Tkinter wizard test.
- Recovery tab: explicit transaction-journal recovery button. Existing G1 code, policies, agents, trusted schemas, main and windows not changed.

## Reproducible Windows CI
GitHub Actions run: https://github.com/nevincho/WORKSHOP/actions/runs/41309990415
Runner: Windows Server 2022, Python 3.11.9; source checkout exact SHA above.
Commands: python -B -m compileall -q workshop_desktop main.py tests;
python -B -m unittest discover -s tests -v (64 PASS);
from apps/workshop_g1: python -B -m unittest discover -s tests -v (31 PASS);
python -B windows_validation.py (6 PASS);
python -B qualification_g1_20261031.py (5 PASS).
TOTAL: 106 PASS, 0 FAIL in these suites. Frozen GUI process smoke, G1 trust selftest, frozen worker/reviewer smoke, PyInstaller onedir, Inno Setup installer and Windows Server silent install/uninstall/credential cleanup all PASS.

Artifacts: WORKSHOPDesktopV1-Installer, artifact ID 13085216454, ZIP SHA256 4f165387fab6b2539b97c646b9379f76e7577f8ca6a5879ba663419312434a3f;
WORKSHOPDesktopV1-Windows-onedir, artifact ID 13084124043, ZIP SHA256 5ea92e1ada6599a088e28d55019cacca0cc26894903bef41ca2eda16a4c6fe46.
These are unsigned tester candidates, not commercial release binaries.

## Required distinct Reviewer work
Read actual PR #4 diff, source at cd7da6223d and raw run 41309990415 logs; assess D1 failure-state coverage, D2 exact-receipt TOCTOU, D3 cross-reviewer conflict policy, journal recovery trust boundary, progress callback and wizard. Independently rerun security/negative tests and record PASS/FAIL on exact source. This document is Worker evidence, NOT independent Reviewer PASS.

## Remaining release gates
- Distinct independent product/security Reviewer: NOT VERIFIED.
- Live fine-grained GitHub PAT, draft PR, separate-account review/accept/reject and remote cleanup: NOT VERIFIED.
- Clean Windows 10/11 interactive install, accessibility, credential lifecycle and restart/crash boundary matrix: NOT VERIFIED.
- Hostile concurrent NTFS/reparse races, signed commercial distribution and customer acceptance: NOT VERIFIED.
- No main/windows merge, no remote proposal merge/deployment, no production COMPLETE.
