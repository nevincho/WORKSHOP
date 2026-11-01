# WORKSHOP G1 — Independent F2A/F2B security and acceptance review

DATE: 2026-10-31
ROLE: DISTINCT INDEPENDENT REVIEWER; REVIEW-ONLY WRITE
REPOSITORY: nevincho/WORKSHOP
BRANCH: repair/g1-create-f2ab-20261031
EXACT SOURCE/TEST SHA: ff3d34b95c77ecfbc1de16e3fe61575e10634197
WORKER HANDOFF SHA: fa198ae48a10e920bb55e9fb6baf5ebc04fd5831 (evidence only)
BASELINE: 1af2bd1f3d03a6adf71be7e9691080953fcd0d74
VERDICT: REWORK FOR CANONICAL G1 SECURITY ACCEPTANCE; F2A/F2B NAMED REPAIR CASES CLOSED
G1_COMPLETE: NO
CHECKPOINT / MERGE / G2 PROMOTION: NOT AUTHORIZED

## Independently inspected evidence

Read `AGENTS.md`, Reviewer and validation/human-gate policies, `planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md`, `tasks/WORKSHOP-COMM-G1-QUALIFICATION-01.md`, previous independent FAIL `review/WORKSHOP-COMM-G1-CANDIDATE-660d7edf-INDEPENDENT-REVIEW-2026-10-30.md`, `review/WORKSHOP-COMM-G1-F2-F5-SCOPE-RECONCILIATION-2026-10-31.md`, Worker handoff `evidence/WORKSHOP-COMM-G1-WINDOWS-QUALIFICATION-01/F2AB-REPAIR-2026-10-31.md`, exact source and qualification test, and isolated workflow. GitHub compare `1af2bd1f3...ff3d34b95` is one commit ahead, zero behind, changing only `apps/workshop_g1/workshop_g1/core.py` (6+/5-), `apps/workshop_g1/qualification_g1_20261031.py` (13+/11-) and the isolated workflow branch trigger (1+). No production app, policy, schema, manifest, main/windows branch or unrelated source change in this bounded diff.

Raw GitHub Actions [run 41208053129](https://github.com/nevincho/WORKSHOP/actions/runs/41208053129), job `124557116919`, attempt 1: `head_sha=ff3d34b95c77ecfbc1de16e3fe61575e10634197`, completed SUCCESS on GitHub-hosted **Windows Server 2022**, `RUNNER_IMAGE=win22 20261026.347.1`, NT `10.0.20348`, Python 3.11.9. Raw job log (not just Worker summary): 31/31 unit PASS, 6/6 Windows NTFS PASS, 5/5 isolated qualification PASS; no reported FAIL, ERROR or SKIP; post-test Git status empty. Runner SHA-256: `core.py=05A46F91E76D40659E662EAB8E93239205ED68042A825B6F4471F10A4C95ADFA`; `qualification_g1_20261031.py=6A3801405BD28543903FB99007C5D2F9C20149F601CA38E4B9321B825A38448D`. This is Windows Server evidence, **not Windows 10/11 client acceptance**.

## Narrow F2 findings

**F2A — CLOSED for reproduced early-root-validation failure (high confidence).** Immediately after exclusive `os.mkdir(path)`, `create_workspace` now obtains root identity and appends `(path, identity, False)` to `created` *before* `safe_path(path)`. The Windows fault-injection fixture raises on `safe_path(dest)`, asserts the new root is gone and the parent's snapshot unchanged; raw log `CREATE_EARLY_ROOT_LEFT_BEHIND=False`. This closes the demonstrated gap, not every possible race between `mkdir` and identity acquisition.

**F2B — CLOSED for demonstrated unconditional unverified unlink (high confidence).** On failure of `_path_identity(workspace)`, the inner handler now closes the exclusive file descriptor and re-raises; it no longer invokes `workspace.unlink()`. The revised fixture calls real `os.replace(foreign, workspace)` after the fd closes, then verifies `workspace.read_bytes()==b'FOREIGN_OBJECT_MUST_SURVIVE'`. This is the correct **destination pathname** after a move. The previous assertion `foreign.exists()` was a **test-harness defect**, not evidence that the source fix failed. Raw log `CREATE_FOREIGN_REPLACEMENT_SURVIVES=True`. The fail-closed choice may strand an owned incomplete root/file if identity cannot be proved; that is safer than deleting unverified foreign data, but is not full rollback completeness.

## Remaining source-level security issue and acceptance decision

**R1 — OUTER ROLLBACK PATHNAME TOCTOU: OPEN, CANONICAL G1 ACCEPTANCE BLOCKER.** The outer exception handler still does `if _path_identity(item) == identity: item.unlink() if is_file else item.rmdir()`. `_path_identity` opens/checks/closes a Windows handle; the subsequent pathname deletion is a separate operation. Another process can replace the pathname *after* the check and *before* unlink/rmdir. A matching prior identity therefore does **not** bind deletion to the object checked. This non-atomic sequence is directly verified in source; successful exploitation under a genuine concurrent Windows adversary is **NOT VERIFIED** by this CI. It is a credible foreign-object deletion risk, not a proven executed attack. Nevertheless canonical G1 contract B expressly requires CREATE rollback to remove **only attempt-owned objects**, preserve pre-existing/foreign data, and fail closed on race or unverifiable identity. The implementation cannot establish that invariant for outer rollback; thus 42 green tests do not justify unconditional G1 PASS. Do not reclassify the corrected F2B test as coverage of R1.

**R2 — PRIOR F2–F5 SOURCE-SCOPE RECONCILIATION: OPEN.** Earlier `windows` branch F2–F5 changes in `core.py` and `app.py` exceeded the original qualification task's narrowly authorized fenced-Markdown-only mutation. The separate reconciliation report found no retroactive authorization. The new F2A/F2B authorization does not waive those earlier scope deviations. Control Room must explicitly accept/reject the previous source scope before canonical promotion; independent Reviewer cannot grant retroactive permission.

**R3 — G1 CLIENT/RELEASE GATES: NOT VERIFIED.** Current CI does support strict OPEN/IMPORT no-write NTFS snapshots (valid/missing/malformed/version/trust), ACL denial/recovery, junction/symlink and bounded GUI provenance-widget construction. It does **not** prove actual Windows 10/11 client interactive CREATE/OPEN/IMPORT, visible provenance and error handling, owner-local distribution identity or client UI acceptance. The G1 first gate does **not** require G2–G7, packaging, live PAT or product release; do not use later-phase gates as substitutes for G1 criteria.

## Smallest correction contract to Control Room

1. **Separate, expressly authorized R1-only source correction**: make rollback deletion identity-bound to the *same* verified filesystem object on Windows (or refuse deletion where this cannot be guaranteed); preserve owned-object cleanup for the already-passing F2A/fsync cases. Do not rely on a second pathname check or sleep. Add a deterministic Windows negative that swaps a foreign file/empty directory **between the final identity check and actual deletion**, verifies the foreign object at its replacement pathname survives byte-for-byte, and confirms unchanged external tree. A handle-bound disposition is one candidate, subject to exact Windows semantics and compatibility verification; no broad redesign.
2. Run the existing 31+6+5 suites and the new adversarial negative on a frozen exact source SHA; independently inspect raw logs. Preserve source rollback commit and untouched protected files.
3. Resolve the separate F2–F5 authorization discrepancy with an explicit Control Room decision, then obtain the G1-specific Windows 10/11 client GUI/NTFS acceptance evidence before a final canonical G1 review. No checkpoint/merge/COMPLETE/G2 authorization on this verdict.

REVIEW METHOD: direct GitHub source/diff/contract/fixture inspection and decoded raw Windows Actions job logs; no independent local Windows client execution, no source/test/policy/schema edits. Confidence HIGH for F2A/F2B narrow closure and non-atomic rollback source pattern; LIMITED for adversarial exploitability and client GUI. Previous FAIL remains historical evidence, not overwritten.
