# WORKSHOP-COMM-AI-PARITY-INTEGRATED-01 — Commercial AI WORKSHOP Desktop integrated campaign

PROJECT: WORKSHOP Commercial Edition
DATE: 2026-11-03
MODE: CONTROL_ROOM → WORKSHOP INTEGRATED CAMPAIGN
STATUS: IN_PROGRESS (PARTIAL IMPLEMENTATION / NO RELEASE)
OWNER OBJECTIVE: Convert the existing installable Windows Desktop into a commercially distributable, user-friendly equivalent of the AI WORKSHOP engineering workflow used in the ChatGPT project. Keep the existing Desktop functions as advanced project tools. No Codex execution is authorized for this campaign.

## Product contract — do not substitute an MVP

The primary screen is **Create Project**: a customer names a project, selects or creates its local workspace and optional repository, describes desired software in plain language, then receives an intelligible bounded plan, authorizes execution, observes real progress, reviews the result and can recover prior states. The WORKSHOP control plane orchestrates Planner/Worker/independent Reviewer/test/checkpoint processes; execution may use a customer-selected **local model**, **external model API**, or **supported GitHub coding agent**. Any provider may be absent, in which case the UI must explain exactly which actions remain available. The existing deterministic Markdown writer remains usable; it is not advertised as an AI coder.

This is a commercial multi-project development application, not just a Markdown task runner. Do not present placeholder integrations or simulated AI outputs as working features.

## Existing baseline and protected scope

Repository: nevincho/WORKSHOP. Existing Desktop candidate: PR #4 on feature/desktop-v1-d1-d3-repair-20261101; base feature/desktop-v1-completion-20261031. Latest source/PR state must be reverified at campaign execution. Desktop components include controller/approval/recovery/evidence, GitHub adapter, installer, G1 browsing and markdown-writer-v1. User manually exercised install, create workspace, coordination Git, settings, GitHub-optional wizard, Plan, approval, local Run, local preflight Review, persisted task state, Recovery no accepted checkpoint, Evidence, Projects and Detail. Live independent GitHub review, full security and commercial release remain NOT VERIFIED.

PROTECT: current Desktop source and behavior, G1, controller authorization boundaries, cryptographic/evidence chain, policies/schemas, other projects, user data, current branch and PR, backward-compatible workspace files, credentials, uninstall/rollback. No unrelated refactors, no direct changes to production TANGRA, no automatic GitHub merges, paid API usage or actual hardware commands.

## Single campaign objective — completed as a dependency-aware integrated product

A. **Functional mapping and product contract:** Use existing WORKSHOP control-room/worker/reviewer/campaign policies, tasks, examples, target repo and Desktop current implementation as evidence. Enumerate functions that actually exist and gaps. Implement only evidence-backed missing product behavior. Do not confuse Markdown role instructions with autonomous executables.

B. **Create Project first, user-friendly UX:** Plain-language prompt, guided project/repository setup, contextual next-action, beginner explanations, task timeline, clear success/error messages, and an Advanced mode exposing ALL existing controls (Welcome, Tasks, Projects, Detail, Approvals, Plan, Run, Review, Recovery, GitHub, Evidence, Settings). Preserve their working interfaces. Replace normal-operation flashing console windows with in-app progress/status/logs where technically possible, without hiding execution failures. Report actual stages, never fabricated percentage.

C. **AI provider settings:** Local inference endpoint (e.g. Ollama / supported OpenAI-compatible localhost), external provider with customer-supplied credentials, and optional hybrid with explicit paid/network escalation consent. Discover capabilities rather than assuming models support tools. Secure local credential storage, cost limits, prompt/data disclosure warnings, offline-only enforcement, provider connection test, clear missing-provider state, observable usage and redaction.

D. **Real coding execution:** Adapt WORKSHOP Controller to controlled tool-capable code editing/build/test in a disposable checkout/worktree, under explicit path/repository permissions, per-task immutable approval and bounded resources. No claim of OS-level sandbox unless actually established on Windows. Provider is a replaceable executor; Control Room owns task routing and state, not the model. Handle cancellation, lost connectivity, restart and rework with no silent replay of writes.

E. **Reviewer and evidence:** Ensure genuine independence: separate reviewer context/identity, frozen diff and evidence, tests that measure claims; never label local preflight as independent acceptance. Human approval gates, immutable proof, safe recovery/rollback, target-repository PR controls remain authoritative.

F. **GitHub coding-agent adapter:** First verify current provider APIs, customer account entitlement, supported authentication, task dispatch, run status, results, PR provenance and charges. Integrate only documented supported functionality; gracefully disable when not eligible. GitHub connection alone must not be represented as enabling agent use. Keep customer credentials and rate/cost boundaries.

G. **Commercial delivery:** Polished English-first Windows UX suitable for nontechnical customers, installer/update/uninstall path, licensing/distribution decision, documentation, onboarding, crash diagnostics, local Win10/11 tests and separate-account GitHub acceptance. No sale-ready claim without required owner-side gates.

## Current active execution handoff (2026-11-04)

WORKER_BRANCH: feature/workshop-ai-local-provider-20261104
WORKER_PR: https://github.com/nevincho/WORKSHOP/pull/6
WORKER_SOURCE: apps/workshop_desktop_v1/workshop_desktop/ai_provider_contract.py and ollama_provider.py
WINDOWS_CI: https://github.com/nevincho/WORKSHOP/actions/runs/41793002189 — 3 tests PASS on hosted Windows, no real Ollama runtime
CURRENT_BOUNDARY: local text-only provider exists; not linked to Controller; no real coding execution; no independent reviewer; no commercial acceptance
NEXT_WORK: verify provider interface consistency and safety; independently review source and evidence; only then plan smallest integrated coding execution unit. A task file, plan, draft PR, or automation trigger is NOT an executing autonomous worker.

## Execution and review

WORKSHOP internally performs appropriate inspection → bounded implementation → actual tests → independent Reviewer → checkpoint, re-evaluating dependencies at each gate and continuing when authorized and safe. Do not create one chat prompt or one repository report per minor internal operation; consolidate artifacts. Codex is prohibited in this campaign unless the owner explicitly changes that decision. Use another validated Worker route; if unavailable, report the exact executor dependency rather than claiming development or inventing execution.

Proof milestone: a newly installed Windows user can create an isolated sample software project in plain language, choose a functioning provider, approve a plan, obtain REAL compilable code plus measured tests/evidence and independently reviewed diff, review and accept/reject with recovery after restart, without knowing Git internals. For ESP32 sample code, compile/test can be demonstrated separately from hardware verification; no fabricated physical validation.

Acceptance: maintain regression and validated existing flow; demonstrate one end-to-end genuine coding task with a real provider, bounded protection and negative tests; provider failures and unavailable/paid-account conditions fail safely; Reviewer assesses complete source/diff/provenance; real Windows customer test and license/commercial gating recorded accurately. Each stage must be described as DONE, NOT VERIFIED or BLOCKED from evidence. Current owner-side release gates remain separate.

STOP: integrated product qualified and owner acceptance gates listed, or exact external/owner-only blocker with preserved artifacts and next eligible dependency. Do not report task creation itself as software implementation.
