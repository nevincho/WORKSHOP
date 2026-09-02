# TASK-059 — TANGRA Vision Recovery Pre-Codex Forensics

- `TASK_ID`: TASK-059
- `PROJECT`: TANGRA
- `PRIORITY`: CRITICAL
- `STATUS`: COMPLETE
- `OBJECTIVE`: Produce a reviewed, evidence-based pre-Codex forensic package for DroneGuard Vision / dual-camera / performance recovery without touching production, canonical TANGRA documentation, HOROS implementation, or Pi5 runtime.
- `SOURCE_PLAN_OR_REQUEST`: Vlad / dedicated TANGRA Vision Control Room, 2026-09-02. This request explicitly reactivates TANGRA only for bounded repository documentation/audit preparation. The existing OFFLINE_HOLD remains in force for runtime/Pi5 actions and implementation.
- `CURRENT_STATE`: Campaign preparation complete. All 11 required deliverables are persisted and repository-verified under `handoffs/TANGRA_VISION_RECOVERY_20260902/`. Independent Reviewer-role reconciliation returned PASS. `VISION_RECOVERY_CODEX_HANDOFF.md` is `READY_FOR_CODEX_REVIEW` with human gate required before Codex execution. Authoritative current DroneGuard development-copy implementation remains `NOT VERIFIED` until Codex reconciliation, by campaign design.
- `PREREQUISITES`: TANGRA-DOCS read access VERIFIED; WORKSHOP write access VERIFIED; owner campaign boundaries supplied; no runtime access required.
- `DEPENDENCIES`: historical evidence reconstruction COMPLETE; FPS metric reconciliation COMPLETE for documented history; Vision trace reconstruction COMPLETE as a pre-Codex historical/current-supplied map; protected HQ baseline identification COMPLETE; hypothesis review COMPLETE; Codex experiment sequencing COMPLETE. Current implementation reconciliation and runtime measurements remain future Codex work.
- `AFFECTED_COMPONENTS`: WORKSHOP coordination documentation only. Future Codex inspection targets include camera acquisition, preprocessing, Hailo primary/secondary paths, filters, NanoTracker, CA integration boundary, Object Resolver, projection/range, CURRENT_TARGET, Fusion input, telemetry, Dashboard/API.
- `PROTECTED_COMPONENTS`: DroneGuard production; validated HQ IMX477 + 50 mm detection/tracking line and independent fallback mode; CA Kalman mathematics; Runtime Controller/OFF-STANDBY behavior; canonical TANGRA-DOCS; HOROS; command/actuation paths.
- `EXECUTION_CLASS`: MONITOR_ONLY
- `CODEX_ALLOWED`: GATE_REQUIRED
- `ACCEPTANCE_CRITERIA`: PASS — all 11 requested deliverables exist in one dedicated Workshop campaign area; evidence classes are explicit; FPS metrics are not mixed; current supplied WIDE findings remain separate from hypotheses; HQ fallback and CA protection are explicit; profiling and experiment plans use one-change/A-B/rollback discipline; independent Reviewer role found no unsupported root-cause claim; final handoff is sufficient for Codex to start with implementation reconciliation, snapshot, trace, instrumentation and first bounded A/B test.
- `VALIDATION_METHOD`: source-to-claim reconciliation against bounded TANGRA-DOCS reports; adversarial Reviewer-role pass against WORKSHOP validation policy; repository re-fetch of final artifacts. No live/runtime validation is claimed.
- `PRE_CHANGE_CHECKPOINT`: TANGRA production/canonical docs unchanged. WORKSHOP pre-task main state before this task is represented by repository history immediately preceding the task start commit.
- `ROLLBACK_METHOD`: delete/revert TASK-059 Workshop-only artifacts via Git history. No target runtime rollback is required because no target implementation was changed.
- `EVIDENCE_PATHS`: `handoffs/TANGRA_VISION_RECOVERY_20260902/` and this task file.

## Completion evidence

Required package files verified in repository:

1. `VISION_RECOVERY_EXECUTIVE_SUMMARY.md`
2. `HISTORICAL_PERFORMANCE_TIMELINE.md`
3. `VISION_END_TO_END_TRACE.md`
4. `HQ_WIDE_ASSUMPTION_MATRIX.md`
5. `PERFORMANCE_PROFILING_PLAN.md`
6. `ROOT_CAUSE_HYPOTHESIS_REGISTER.md`
7. `DUAL_CAMERA_MODE_DECISION_MATRIX.md`
8. `CODEX_CONTROLLED_EXPERIMENT_PLAN.md`
9. `SOURCE_EVIDENCE_MANIFEST.md`
10. `INDEPENDENT_REVIEW.md`
11. `VISION_RECOVERY_CODEX_HANDOFF.md`

Final package review status: `PASS`.

Final handoff status: `READY_FOR_CODEX_REVIEW — HUMAN GATE REQUIRED BEFORE EXECUTION`.

Production modified: `NO`.

Canonical `TANGRA-DOCS` modified: `NO`.

Pi5/runtime probed or changed: `NO`.

HOROS implementation modified: `NO`.

## Hard campaign rules

`NO FIX BEFORE TRACE`.

Do not infer current implementation from TANGRA-2.0, HOROS artifacts, memory, or historical source-path descriptions. Historical source paths identify files/interfaces for later reconciliation only. Any current implementation statement unavailable from the authoritative development copy is `NOT VERIFIED`.
