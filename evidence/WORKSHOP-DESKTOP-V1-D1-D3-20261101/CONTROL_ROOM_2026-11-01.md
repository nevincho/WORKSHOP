# WORKSHOP Desktop V1 — Control Room bounded source audit and continuation
DATE: 2026-11-01
STATUS: IMPLEMENTATION CANDIDATE / WINDOWS SERVER 2022 CI PASS / DISTINCT RELEASE REVIEW NOT VERIFIED
ROLE: CONTROL ROOM + IMPLEMENTATION; NOT AN INDEPENDENT REVIEWER
REPOSITORY: nevincho/WORKSHOP
BRANCH: feature/desktop-v1-d1-d3-repair-20261101
PR: https://github.com/nevincho/WORKSHOP/pull/4 (OPEN DRAFT, UNMERGED)
EXECUTABLE_SOURCE_SHA: cac097d69b781843159b5c9474cbabe9ea25ead6
PREVIOUS_SOURCE_SHA: d39385a6a2a3631e3200031eea4b03162c2a4787

## Read-only audit and concrete findings
- Inspected AGENTS.md, AUTONOMY and CONTROL_ROOM_WORKSHOP_CAMPAIGN policies, Desktop V1 spec sections 2/5/6/10/11, Worker evidence, current PR head and exact GitHub source of engine, GitHub adapter, worker, reviewer, vault and tests.
- Verified raw Windows Server 2022 CI job 124859068025 from run 41310296429: source d39385a6; 65 Desktop + 31 G1 + 6 NTFS + 5 G1 qualification = 107 PASS. This does not independently certify the release.
- F4: worker metadata JSON decode/type errors and worker launch OSError were not caught by Controller.run(), leaving durable IN_PROGRESS without normal failure evidence. Bounded correction now records BLOCKED with run evidence and error category. Negative tests added for malformed JSON, non-object JSON and launch OSError.
- F4: Controller.review() accepted a synthetic PASS report with matching SHA and PID but missing required check attestations. Bounded correction now requires exact five reviewer check keys, all strictly True, valid PID and exact evidence SHA; negative forged-PASS test added.
- Initial CI run 41312097971 had 67 tests and one test-expectation mismatch (WORKER_METADATA_INVALID vs WORKER_OUTPUT_INVALID); corrected the expectation to preserve specific failure classification. No production defect inferred from that assertion failure.

## Exact Windows validation
- Workflow: .github/workflows/workshop-v1-integrated-candidate.yml
- Run: https://github.com/nevincho/WORKSHOP/actions/runs/41312301693
- Job: 124865034909; GitHub Actions conclusion SUCCESS; Windows Server 2022, Python 3.11.9.
- Commands: python -B -m compileall -q workshop_desktop main.py tests; python -B -m unittest discover -s tests -v (68 PASS); apps/workshop_g1: python -B -m unittest discover -s tests -v (31 PASS); python -B windows_validation.py (6 PASS); python -B qualification_g1_20261031.py (5 PASS). TOTAL 110 PASS / 0 FAIL.
- Windows onedir PyInstaller build, Inno Setup compile, frozen GUI process smoke (not interactive GUI acceptance), frozen G1 trust verification, worker/reviewer smoke, silent installer/uninstaller smoke and credential cleanup steps completed SUCCESS.
- Artifact: WORKSHOPDesktopV1-Installer, ID 13085666730, ZIP SHA256 7c2fc014c6353ac4e6629127f5279b850cf12ba58b5776aefbcc49323f24e794.
- Artifact: WORKSHOPDesktopV1-Windows-onedir, ID 13085512107, ZIP SHA256 ffe36cc3fdf0eb46c508f98599b39afe93c2ebee567cf6c0d3e8be7d124a4a1e.
- Both are unsigned Windows Server-tested candidates; ZIP artifact SHA is not a binary signing attestation.

## Protection and gates
- Source changes confined to apps/workshop_desktop_v1/workshop_desktop/engine.py and tests/test_product_completion.py; no main/windows merge, G1 production edits, trusted schema, agent or policy modifications.
- A separate authenticated product/security Reviewer has NOT reviewed this new source; this audit must not be relabelled independent PASS. GitHub PR #4 has no APPROVED review at audit time.
- Windows 10/11 clean interactive first-launch, usability/accessibility, actual PAT scope/revocation, two distinct GitHub identities, draft PR/accept/reject, hostile concurrent NTFS/reparse races, release signing/licensing and full client crash-boundary drill: NOT VERIFIED.
- No production COMPLETE, no target merge or deployment. Remote GitHub operations in the customer app were tested with fixtures, not live credentials.

## Next eligible action
Distinct Reviewer: read exact PR #4 diff at cac097d6, source and raw Windows job 124865034909; independently assess D1-D3, worker metadata error state, reviewer report schema, transaction journal/rollback, GitHub authenticated review, installer provenance and repository hygiene. Record explicit PASS/FAIL on immutable source. On FAIL, perform smallest bounded correction and rerun Windows CI. Only after distinct PASS, perform owner-only Windows 10/11 and live two-identity G7 acceptance. Preserve draft PR and rollback; do not infer commercial release from CI.
