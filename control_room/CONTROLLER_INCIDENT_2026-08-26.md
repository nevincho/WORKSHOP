# WORKSHOP Controller Incident — 2026-08-26

STATUS: REPAIRED / MONITORING
CLASSIFICATION: COORDINATION / SCHEDULER FAILURE

## Observed failure
At Control Room inspection on 2026-08-26, the active automation `WORKSHOP Fresh Controller` was found disabled. Its last recorded run was controller run 23 at approximately 07:31–07:36 BST. No subsequent hourly controller pass occurred after later TASK-008 Codex/runtime evidence and later `nevincho/LIVE@Legacy` changes were committed.

Repository symptoms were therefore stale coordination artifacts, not proof that Worker/Reviewer implementation had failed:
- `status/WORKSHOP_STATE.yaml` still held TASK-008 as `READY_FOR_CODEX_REVIEW` after `evidence/TASK-008/CODEX_RUN.md` made it reviewable;
- Independent Reviewer status remained older than the live TASK-008 evidence;
- downstream TASK-030 remained blocked on the stale TASK-008 coordination state;
- target `nevincho/LIVE@Legacy` advanced beyond the controller's last inspected checkpoint.

## Root cause
Primary verified root cause: the hourly `WORKSHOP Fresh Controller` automation itself was disabled, so no post-runtime reconciliation pass could execute.

Secondary design weakness: the controller prompt selected work primarily from coordination state and did not explicitly require reconciliation of newer Codex/runtime/target-repository evidence when `WORKSHOP_STATE.yaml` was stale. This could leave a task at a pre-execution gate even after valid external execution evidence existed.

The reason the scheduler became disabled is NOT VERIFIED from repository evidence alone.

## Repair applied
1. Re-enabled the exact `WORKSHOP Fresh Controller` automation.
2. Reset it to an exact hourly schedule beginning 2026-08-26 17:00 Europe/London.
3. Updated its controller instruction to:
   - read `STATE_MACHINE` and `QUEUE_PROTOCOL` every run;
   - reconcile newer execution/runtime/Codex evidence before selecting READY tasks;
   - route reviewable results to Independent Reviewer even if coordination state is stale;
   - never promote a Codex report directly to COMPLETE;
   - avoid rerunning already completed phases;
   - recompute downstream unblock conditions only after independent PASS.
4. Re-enabled `WORKSHOP Controller Watchdog` and bound it explicitly to the Fresh Controller automation rather than an ambiguous controller name.
5. Reset watchdog schedule to 2026-08-26 17:05 Europe/London and every 3 hours thereafter.
6. Independently reviewed TASK-008 from its task, gate, implementation diff, runtime evidence, current target state and protected memory semantics. Review verdict: PASS. See `review/TASK-008.md`.
7. Updated `tasks/TASK-008-VK-IMOU-INTEGRATION.md` to COMPLETE/PASS at checkpoint `840f94abb18f10c87798c2e4a54796dd6dab2bc2` with rollback `cf911176be543393f1a05e578b4ea30d70f010bb`.

## Important target-repository observation
During repair, `nevincho/LIVE@Legacy` was inspected and found at `4a0cc9253bcc890f64de678e64708de6b8368980`, one commit after the TASK-008 implementation checkpoint. The later commit routes explicit camera sources in `vk_runtime.py`. It preserves candidate-only perception semantics in the inspected source, but its mapping to a separate WORKSHOP task and its independent validation status are NOT VERIFIED by this incident report. The restarted controller must reconcile it rather than assuming it belongs to TASK-008 or any downstream task.

## Acceptance for incident closure
The incident is considered scheduler-repaired now. Full operational closure requires observing a subsequent Fresh Controller run with:
- automation still enabled;
- updated `last_run_time` within the expected hourly window;
- repository-side reconciliation of current task/evidence/review state;
- no duplicate controller/task creation;
- downstream task promotion only when all task-specific unblock conditions are verified.

No protected VK Core/personality/canonical-memory component was modified by this repair. No Codex was invoked by Control Room for the repair.
