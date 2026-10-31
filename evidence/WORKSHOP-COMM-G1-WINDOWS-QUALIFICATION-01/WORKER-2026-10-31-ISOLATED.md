# WORKSHOP G1 — isolated Windows qualification Worker evidence

DATE: 2026-10-31
ROLE: BOUNDED WORKER / NOT INDEPENDENT REVIEWER
REPOSITORY: nevincho/WORKSHOP
BASELINE: windows@d78976812315448973b9d59fe96d2196dbe89c8e
ISOLATED_BRANCH: qualification/g1-windows-f2-f5-20261031
TESTED_SOURCE_COMMIT: cb0d0a187d4342be0c52c928b29473f3bee70de4
CI_RUN: https://github.com/nevincho/WORKSHOP/actions/runs/41202289977
CI_JOB_ID: 124540305748
CI_RESULT: FAILURE — 2 reproduced G1 CREATE acceptance defects
G1_VERDICT: REWORK / NOT COMPLETE
INDEPENDENT_REVIEW: PENDING
CLIENT_WINDOWS_10_11: NOT VERIFIED
CHECKPOINT: NOT CREATED
G2_G7_ACCEPTANCE: NOT AUTHORIZED BY G1

## Source, scope and execution method

Read canonical G1 contract, qualification task, and independent FAIL review at baseline. The separate scope decision is `review/WORKSHOP-COMM-G1-F2-F5-SCOPE-RECONCILIATION-2026-10-31.md`. It finds no explicit retroactive G1 authorization for F2–F5 source changes outside the narrow parser/test repair scope. No production `core.py`, `app.py`, trusted manifest/schemas, existing G1 tests, policies, agents, `windows` or `main` were modified in this campaign.

Added only `apps/workshop_g1/qualification_g1_20261031.py` (isolated, disposable NTFS fixtures), branch-scoped `.github/workflows/workshop-g1-isolated-f2-f5-qualification.yml`, and bounded evidence. CI used GitHub-hosted Windows Server 2022, Python 3.11.9, runner platform string `Windows-10-10.0.20348-SP0` (NT kernel version string; **NOT Windows 10 client**). Raw CI job logs show source commit and runner identity; source tree `git status --porcelain` empty before/after.

Exact commands in CI, working directory `apps/workshop_g1`:
- `python -B -m unittest discover -s tests -v` — **31/31 PASS**.
- `python -B windows_validation.py` — **6/6 PASS** (junction, file symlink, UNC/device, deterministic root swap, CREATE failure rollback, generic OPEN/IMPORT snapshots).
- `python -B qualification_g1_20261031.py` — **5 executed, 3 PASS, 2 FAIL**; zero skip. This is intentionally a **red acceptance gate**, not a green suite. Raw logs are linked above.

## New Windows NTFS evidence — PASS within exact test scope

1. Strict OPEN with `require_metadata=True` checked **valid, missing, malformed, unsupported version and incompatible trusted commit** metadata. Each case yielded the expected diagnostic or empty diagnostics. IMPORT FOLDER remained untrusted generic inspection and did not enforce workspace metadata. For each case, before/after NTFS snapshot digests were identical across OPEN and IMPORT, including hidden `.hidden` and `.git/config` contents and file metadata. This is API-level strict OPEN, not an interactive button click.
2. Windows `icacls` denied read access to a disposable task file; strict OPEN returned `('TASK-LOCK.md', 'UNREADABLE')`. Size and mtime stayed unchanged during refusal. ACL denial was removed and original bytes rechecked identical. No customer path was touched.
3. A real Tkinter root constructed the provenance `TLabel` with the trusted repository identity, full commit and both SHA-256 hashes. `mainloop` was intercepted to inspect widget properties; this **does not prove visual rendering, layout, or a human GUI interaction**.

## Newly reproduced source defects — FAIL

**G1-CREATE-F2A: Early root creation rollback.** `core.create_workspace()` calls `os.mkdir(path)` before `safe_path(path)` and `_path_identity(path)`, but appends the new root to `created` only afterward. Injecting `G1Error('INJECTED_ROOT_VALIDATION_FAILURE')` on the post-mkdir validation left the newly created root present. Raw log: `CREATE_EARLY_ROOT_LEFT_BEHIND=True`, assertion failed. This violates the G1 failure rollback invariant for this deterministic fault. No arbitrary attacker race was required to demonstrate the failure.

**G1-CREATE-F2B: Unverified cleanup deletes a foreign replacement.** After exclusive creation of `workspace.json`, inject an identity-acquisition failure. The exception path closes the file descriptor and calls `workspace.unlink()` **without verifying the object identity**. A deterministic interleaving immediately before that unlink replaces the path with a separate pre-existing sentinel file via `os.replace`; the cleanup deletes that replacement. Raw log: `CREATE_FOREIGN_REPLACEMENT_SURVIVES=False`, assertion failed. This proves unsafe cleanup under a controlled replacement interleaving, **not a demonstrated uncontrolled exploit on a customer machine**.

The two failures correspond to specific source paths `apps/workshop_g1/workshop_g1/core.py` lines 411–414 and 426–432 at the tested baseline. Both were predicted as unqualified paths by the prior independent FAIL review and are now reproduced on actual Windows NTFS.

## Minimal proposed repair — requires separate explicit authorization

Do not change protected production source in this branch without a new bounded authorization. Proposed limited repair in `create_workspace()` only:
- Acquire and retain trustworthy identity/handle of the newly created root as early as possible, before operations that can fail; on early validation failure, remove only an identity-proven owned empty root, otherwise preserve it and report a deterministic fail-closed cleanup diagnostic.
- Remove unconditional `workspace.unlink()` in the identity-exception branch. Compare an identity obtained from the exclusively created file/handle with the current path before cleanup, or refuse deletion when identity cannot be proven; never unlink a foreign replacement.
- Preserve normal CREATE behavior, existing rollback, trust verification, and zero-write OPEN/IMPORT. Add these two exact Windows negatives to the permanent authorized regression suite, plus recovery/foreign-object preservation evidence. Avoid broad refactoring.

## Independent Reviewer handoff

Review exact commit `cb0d0a187d4342be0c52c928b29473f3bee70de4`, raw job logs `41202289977/124540305748`, source and tests, scope decision, and prior FAIL review. Independently classify whether the two deterministic interleavings reproduce G1 contract violations; verify PASS claims against raw logs and inspect `icacls` cleanup. **Do not grant source-change authorization by reviewer fiat**. Return REWORK/BLOCKED until Control Room explicitly authorizes the minimal CREATE fix, then rerun actual Windows NTFS qualification and independent review.

Remaining acceptance gates: Windows 10/11 **client** install/launch and interactive CREATE cancel/confirm, strict OPEN and IMPORT buttons, visible full trust provenance, diagnostics, user-selected workspace snapshots, source/installer identity, and independent security acceptance. Windows Server 2022 widget inspection is not a substitute. Full G1 checkpoint and release approval are prohibited at this stage.

## Rollback and protection

Only this isolated branch contains the new test harness/workflow/evidence. No main/windows merge, no production source change, no G1 COMPLETE checkpoint. Keep raw failed CI run for audit and delete only disposable test fixtures after tests.
