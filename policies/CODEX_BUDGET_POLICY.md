# CODEX BUDGET POLICY

STATUS: MANDATORY
APPLIES TO: ALL AGENTS, CODEX, AUTOMATIONS
OVERRIDE: ONLY VLAD / WORKSHOP CONTROL ROOM

Codex capacity is scarce and must be conserved.

Codex MUST NOT be used for repository discovery, general audits, inventory, documentation reading, task decomposition, mechanical file work, log summarization, evidence collection, or validation that another capable worker can perform.

## DEFAULT EXECUTION MODEL — CONSOLIDATE BEFORE CODEX

WORKSHOP agents must exhaust all authorized repository-side work before escalating to Codex. This includes analysis, implementation that is safe within the target repository, fixtures, tests, documentation, evidence, independent review, downstream preparation, and dependency-chain consolidation.

A task reaching a runtime/human gate MUST NOT automatically prevent repository-safe preparation or implementation of downstream tasks when those downstream steps can be performed and validated without claiming the gated runtime prerequisite as proven. Such work must clearly record any runtime-dependent assumptions and must not claim live validation.

Prefer ONE consolidated Codex integration/deployment/live-validation run over multiple component-level Codex runs. A Codex handoff should, where prerequisites allow, package all reviewed repository-ready changes in the current dependency chain that belong to the same target runtime/integration session.

Codex's default high-value role is to take reviewed repository-ready work into the actual target environment and perform the environment-specific integration, deployment/configuration, difficult runtime debugging, hardware/local-network interaction, and live validation that WORKSHOP repository agents cannot perform.

Repository coding by Codex is an exception, not the default. Codex Gate must state why the required repository implementation could not reasonably be completed by authorized WORKSHOP workers before escalating coding work to Codex.

Do not duplicate or rewrite repository implementation already completed and reviewed by WORKSHOP unless verified integration evidence proves a change is necessary.

Before escalation to Codex, WORKSHOP must provide a minimal consolidated implementation/integration package containing: task IDs covered, exact objective, verified current state, affected components, prerequisites, protected components, acceptance criteria, validation method, rollback/checkpoint, explicit non-goals, target runtime/host, and the reviewed repository commits/artifacts to integrate.

CURRENT OPERATING MODE — HUMAN CODEX GATE:
1. Agents and automations MUST NOT invoke Codex automatically.
2. Codex Gate may inspect tasks and prepare a minimal consolidated Codex handoff package, but execution requires explicit approval from Vlad / WORKSHOP Control Room.
3. Agents must complete all repository-side analysis, preparation, low-risk implementation, fixtures, tests, documentation, evidence and review that can be done without Codex.
4. A runtime-gated task may be recorded as `HOLD_FOR_CONSOLIDATION` while downstream repository-safe work continues. This is not FAILED and is not a technical BLOCKED state.
5. Downstream repository-safe work may proceed across such a hold only when it does not require pretending that the missing runtime evidence already exists. Runtime-dependent acceptance criteria remain NOT VERIFIED until the real integration/live-validation run.
6. When no further justified repository-safe work remains, Codex Gate prepares one consolidated `READY_FOR_CODEX_REVIEW` package for the target runtime/integration boundary.
7. Vlad may approve that consolidated package for Codex-assisted integration/deployment/testing on the relevant runtime or host.
8. No implicit approval carries to a different target runtime or unrelated consolidated package.

Use Codex only after explicit approval for target-environment integration/deployment/live validation, non-trivial implementation that workers demonstrably cannot perform, difficult debugging, sensitive integration, architecture-dependent precision work, or work beyond validated worker capability.

Never resend a failed Codex task without first identifying why the previous attempt was insufficient.
