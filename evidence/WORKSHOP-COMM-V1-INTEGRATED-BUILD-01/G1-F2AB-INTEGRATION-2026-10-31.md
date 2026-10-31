# WORKSHOP Desktop V1 — isolated G1 CREATE repair integration qualification

DATE: 2026-10-31
ROLE: CONTROL ROOM / BOUNDED INTEGRATION WORKER
STATUS: WINDOWS SERVER CI PASS; INDEPENDENT PRODUCT ACCEPTANCE PENDING
BRANCH: integration/desktop-v1-g1-f2ab-20261031
SOURCE_COMMIT: be653c1ef23d621768a4a8fbc59e388d7234b490
BASE: feature/workshop-desktop-v1-integrated-20261030@5dc59a7f63a5baa8dcd6e23ebff9bf6760f8711c
G1_REPAIR_SOURCE: repair/g1-create-f2ab-20261031@ff3d34b95c77ecfbc1de16e3fe61575e10634197

## Exact scope

Only 5 files changed from the independently reviewed prior integrated candidate: existing G1 core CREATE ownership fix, one isolated qualification harness, integrated CI workflow, GUI G1 CREATE boundary, one GUI regression test. No main/windows, canonical policies, trusted manifest/schemas, agent roles, unrelated repositories or customer workspace changes. PR #2 remains Draft/unmerged.

G1 F2A: ownership identity registered before potentially failing root validation; failure rollback removes owned empty root. G1 F2B: unverified identity exception no longer blindly unlinks potentially foreign replacement; fail closed may preserve an incomplete owned root when identity cannot be proven. Corrected Windows negative injects foreign os.replace after original fd close and asserts bytes at replacement path.

Integrated GUI defect found and minimally repaired: CREATE previously invoked ctrl.initialize() implicitly, creating a Git coordination repository without separate consent, contrary to canonical G1 CREATE. Now CREATE only makes G1 workspace; separate INITIALIZE COORDINATION button requires explicit confirmation. New test asserts no .workshop_v1 after CREATE.

## Exact Windows CI evidence

Run: https://github.com/nevincho/WORKSHOP/actions/runs/41208277504
Job: 124557741977
Runner: GitHub-hosted Windows Server 2022, Python 3.11.9; not a Windows 10/11 customer-client acceptance.

Raw job logs reviewed at exact SOURCE_COMMIT:
- Integrated desktop suite: **33/33 PASS**.
- Existing G1 suite: **31/31 PASS**.
- Actual Windows NTFS fixtures: **6/6 PASS**.
- Additional strict OPEN / ACL / GUI provenance / CREATE fault/race qualification: **5/5 PASS**.
- CREATE_EARLY_ROOT_LEFT_BEHIND=False; CREATE_FOREIGN_REPLACEMENT_SURVIVES=True.
- Frozen GUI process smoke PASS (not interactive UI), frozen G1 trust selftest PASS, frozen Worker/Reviewer smoke PASS.
- Silent installer install/uninstall and credential cleanup on Windows Server: PASS.
- Windows onedir and installer uploaded by CI.

Installer artifact ID: 13044863635; artifact ZIP name WORKSHOPDesktopV1-Installer.
Downloaded ZIP SHA-256: 80e4bc1b67290f997fcab55de6ba63af8e1ea4fa514c4958a594a81c3217e899.
ZIP contains WORKSHOPDesktopV1-Setup.exe (10,549,123 bytes); EXE SHA-256: d0607f8794f2577b0e61507bb762e3207d45bcbbec38401f4521e31adbd9ba4a.
These are Control Room local download hashes, not independent binary-signing attestations.

## Acceptance and protected boundaries

This is a tested **candidate**, not commercial release. Independent G1 F2A/F2B security review and integrated release review have been requested; neither verdict is recorded here. Prior F2–F5 protected-source scope reconciliation is unresolved; do not silently waive. Residual outer rollback identity-check-to-unlink TOCTOU needs independent classification; do not claim atomic deletion. No source promotion, PR merge or G1 COMPLETE checkpoint.

Owner-only remaining evidence: clean Windows 10/11 interactive CREATE/OPEN/IMPORT, trust UI visibility, installer/uninstall and local credential behavior, exact client source/binary identity, real scoped GitHub PAT draft PR in disposable repository, release signing/distribution. General-purpose autonomous coding is not implemented: Worker remains a bounded deterministic Markdown writer.

Next Control Room action: inspect independent reviews; if bounded PASS, arrange client acceptance using this exact installer; if REWORK, implement only independently demonstrated narrow correction, rerun CI, and re-review. Keep branch isolated and PR #2 Draft until gates pass.
