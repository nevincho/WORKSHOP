# WORKSHOP-COMM-APP-01 — Independent Architecture & Security Review

Date: 2026-10-24
Repository: nevincho/WORKSHOP
Reviewed commit / verified branch HEAD before review: 64b6dc4afc0bed5a9b9db10dc394ce25e0cb1741
Branch: workshop-comm-port-01-simulation
RESULT: CONDITIONAL PASS
Scope: Architecture and security design review for G1 only; no implementation, test execution, or production qualification.

## Sources and authority
Reviewed planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md; tasks/WORKSHOP-COMM-APP-01.md and WORKSHOP-COMM-PORT-01.md; checkpoints/WORKSHOP-COMM-PORT-01.md; review/WORKSHOP-COMM-PORT-01.md; README.md; AGENTS.md; schemas/TASK_SCHEMA.md and STATE_MACHINE.md; and applicable AUTONOMY, VALIDATION, HUMAN_GATE, REPOSITORY_COMMUNICATION, CHECKPOINT_AND_BACKUP and REPOSITORY_HYGIENE policies at the pinned commit.
GitHub compare confirmed branch HEAD identical to the candidate before this review. PORT-01 PASS covers 12 synthetic simulation tests only; neither real portability nor hardened controller security was demonstrated.

## Architecture verdict
Tkinter/ttk is an appropriate low-dependency Windows-first implementation for a one-window read-only browser. Use clear GUI -> ApplicationService -> read-only repository/schema interfaces, with no executor/control-plane mutation path exposed by G1. Git remains authoritative for coordination; an in-memory index is non-authoritative. Keep the G1 component footprint limited to workspace bootstrap/open, pinned document loading, schema interpretation, task/project presentation and diagnostics. No need for SQLite authority, scheduler, subprocess worker, GitHub token store, approval ledger or reviewer process in G1.
The proposed broader controller/executor/reviewer/checkpoint boundaries are directionally coherent but design-only and must be separately qualified before G2-G7. Existing Markdown policies/schemas are not by themselves a complete typed configuration/runtime model. State labels must reflect canonical source exactly; never imply the GUI can authorize arbitrary state transitions.
Packaging via PyInstaller onedir is reasonable later, but Windows build, signing, installer, commercial distribution and license validation are NOT VERIFIED and are not G1 coding prerequisites.

## Security findings and severity
- HIGH — G1 trust bootstrap is insufficiently specified: a user-selected repository cannot be allowed to redefine authoritative policy/schema identity merely by providing similarly named files. Define the trusted source, exact pinned commit/object identities, permitted offline cache behaviour and unsupported-schema refusal before implementation. User-supplied Markdown/task text is data, never executable instructions.
- HIGH — G1 workspace creation/open semantics are ambiguous against “no repository changes without explicit user action”. Define explicit create/import/open choices, destination/path consent, exact allowed local writes and clear non-destructive behaviour. Opening/inspecting existing repositories must not implicitly checkout, pull, fetch, reset, initialize, install hooks, run Git aliases or scripts, or write to protected/target repos.
- HIGH (gated for later executable/write capabilities) — subprocess confinement on Windows cannot be inferred from cwd or path allowlists; job/process-tree controls and OS privilege boundary require validation before G3.
- HIGH (gated for later write capabilities) — symlink/junction/reparse escape, repository boundary and TOCTOU checks need proven enforcement before any write/executor operation. G1 should avoid following untrusted paths outside selected read scope and perform no repo mutation.
- HIGH (gated for later Git writes) — branch/commit substitution, changed HEAD and concurrent writers require immutable commit/object verification and expected-HEAD write preconditions before G2/G5 write flows.
- HIGH (gated for later GitHub connectivity) — GitHub least-privilege authentication, revocation and Windows Credential Manager handling are design intent, not a validated adapter. G1 requires no token.
- HIGH (gated for later execution) — human approval identity, plan/scope/commit/cost binding, replay and expiry; paid executor hard denial; independent reviewer identity; evidence authenticity; tamper-resistant audit log are unimplemented and must be demonstrated before affected capabilities. SHA-only event chaining is insufficient against privileged rewriting.
- HIGH (gated for later execution) — interrupted execution reconciliation, journal atomicity, idempotency and rollback of external side effects are unresolved; do not use PORT-01 restart readback as crash-safety evidence.
- MEDIUM — G1 malformed Markdown, malicious repository content and prompt-injection payloads must remain inert display data, be escaped in UI, bounded in size/depth and handled with explicit parse errors. Do not hand untrusted content to an LLM or execute embedded links/commands automatically.
- MEDIUM — G1 schema completeness: required fields, unknown versions, missing prerequisites, duplicate task IDs and cross-document references need deterministic diagnostics, not guessed eligibility; no canonical state mutation.
- LOW — Defer GUI styling sophistication, installer choice, market pricing, code signing and complex modularization until usability/build evidence justifies them.

## Mandatory corrections/prerequisites before G1
1. Record a minimal trusted-source manifest/bootstrap contract: canonical repository/ref and exact schema/policy commit, trusted bundled-or-verified content rules, update/migration policy, offline/read-only behaviour and rejection of unsupported versions. Do not interpret arbitrary user repository instructions as trusted policy.
2. Define G1 operations precisely: explicit user-confirmed local workspace creation is the only allowed initializer write; existing workspace open/import/browse defaults read-only; no implicit Git network, hooks, subprocess execution or target-repo write; distinguish local directory scaffolding from committing/pushing a Git repository.
3. Specify G1 parser and boundary acceptance checks: robust missing/invalid-schema diagnostics, strictly inert task content, path canonicalization/reparse safety for reading, no elevation, no tokens, no task transitions, no repository mutation on browse. Verify with malicious and malformed fixture cases before claiming G1 complete.
These are small scoped design clarifications, not a demand to implement G2-G7 security features first. G1 coding is contingent on owner authorization and the above interface/acceptance clarification.

## G1 implementation readiness
CONDITIONAL: suitable as the first bounded implementation after the three G1-specific corrections. No implementation is authorized by this review. No reason to introduce Qt, Electron, Tauri, SQLite authority, AI executors, API billing or a scheduler for G1. Keep any Git reading via verified read-only object access; Git CLI is not intrinsically side-effect free and must be constrained/tested if used.

## Deferred requirements
G2 canonical transition enforcement and immutable approvals; G3 Windows worker isolation and execution budgets; G4 genuine independent reviewer and recoverable checkpoint proof; G5 authenticated GitHub scoped writes, ref race and credential control; G6 packaging/distribution; G7 clean Windows/customer-account integration and interruption/security testing. Each requires its own implementation/review gate; do not infer readiness from this verdict.

## Scope protection and evidence limits
Review only, no Desktop source, test run, code change, canonical mutation, task status change, controller action, main change or next-phase activation. Repository hygiene: review produces one necessary permanent evidence artifact; no disposable outputs.
NEXT_STEP: STOP — OWNER APPROVAL REQUIRED.
