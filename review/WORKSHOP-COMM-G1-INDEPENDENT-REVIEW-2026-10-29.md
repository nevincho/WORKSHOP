# WORKSHOP-COMM-G1-01 — Independent Architecture, Code and Security Review

DATE: 2026-10-29
ROLE: Independent reviewer (read-only GitHub source inspection; not original implementation coordinator)
VERDICT: BLOCKED
COMPLETION: NOT AUTHORIZED
REPOSITORY: nevincho/WORKSHOP
BRANCH: windows
FROZEN_IMPLEMENTATION: 99723cfea33201c10b1a60eb3520bfc504321bf0
SCOPE: Exact frozen commit, canonical G1 readiness contract, source and tests, owner-reported Windows evidence. No implementation/policy edits.

## Evidence provenance and limitations

- Independently fetched at the frozen commit: planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md; apps/workshop_g1/{README.md,main.py,tests/test_g1.py,workshop_g1/{__init__.py,app.py,core.py,trusted/{manifest.json,TASK_SCHEMA.md,STATE_MACHINE.md}}}; evidence/WORKSHOP-COMM-G1-WINDOWS-EXECUTION-2026-10-29.md; source-manifest handoff and task document.
- Independent GitHub compare 0274eaac323381e7140527e3579f68a141b1fc14...99723cfea33201c10b1a60eb3520bfc504321bf0: nine new source files, G1 evidence and one task-file modification; no pre-existing canonical policy or production code path appears in this compare. Frozen commit is ancestor of windows; branch was one handoff-only commit ahead at review time.
- The original ZIP SHA-256 values are reported by the coordinator in evidence/WORKSHOP-COMM-G1-SOURCE-MANIFEST-REVIEW-HANDOFF.md. Independently recalculating all nine original ZIP hashes is NOT VERIFIED because original attachment bytes were not accessed by this review. Blob SHAs seen in GitHub are Git object IDs, not a substitute for raw SHA-256 comparison.
- apps/workshop_g1/windows_validation.py does not exist at frozen commit (GitHub 404), consistent with supplemental Windows harness being distributed separately. Its exact code, fixtures and test methodology are NOT VERIFIED.
- Windows log 17 tests: 15 PASS / 2 SKIP; standalone qualification: 3 PASS / 1 SKIP; aggregate 18 owner-reported PASS, 3 owner-reported SKIP, 0 owner-reported FAIL. Independent test reproduction: 0. No actual Windows runtime or NTFS fixture executed by this reviewer. Owner logs are evidence of reported execution, not independent qualification.
- Manifest embeds repository nevincho/WORKSHOP, pinned commit a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a, and SHA-256 strings for TASK_SCHEMA.md and STATE_MACHINE.md. verified_trust() checks specified fields and hashes but does not strictly reject unknown manifest keys, and the manifest format does not explicitly list relative paths and application compatibility mappings as demanded by the readiness contract.

## Static architecture/security review

1. TRUST — PARTIAL: verifying two bundled document hashes and failing on missing/modified files is implemented. Manifest exact schema, compatibility mapping and distributor trust authentication are not independently proven. The bundle is trusted only by its location in application code; distribution authenticity is a future security boundary, not a G1 installer acceptance criterion.
2. CREATE — PARTIAL: GUI shows destination and preview text and requires affirmative confirmation; implementation only creates workspace.json and tasks/. There is no atomic create/commit protocol; failures and races around mkdir/write/rollback are not shown safe. mkdir occurs after a check-then-use gap, and rollback is best-effort. Parent and leaf link checks are path-based.
3. OPEN/IMPORT — PARTIAL: no intentional workspace write path in inspect_workspace(); no Git/subprocess/network invocation visible in app/core. Independently observed Windows before/after snapshots, including .git hidden files and metadata, are NOT VERIFIED. IMPORT selects directories only, not an individual file.
4. PATH — BLOCKER: safe_path lstat checks pathname components and Windows FILE_ATTRIBUTE_REPARSE_POINT; read_limited rechecks metadata of pathname before/after opening. This is not descriptor-based race-safe confinement. Between lstat and open, a hostile pathname can be swapped; same path check is not a strong identity guarantee for the opened handle. Complete Windows device path/UNC/reparse/TOCTOU adversarial coverage is NOT VERIFIED.
5. PARSER — BLOCKER: parse_task checks nonempty required fields and enums, but doesn't validate reference semantics or schema profile against manifest during task parsing; accepts unversioned tasks without explicit proof of a documented legacy profile; ignores unsupported unknown field aliases except repeats of exact names. inspect_workspace scans only direct tasks/ children and does not verify referenced project/context artifacts, dependencies, prerequisites or EVIDENCE_PATHS. Marked READY values are shown raw with no eligibility qualification. A missing task-like file containing no TASK_ID is classified as legacy rather than validated. Invalid tasks are listed as diagnostics, but colliding duplicate IDs still remain in returned tasks.
6. UNTRUSTED INPUT — PARTIAL: Tkinter Treeview and Text display data without Markdown/HTML execution; no LLM, network or agent execution is present. Tests that merely assert an injected string survives parsing are not a comprehensive UI safety or bidi/control escaping qualification.
7. TEST SUITE — PARTIAL: base suite contains unconditional skip for the Windows reparse test; available tests do not qualify all contract negative fixtures, source-to-zip provenance, adversarial TOCTOU or Windows execution. The separately reported real junction PASS only covers that fixture, not every reparse/path race.
8. PROTECTED SCOPE — PASS for GitHub compare of frozen candidate against stated base: changed paths are new G1 app/evidence plus the G1 task record; canonical policy files are not changed. Does not imply an independent runtime write audit.

## Exact unresolved G1 acceptance requirements

A. Independently verify exact nine-file raw SHA-256 identity against original ZIP and preserve independently inspectable Windows harness and fixtures.
B. Independently run on clean Windows and record executable/version, commands, test logs, GUI launch and before/after selected-tree snapshots (content + metadata + hidden .git entries) for OPEN/IMPORT and failure/abort CREATE.
C. Test actual Windows file symlink and directory junction/reparse escapes, root-swap/TOCTOU adversarial substitutions, device/UNC paths and unreadable entries, and demonstrate fail-closed refusal without outside-root read/write; replace unsafe behaviour only under separately authorized implementation work.
D. Enforce and test explicit supported profile/manifest compatibility, strict manifest schema, exact required hashes/paths, and altered/missing trust failure without untrusted fallback.
E. Resolve and diagnose missing/invalid DEPENDENCIES, PREREQUISITES, EVIDENCE_PATHS, referenced project/context artifacts, invalid relative references and case-fold collisions; do not misrepresent unchecked READY status as eligibility.
F. Demonstrate parser negative coverage for malformed/oversized Markdown, unsupported schemas, duplicate/colliding task IDs, injection, control/bidi display handling, Windows path anomalies and unreadable files.
G. Demonstrate CREATE atomicity, race/refusal behavior and rollback of exactly new objects, while preserving existing files.
H. Meet or explicitly re-scope the individual-file IMPORT selection requirement in the canonical contract. This review does not authorize re-scoping.
I. Complete independent Windows qualification, acceptance review and validated checkpoint before any COMPLETE promotion.

## Decision

BLOCKED, not PASS. No independent Windows reproduction occurred, and code-level canonical acceptance gaps remain. This does not contradict the owner-reported 18 PASS/3 SKIP; it identifies acceptance objectives those tests did not independently establish. Preserve G1 as not complete; do not authorize G2 or modify production, policies or main. Any repair requires separate owner-authorized bounded scope. STOP after this review.
