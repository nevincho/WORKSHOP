# WORKSHOP Desktop V1 — Implementation-Ready Product Design (NO IMPLEMENTATION)

PROJECT: WORKSHOP COMMERCIAL EDITION
TASK_ID: WORKSHOP-COMM-APP-01
DATE: 2026-10-24
STATUS: DESIGN CANDIDATE / NOT INDEPENDENTLY REVIEWED
SCOPE: Windows-first, local-first, one user, one bounded task at a time, explicit human authorization.
REPOSITORY_BASELINE: WORKSHOP main 484240cddc47c489bc2787c433963e37079589c5.
SIMULATION_REFERENCE: PORT-01 0d248fad2aa48ce28d073b489447a63a08bae207; independent synthetic PASS at e0861b3b0de1bbfddc16645cdf36ab06f1e10ba4.
TANGRA: EXCLUDED. CODEX/WORK/PAID_API EXECUTION DURING DESIGN: NONE.

## 1. Authority, facts, assumptions and design constraints

Facts:
- WORKSHOP README and policies designate WORKSHOP Git as coordination authority, target project repo/runtime as implementation authority; chat transcripts are non-authoritative.
- Existing roles are Markdown instructions, not independently running local processes.
- Task, state-machine, queue, checkpoint and review schemas exist in Markdown.
- PORT-01 is a standard-library synthetic demonstration, not hardened production controller. It uses an untrusted caller-supplied approval boolean, no credential identity and file allowlist without symlink protection; chained hashes are not cryptographic authenticity.
- Scheduler is external automation in status/WORKSHOP_STATE.yaml and recorded as unstable. staging/github-cron-controller is inactive, 869 commits behind main when compared during campaign. Do not merge directly.
- Existing target-specific handoffs and test source are NOT generic Desktop app code.
- WORKSHOP repository does not provide a Desktop installer or production executor implementation.

Assumptions requiring validation:
- Customer has an authorized local Windows session and internet for GitHub (offline local viewing possible).
- V1 accepts repositories selected by user and created WORKSHOP coordination workspace; no implicit target-repo writes.
- Single user, one outstanding task, local scheduler disabled by default.
- User can supply a deterministic local worker; AI provider integration is optional until authenticated/permission-bounded.

## 2. Customer workflow and UX

Install -> first-launch workspace wizard -> choose/create WORKSHOP coordination Git repo -> connect GitHub (scoped authorization) -> choose target repo (read-only by default) -> configure executor (deterministic local / explicitly opted-in provider) -> draft bounded task -> policy validation -> review requested operations/cost -> human approve -> run once -> live local logs/evidence -> distinct Reviewer -> accept/reject change proposal -> checkpoint/rollback reference -> next task only on new approval.

Beginner screens: Welcome & Workspace; Connections; Projects; Task Board; Task Detail / Scope; Approval Queue; Execution Monitor; Review; Checkpoints/Recovery; Settings.
Advanced panels: policy provenance/versions, task schema, executor capabilities, raw evidence, commit identities, audit chain, budget limits, protected paths, permission details.
UX statuses: READY, IN_PROGRESS, REVIEW, REWORK, COMPLETE, BLOCKED, HOLD, HUMAN_GATE exactly map from canonical state machine. Never expose a button to force arbitrary transition.

## 3. V1 architecture and trust boundaries

Single packaged desktop process with separate controller service class and subprocess execution boundary (NOT a network service).

GUI -> ApplicationService -> Policy/Schema Adapter -> Deterministic Controller -> RepoStore (WORKSHOP Git workspace) -> GitHubAuthAdapter/RepositoryClient
                                          |-> ApprovalLedger -> ExecutorRouter -> SupervisedWorkerProcess -> EvidenceStore
                                          |-> ReviewCoordinator -> independent reviewer instance (separate execution identity)
                                          |-> CheckpointManager -> Git refs + verified artifacts.

- UI is untrusted request surface and cannot write canonical state directly.
- Python controller is the sole state-transition and approval-verification authority, enforcing the documented canonical rules. Existing PORT-01 simulator informs behavior but cannot be copied as a production security implementation without changes.
- Git working tree + commit object IDs hold coordination truth. In-memory cache is disposable; no authoritative competing SQLite state in V1. Temporary transactional journal permitted for crash recovery, reconciled to Git.
- Target repos are separately mounted/checked-out from WORKSHOP coordination store. No writes to target without per-task explicit scoped approval and independently verified target ref.
- Separate execution sandbox/worktree with default-deny writable roots; arbitrary customer command execution is dangerous. OS process sandboxing on Windows requires a verified method before claiming containment; allowlisted paths alone are not a sandbox.
- No background scheduling, external listeners or hidden autonomy by default. Scheduled work becomes separate later gated capability.

## 4. Configuration contract (not active code)

Workspace config must have schema version, opaque workspace ID, Git coordination URL/ref and commit, explicit target project repo IDs/refs, repository read/write permissions, protected glob/path set, executor ID/mode/command + capabilities, max elapsed time/resource limits, cost ceiling and approval requirement, reviewer identity policy, evidence directory and rollback mode. No secrets within Git or exported YAML.
Credential identifiers only reference Windows Credential Manager entries; no plaintext tokens in config/logs.
Migration must be explicit and reversible. Reject unsupported version rather than silently upgrading or mutating canon.
Policies and schemas are version-pinned at workspace creation; update only by user-approved migration with diff and checkpoint.
All data paths normalized/resolved and compared against canonical workspace roots and symlinks/reparse points; repo branch/ref and immutable commit identity verified before mutation.

## 5. Feature implementation classification

| Feature | Reuse | Additional engineering |
| --- | --- | --- |
| Local app launch | None | GUI/bootstrap, settings and error handling |
| Create/open WORKSHOP workspace | README registry, schemas | initializer, schema/version loader, Git adapter |
| Connect GitHub | registry concepts only | GitHub App device flow or scoped fine-grained PAT adapter, OS credential vault |
| Project/task views | task/state schema | parser/index, validation, visual UI |
| Prerequisites and scope checks | policies, task schema | deterministic parser and protected path enforcement |
| Executor selection | routing policy + PORT-01 mock | adapter interface, capability/mode validation, subprocess boundary |
| Approval | HUMAN_GATE_POLICY | durable signed/attributed local approval record bound to task hash, commit and executor |
| Run one bounded task | PORT-01 synthetic semantics | real controller, cancellation, subprocess supervisor, timeout, logs |
| Evidence and logs | evidence paths/report schema | safe capture, redaction, content hashes |
| Independent review | role/review policy | distinct reviewer invocation and identity, review of immutable diff/evidence |
| Accept/reject | state schema, checkpoint policy | merge-free proposal/patch or PR gate, explicit human decision, rollback verification |
| Recovery | checkpoint schema; PORT-01 restart reload | transactional atomic writes, crash journal, safe resume/reconcile |

No component above except policy/state schema is currently qualified as customer-ready software.

## 6. Explicit controller interfaces (design only)

Workspace.open(config) -> verified workspace identity, policy/schema version and Git HEAD.
Task.discover(project) -> canonical task ID/ref plus content hash.
Task.evaluate(id, snapshot) -> eligibility, exact missing prerequisites, protected paths, allowed executor set.
Approval.request(plan_hash, repo_heads, executor_id, operations, max_cost, expiry) -> pending approval.
Approval.commit(authenticated_user, plan_hash) -> immutable approval ID; must reject changed plan/ref, replay, expiry.
Executor.plan(task, worktree, permissions) -> declared I/O capability + cost estimator.
Executor.run(approval_id, timeout, cancel_token) -> structured run ID and event/evidence records; zero-cost mode must be enforceable.
Reviewer.review(frozen_commit, evidence_hashes, acceptance) -> signed/attributed verdict; same run identity cannot review itself.
Checkpoint.record(review_id, implementation_ref, verified_rollback) -> checkpoint ID.
Controller.transition(task_id, from, to, attestations) -> canonical rules only.
Recovery.reconcile(event_log, Git ref, workspace journal) -> known state or BLOCKED, never guessed COMPLETE.
All state writes use expected HEAD/content hash (optimistic concurrency) to avoid lost updates.

## 7. Security and failure model

A. Authorization: GitHub token least privilege per repo; read-only until user approves exact write operations. Use GitHub App installation scope when supportable; fine-grained PAT may be V1 fallback with explicit expiration/revocation. GitHub App OAuth device flow documented; registration and customer UX remain unimplemented.
B. Credentials: Windows Credential Manager (CredRead/CredWrite), DPAPI fallback if justified; no repo/git config plaintext, no secrets in subprocess argv, logs or crash dumps. Access-token revocation and logout UI required.
C. Filesystem: disallow absolute/parent traversal, symbolic links/reparse point escape, unsafe rename/copy, protected paths; verify both workspace and target repo roots before/after operations. Run commands in restricted working directory with separate temporary worktree and OS-enforced user rights if execution risk requires; if confinement unavailable do not offer arbitrary code execution as 'safe'.
D. Approvals: approval bound to immutable task, exact target Git commit, diff/intended file set, executable identity, upper cost budget, time bound; missing or altered scope invalidates approval; approval provenance includes local OS user plus durable event.
E. Budget: advisory token forecast is not enforcement. Real no-paid mode requires network/provider disabled or disallowlist plus no available paid credentials; cost ceiling requires an adapter that can stop requests by checked usage before limit and cannot guarantee final post-billed total unless provider exposes authoritative limits. Paid connector must be explicitly opted in.
F. Worker: timeout/cancel process group, bounded stdout/stderr, OS resource budget where available, kill child processes; cancellation does not imply remote action rollback. Idempotency keys and at-least-once recovery needed for crashes.
G. Reviewer: separate authenticated reviewer invocation, no self-review; check hash/commit/diff and actual test evidence; user final acceptance remains distinct.
H. Audit: append-only at the application permission boundary, hash linking plus signed/ref-protected storage where required; SHA-only chaining doesn't stop privileged rewrite. Redact secrets.
I. Rollback: record baseline commit, exact proposed commit, restore method, external side effects. Git reset alone cannot reverse external API/hardware effects. Never promise universal rollback.
J. Interrupted execution: reconcile journal, Git HEAD, evidence and run status; orphaned runs become REVIEW_REQUIRED/BLOCKED rather than silently resumed; simulate crash points before release.
K. Threats explicitly in scope: compromised repository prompt content, malicious task instructions, token leakage, symlink traversal, branch substitution, destructive commands, review spoofing, paid escalation, tampered evidence.

## 8. Provider and cost compatibility (research as of 2026-10-24)

- ChatGPT website subscription: separate from OpenAI API billing; no assumption that website membership gives third-party Python application API capacity. Do not automate consumer chat UI.
- OpenAI API: documented programming interface; usage charges accrue to customer's platform account, separate credentials and billing; optional opt-in only.
- Codex ChatGPT/app/CLI: plan access subject to current terms and caps; not the same thing as arbitrary third-party hosted orchestration entitlement. Codex SDK and app-server are documented integration surfaces, but commercial usage/auth rights must be checked for proposed distribution. Do not implicitly bundle Codex as free API.
- Other AI APIs: design provider adapter only after validating official terms, auth, rate limits and price for each provider. None enabled for design or V1 default.
- Local AI: optional subprocess/HTTP localhost model adapter, zero per-token cloud charge but disk, power, model license, model install and device constraints apply. No assumed model quality.
- Deterministic Python subprocess worker: no paid AI service required; local electricity/hardware and potential GitHub/network costs still apply.
- GitHub: free account may support core repo use subject to current plan/rate/action limits; workflow minutes and private project limits can have costs. V1 must not require Actions.
- Windows app: no mandatory SaaS/server. Commercial code-signing certificate and distribution support may have seller-side cost. Dependence on GitHub connectivity only for remote operations; offline view/local operations possible.

Sources to reverify before implementation/distribution:
https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform
https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
https://learn.chatgpt.com/docs/codex-sdk
https://learn.chatgpt.com/docs/app-server
https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps
https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

## 9. Windows UI, build and packaging tradeoff

Option A — Tkinter/ttk (recommended smallest V1): included in standard Python, built-in cross-platform widgets, simple standard dialogs, no Electron/Node runtime. Downsides: more effort for highly polished UI and complex tables/workspace tooling. Suitable for one-window task/approval workflow.
Option B — PySide6 Qt Widgets (alternative if UI acceptance proves Tkinter insufficient): stronger table/docking accessibility potential but larger distribution and Qt LGPL/GPL/commercial obligations; verify legal compliance especially static/dynamic linking/replacement requirements, not legal advice.
Option C — Tauri + Python backend: additional Rust/JS toolchains, interprocess/native bridge and updater surface; not minimal for initial Python-first product.
Option D — Electron + Python backend: broad web UI ecosystem but Chromium/Node bundle and multiple runtimes make size, updates and attack surface larger.

Initial packaging recommendation: PyInstaller Windows onedir with pinned Python/dependencies for reproducible tests and support; optional installer after qualification (WiX/Inno Setup subject to current licensing evaluation). Onefile only after onedir acceptance. Do not claim .exe created.
Python built-in tkinter docs: https://docs.python.org/3/library/tkinter.html
PySide6 licensing docs: https://doc.qt.io/qtforpython-6
PyInstaller operating modes: https://pyinstaller.org/en/stable/operating-mode.html
PyInstaller license: https://github.com/pyinstaller/pyinstaller/blob/develop/doc/license.rst
Windows credential storage: https://learn.microsoft.com/en-us/windows/win32/secbp/handling-passwords

## 10. Minimal implementation sequencing (future work, not authorized by this design)

G0: verify install/license/credential architecture and replay test against frozen canonical schema, independent review.
G1: safe Git-backed workspace initializer, policy-version pin and read-only task browser; no executor.
G2: deterministic controller transitions with immutable approvals and event journal; comprehensive negative and crash tests.
G3: isolated deterministic local task executor with cancellation/timeouts, evidence/logging, no network paid access.
G4: genuinely separate Reviewer with source/diff/evidence checking; accepted checkpoint + rollback exercise.
G5: scoped GitHub authentication and read-only -> controlled write with reviewed PR path; real separate customer test account.
G6: Tkinter UX/wizard integrated to verified service interfaces; packaging/installer, signing decision, accessibility/security QA.
G7: fresh Windows machine/user install and end-to-end human-approved customer task, external GitHub account, restart/recovery and uninstall without credentials left behind.

Order may change based on verified dependencies; do not parallelize implementation across unproved interfaces.
For V1, "real bounded engineering task" must be constrained to a deterministic, explicit allowlisted fixture task with independently checked repository diff. Arbitrary coding agents must be a separate phase after stronger execution sandbox/security qualification.

## 11. Acceptance criteria for first sale candidate

A. Clean Windows VM installs application without developer Python; uninstall removes binaries and offers local data preservation/deletion.
B. New customer account initializes separate WORKSHOP repo, no owner secrets/data/chat; live GitHub authorization and revocation tested.
C. User opens target repo read-only, approves explicit bounded test change, runs deterministic worker, sees evidence, independently reviews, accepts/rejects via approved Git proposal flow.
D. Canonical READY -> IN_PROGRESS -> REVIEW -> COMPLETE trace, human gate held, unauthorized transitions refused.
E. Missing credential, protected path, malicious task and paid-escalation tests demonstrate hard denial (not just prompt refusal).
F. Crash/restart at each persistent state boundary and before/after repo write does not fabricate COMPLETE or lose known-good checkpoint.
G. Hash/identity of source, task, executor, reviewer, evidence, approval and checkpoint traceable.
H. One rollback drill reestablishes the recorded baseline for repository-only effects; external side effects clearly excluded.
I. No external API billed without explicit customer opt-in and verified cost display; free mode has no paid connectors enabled.
J. No production/TANGRA modifications and no mandatory background services.
K. Independent security/review gate, legal licenses review, usability test with novice customer, rollback and support documentation.
All above are release goals, not validated present capabilities.

## 12. Pricing/product packaging hypothesis (unvalidated market assumptions)

WORKSHOP Desktop Free: local workspace/task browsing, synthetic/demo deterministic workflow, manual review and repository inspection; no automatic paid inference.
WORKSHOP Desktop Pro (one-off license candidate): supervised bounded task execution, richer project/review/checkpoint experience, configurable optional provider adapters, export/audit; external provider/API usage billed separately by respective vendors.
Team/Business deferred: shared approver roles, enterprise credential governance, policy-enforced remote workers, multi-user scheduling; requires separate security and architecture scope.
Avoid selling “autonomous AI engineers” before actual operational evidence. Product promise: auditable, human-approved engineering workflow coordinator.
Business assumptions NOT VERIFIED: customer willingness to pay, price, support workload, commercial license eligibility, app-update signing costs. Conduct user interviews and maintenance cost model before price selection.

## 13. Readiness verdict and unresolved decisions

DESIGN READINESS: implementation-oriented draft, NOT independently reviewed.
IMPLEMENTATION READINESS: CONDITIONAL / NOT AUTHORIZED.
PORTABILITY: synthetic account-neutral model verified; real external account integration NOT VERIFIED.
Most important gates: hardened controller/approval enforcement, separate Reviewer, credential/host isolation, Git concurrency and rollback, real GitHub authentication, packaging/tested Windows install, source licenses.
Owner decisions: approve V1 as single-user desktop deterministic-worker-first product? approve GitHub App registration or fine-grained PAT fallback? authorize implementation only after separate review and threat-model acceptance? choose license and pricing after market test?
No Desktop source, binary, GUI or deployment created under COMM-APP-01.
