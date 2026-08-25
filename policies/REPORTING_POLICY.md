# REPORTING POLICY

STATUS: MANDATORY
APPLIES TO: WORKSHOP CONTROLLER, ALL AGENTS, TASK EVIDENCE, AND ALL PROJECT REPORTS

## Principle: repository is working state, not a report archive
The repository MUST remain small enough for humans and AI agents to inspect economically. Intermediate narrative artifacts are disposable once their useful facts have been consolidated into authoritative task/evidence state.

Do NOT preserve obsolete reports "just in case". Git history is the rollback/audit mechanism for deleted tracked material; do not create archive, legacy, old, backup, v2/v3/v4, superseded, or recovery copies merely to retain narrative history.

## Task-convergence cleanup gate
When a task reaches either:
- final validated completion; or
- `READY_FOR_CODEX_REVIEW` / equivalent Codex-action gate,

the responsible agent/controller MUST perform documentation compaction immediately.

After compaction, retain only the minimum current set needed to execute, review, validate, or understand the task:
1. the authoritative task specification/current task state;
2. ONE concise final/consolidated evidence or engineering report when explanation is required;
3. machine-relevant evidence that is genuinely required to substantiate acceptance criteria (for example test output, hashes, measurements, or exact validation references);
4. implementation/source artifacts that are part of the product;
5. required rollback/checkpoint references.

Delete superseded intermediate planning notes, duplicate analyses, worker/reviewer narrative reports whose conclusions are already consolidated, repeated status reports, stale drafts, temporary handoffs, duplicated evidence summaries, and obsolete versioned report variants.

## No shadow archives
Cleanup MUST NOT respond to deletion by moving the same clutter elsewhere in the repository. Specifically prohibited unless a human explicitly requests retention for a defined reason:
- `archive/`, `old/`, `legacy/`, `backup/`, `superseded/`, `recovery/` copies of intermediate reports;
- numbered report generations kept after consolidation;
- duplicate checkpoints containing information already represented by current state plus Git history.

If an intermediate tracked document has historical value only, delete it from the current tree and rely on Git history.

## Codex context protection
Before handing a task to Codex, the Codex Gate/Task Engineer MUST minimize the documentation/context surface. Codex should receive the authoritative task, required interfaces/files, protected-component rules, exact evidence needed for the change, and acceptance tests — not the full history of intermediate reports.

Codex MUST NOT be asked to scan broad historical documentation when a compact current-state packet can be produced by WORKSHOP first.

## Periodic reports
Periodic operational reporting must be concise and state-oriented. Reports do not pause autonomous work unless a human gate exists.

A current operational report may include:
- reporting window;
- tasks completed and independently validated;
- blockers/root causes;
- current validated checkpoints/rollback references;
- Codex usage and justification;
- tests actually run and what objective they measured;
- NOT VERIFIED items;
- next eligible tasks;
- human decisions required.

Do not create a new report merely because a cadence boundary passed when there has been no material state change. Prefer updating/consolidating current state over accumulating repetitive reports.

## Evidence rule
A report is a summary, not proof. Claims of completion/validation must point to repository/runtime evidence. Agent reports alone do not establish project state.

Evidence retention is justified by acceptance/validation needs, not by the fact that an agent happened to generate it.

## Notification rule
Do not notify Vlad between scheduled reporting windows unless a human gate requires intervention.
