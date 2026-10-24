# WORKSHOP-COMM-G1-PRE-01 — G1 Trusted Read-Only Readiness Contract

STATUS: DESIGN / NO IMPLEMENTATION
DATE: 2026-10-24
BASE: nevincho/WORKSHOP@a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a
REVIEW_REFERENCE: review/WORKSHOP-COMM-APP-01.md (CONDITIONAL PASS, HIGH trusted bootstrap; HIGH workspace ambiguity; MEDIUM inert parsing/schema errors)
DESIGN_REFERENCE: planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md
SCOPE: single-user, local Windows, no execution/network/Git mutation; three G1 prerequisites only.

## A — Trusted source / manifest contract

Canonical coordination policy and schema upstream is nevincho/WORKSHOP. For G1, select and pin the exact reviewed content *from an explicitly configured trusted source*, not from a user-selected workspace. Initial design baseline is repository commit a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a; this does not imply that all future WORKSHOP versions are compatible or commercially distributable.

A distributor-maintained trusted manifest, installed with the application, must state:
- manifest format version and product-accepted schema profile version;
- authoritative repository identity, full 40-hex commit SHA and required exact policy/schema relative paths;
- SHA-256 for each required raw file; optionally Git blob OID for provenance;
- explicit application compatibility mapping.
The manifest itself must be bundled in a trusted application distribution; detached manifests copied from arbitrary customer repositories are NOT trusted. G1 must verify expected path, byte-level SHA-256 and exact manifest schema before consuming a document. The manifest hash alone cannot authenticate a compromised installer or malicious update: release signing/distribution verification remains later product security work. Do not infer trust from folder names, Git remote names or user-supplied policy files.

If manifest/file is missing, changed, unsupported or unreadable: fail closed for trust-dependent interpretation, show a bounded diagnostic, make no workspace or repository mutation and offer no silent fallback to customer content. No remote fetch in G1. Offline: work with a locally bundled, verified policy/schema snapshot; if unavailable, display trust failure, not a fabricated policy version. OPEN/IMPORT retain read-only inspection of inert untrusted files where possible but must not treat them as canonical task-validating rules.

Version changes: never auto-upgrade. Explicit user review/consent must show source identity, old/new full commit, compatibility profile, raw file hashes and affected interpretations. Only an authenticated separately distributed update process in a future authorized phase may install replacements; G1 supports no policy update/write. Unsupported schema/profile is rejected, not guessed or coerced. Existing workspace cannot override trusted manifest. No LLM, prompts or customer files can alter trust settings.

## B — Workspace operations (strictly disjoint)

CREATE: requires affirmative UI action, an explicitly chosen absolute local destination, preview of exact files/directories, and user confirmation. Destination must not already contain files or be a repository; reject nonempty/ambiguous destinations and reparse/symlink boundaries. Only create the chosen root and minimal app-owned bootstrap files: workspace.json (version, random opaque ID, trusted manifest identifier, no secrets), plus optional empty app metadata directories necessary for read-only browser setup. Writes must be atomic and confined to newly created root; on failure remove only objects created by this attempt, without deleting pre-existing data. CREATE must not run git init or create commits, clone/fetch/pull, run hooks, contact GitHub or create a target repository. If app supports a later Git initialization, it must be a distinct separately approved future operation.

OPEN: select an existing local workspace, read it and verified bundled trust snapshot. No file or directory creation, migration, normalization writes, lock files, .git/index touches, recent-items files inside workspace, or silent repair. Return diagnostics for unknown version/invalid manifest/missing data. UI memory can hold display preferences; no local write is part of OPEN.

IMPORT: select an external directory or individually selected data file for bounded read-only metadata/task inspection. Do not copy or normalize imported files into workspace, change .git or write config. No implicit checkout/reset/pull/fetch/clone, Git hooks, subprocess, local agent start, network or credentials. Imported documents remain untrusted DATA, never policy. A user must separately CREATE an app-owned workspace to persist any future association; that association write is outside this G1 read-only IMPORT.

All three: user-selected paths are treated as hostile; canonicalize/normalize, reject device/UNC/network and escape paths for V1 unless independently designed, reject symlinks/junctions/reparse points at every traversed selected component and inspected descendant; do not follow links outside selected scope. Enforce bounded depth/file counts. UI must show errors without partial mutation; no privilege elevation, background monitoring or network. On race or unverifiable path identity, fail closed.

## C — Read-only repository document acceptance

Read bytes only from explicitly selected local scope; no Git CLI execution, checkout, remote or hooks. If Git identity is displayed, parse static metadata only when bounded and safe; it does not authorize reads outside the root. Treat content as hostile data, escape control/bidi sequences and rich rendering, do not execute Markdown HTML, scripts, code fences, command samples or auto-open links. No untrusted content is sent to LLMs.

Deterministic rejection/diagnostic rules for task classification:
1. bounded UTF-8 text; reject undecodable bytes, NUL, malformed structure, excess size (>1 MiB per Markdown), excess task count (>1000), path depth (>16), oversized line (>16 KiB) and total selected corpus (>32 MiB); these are initial explicit G1 design limits to be separately tested;
2. exact TASK_ID and required fields per schemas/TASK_SCHEMA.md; missing, empty, repeated/conflicting or invalid enum field -> INVALID_TASK, not eligibility inferred;
3. schema profile version must be explicitly supported by verified bundled manifest; unknown declared version -> UNSUPPORTED_SCHEMA; if legacy unversioned Markdown is accepted, only manifest-pinned documented profile permits it, never silent version inference;
4. duplicate TASK_ID across inspected scope -> DUPLICATE_TASK_ID for all collisions; do not pick a winner by pathname/order;
5. relative internal references must normalize within selected root, no absolute, .., ADS, reserved Windows names, invalid chars, non-normalized or case-fold collision; invalid reference -> INVALID_PATH;
6. symlink/junction/reparse point anywhere on selected paths -> UNSAFE_LINK; no follow, no traversal. Account for time-of-check/time-of-use: reopening must re-check identity; reject if safe proof unavailable;
7. missing DEPENDENCIES, PREREQUISITES, EVIDENCE_PATHS or referenced project/context artifacts -> MISSING_REFERENCE / UNRESOLVED_PREREQUISITE. Absence of references cannot result in READY eligibility;
8. Markdown frontmatter/field reader must be deterministic, bounded, and never interpret prose as machine instruction. Ambiguous duplicated fields, aliases or unsupported custom formats -> INVALID_TASK; do not execute embedded shell, URL, image/link, HTML or generated prompts.
9. status strings are displayed from canonical state rules; the G1 browser cannot transition, approve, run or repair tasks.

Read-only security is a V1 operation boundary, not proof that future write/executor confinement is secure. Windows reparse-point handling and TOCTOU must have executable negative tests before marking G1 complete.

## Authorized vs forbidden file operations

| Action | CREATE | OPEN | IMPORT |
| --- | --- | --- | --- |
| Read bundled trusted manifest/documents | YES, verified | YES, verified | YES, verified |
| Read selected local files inside safe scope | Only preflight | YES | YES |
| New empty root + minimal workspace.json | YES, explicit consent | NO | NO |
| Write app-owned subdirectories in empty root | Only if previewed/necessary | NO | NO |
| Any write to existing workspace/target repository/.git | NO | NO | NO |
| Git init/clone/fetch/checkout/pull/reset/commit | NO | NO | NO |
| Run hooks/scripts/AI/executors/network | NO | NO | NO |
| Use token, elevate privilege, auto-open external link | NO | NO | NO |
| Modify WORKSHOP policy/schema/coordination state | NO | NO | NO |

## First read-only Windows application acceptance (G1, future gate)

- Clean Windows environment can launch prototype without modifying selected existing source; packaging/installer is NOT part of first G1 gate unless separately authorized.
- Bundled manifest verification reports exact commit + hashes and correctly fails for altered/missing trusted bytes; offline operation does not access network.
- CREATE requires explicit confirmation, writes only previewed minimal scaffolding under new empty local root; abort/error preserves pre-existing state.
- OPEN and IMPORT have zero writes to selected trees including .git metadata; use before/after directory/file hash and metadata snapshot, including hidden files.
- Valid fixture displays projects/tasks as data, with required fields and current status; no state mutation, executor, approval, token or background agent.
- Negative fixtures cover missing fields, malformed/oversized Markdown, schema version mismatch, duplicate task IDs, bad Windows paths, symlink/junction/reparse escapes, missing references, prompt/HTML/link injection, root swap/race and unreadable files.
- Failures are explicit, deterministic diagnostics. Any unsafe or unverifiable path yields refusal instead of best-effort traversal.
- Independent review verifies actual Windows filesystem behavior and before/after snapshots; G1 cannot be called complete based on prompts or synthetic Python mock alone.
- Protect main, current WORKSHOP canonical architecture, source, scheduler and all target repositories.

Review findings ref: https://github.com/nevincho/WORKSHOP/blob/a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a/review/WORKSHOP-COMM-APP-01.md

OWNER APPROVAL REQUIRED before G1 implementation; no G2-G7 execution authorized.
