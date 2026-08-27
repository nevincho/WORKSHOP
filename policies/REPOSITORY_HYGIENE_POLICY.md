# REPOSITORY HYGIENE POLICY

STATUS: MANDATORY
APPLIES TO: ALL AGENTS, CODEX, AUTOMATIONS, WORKSHOP AND TARGET REPOSITORIES
OVERRIDE: ONLY VLAD / WORKSHOP CONTROL ROOM

## Purpose

Prevent repositories from accumulating disposable intermediate work that later consumes engineering/Codex capacity merely to rediscover and clean it. Repository hygiene is part of the work itself, not a deferred maintenance phase.

## Mandatory same-task cleanup

1. Cleanup MUST occur immediately as part of completing the task that created or superseded the files.
2. A task is not ready for final Reviewer PASS/COMPLETE until task-local repository hygiene has been checked.
3. Do not defer known disposable-file cleanup to a later cleanup task, backlog item, Codex session, or periodic maintenance run when it can safely be resolved during the current task.
4. Worker/Codex owns cleanup of disposable artifacts created by its work. Reviewer verifies the resulting repository state before PASS.

## Keep

Retain only artifacts with continuing engineering, operational, evidentiary, or rollback value, including:

- current authoritative/production source and configuration;
- required tests, fixtures, datasets and licensed production assets;
- canonical specifications, decisions and interfaces;
- concise task evidence describing what changed, why, how it was validated, and relevant commit/checkpoint references;
- final independent reviews and required reports;
- checkpoint/rollback references or artifacts required by CHECKPOINT_AND_BACKUP_POLICY;
- material required by an active unfinished task or dependency;
- unique evidence required to support a validation or incident conclusion.

## Remove or avoid committing

Unless specifically justified by an active requirement, remove or do not commit:

- temporary/scratch files;
- generated debug dumps with no continuing evidentiary value;
- disposable test outputs and transient logs;
- failed experimental variants after their conclusion is captured in concise evidence;
- superseded implementation copies;
- duplicate files and redundant exports;
- naming variants such as `old`, `new`, `final2`, `backup-copy`, `tmp`, or equivalent when Git/checkpoint history already preserves the needed history;
- abandoned partial drafts and incomplete generated documentation;
- stale generated caches/build artifacts that are reproducible and not required deliverables;
- copied source trees or archives retained only as convenience when an authoritative source/checkpoint exists.

Git history and approved checkpoints are the normal version-history mechanism. The live repository must not become a museum of obsolete working versions.

## Evidence preservation

Cleanup MUST NOT destroy the engineering thread. Before removing an intermediate artifact whose existence materially explains a decision, failure, or validation result, preserve the necessary conclusion in concise task evidence. Evidence should record the result and relevant method/reference, not every disposable intermediate file.

## Safety boundaries

Cleanup is not permission for broad repository deletion.

- Default cleanup scope is files created, generated, replaced, or made obsolete by the current task.
- Do not delete an existing file merely because its name looks old or temporary without verifying references, ownership, dependency and current repository state.
- Do not remove the sole rollback artifact, sole validation evidence, authoritative source, production asset, active-task dependency, or legally required provenance/license material.
- Broad cleanup of pre-existing repository debt requires a separate inventory/review unless deletion safety is directly evidenced.
- Protected components remain protected; hygiene does not override protection or human-gate policies.

## Codex conservation

Repository hygiene is expected to be cheap and immediate. Do not route ordinary cleanup, duplicate removal, scratch-file deletion, or documentation pruning to Codex when Worker/controller can safely perform it. Codex must not be consumed later to clean disposable artifacts that should have been removed during the originating task.

## Definition of Done

Before a task can be marked PASS/COMPLETE, Reviewer must establish:

1. required implementation/deliverables are present;
2. validation evidence is preserved;
3. no known task-created disposable/superseded artifacts remain without justification;
4. no required authoritative, rollback, provenance, or validation artifact was removed;
5. repository state is understandable from current files plus concise evidence and Git/checkpoint history.

If hygiene fails, return the task for task-local cleanup rather than opening a later generic cleanup task, unless cleanup itself is unsafe or requires a separate human decision.
