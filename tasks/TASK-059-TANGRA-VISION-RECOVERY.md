# TASK-059 — TANGRA Vision Recovery Pre-Codex Forensics

- `TASK_ID`: TASK-059
- `PROJECT`: TANGRA
- `PRIORITY`: CRITICAL
- `STATUS`: IN_PROGRESS
- `OBJECTIVE`: Produce a reviewed, evidence-based pre-Codex forensic package for DroneGuard Vision / dual-camera / performance recovery without touching production, canonical TANGRA documentation, HOROS implementation, or Pi5 runtime.
- `SOURCE_PLAN_OR_REQUEST`: Vlad / dedicated TANGRA Vision Control Room, 2026-09-02. This request explicitly reactivates TANGRA only for bounded repository documentation/audit preparation. The existing OFFLINE_HOLD remains in force for runtime/Pi5 actions and implementation.
- `CURRENT_STATE`: TANGRA-DOCS repository history is accessible and contains historical baseline/performance/vision evidence. Authoritative current DroneGuard development-copy implementation is intentionally not available to Workshop at this phase and remains `NOT VERIFIED` until Codex reconciliation.
- `PREREQUISITES`: TANGRA-DOCS read access VERIFIED; WORKSHOP write access VERIFIED; owner campaign boundaries supplied; no runtime access required.
- `DEPENDENCIES`: historical evidence reconstruction; FPS metric reconciliation; Vision trace reconstruction; protected HQ baseline identification; hypothesis review; Codex experiment sequencing.
- `AFFECTED_COMPONENTS`: WORKSHOP coordination documentation only. Future Codex inspection targets include camera acquisition, preprocessing, Hailo primary/secondary paths, filters, NanoTracker, CA integration boundary, Object Resolver, projection/range, CURRENT_TARGET, Fusion input, telemetry, Dashboard/API.
- `PROTECTED_COMPONENTS`: DroneGuard production; validated HQ IMX477 + 50 mm detection/tracking line and independent fallback mode; CA Kalman mathematics; Runtime Controller/OFF-STANDBY behavior; canonical TANGRA-DOCS; HOROS; command/actuation paths.
- `EXECUTION_CLASS`: MONITOR_ONLY
- `CODEX_ALLOWED`: GATE_REQUIRED
- `ACCEPTANCE_CRITERIA`: all 11 requested deliverables exist in one dedicated Workshop campaign area; evidence classes are explicit; FPS metrics are not mixed; current supplied WIDE findings remain separate from hypotheses; HQ fallback and CA protection are explicit; profiling and experiment plans use one-change/A-B/rollback discipline; independent Reviewer role finds no unsupported root-cause claim; final handoff is sufficient for Codex to start with implementation reconciliation, snapshot, trace, instrumentation and first bounded A/B test.
- `VALIDATION_METHOD`: source-to-claim reconciliation against bounded TANGRA-DOCS reports; adversarial Reviewer-role pass against WORKSHOP validation policy; repository re-fetch of final artifacts. No live/runtime validation is claimed.
- `PRE_CHANGE_CHECKPOINT`: TANGRA production/canonical docs unchanged. WORKSHOP pre-task main state before this task is represented by repository history immediately preceding this commit.
- `ROLLBACK_METHOD`: delete/revert TASK-059 Workshop-only artifacts via Git history. No target runtime rollback is required because no target implementation is changed.
- `EVIDENCE_PATHS`: `handoffs/TANGRA_VISION_RECOVERY_20260902/` and this task file.

## Hard campaign rules

`NO FIX BEFORE TRACE`.

Do not infer current implementation from TANGRA-2.0, HOROS artifacts, memory, or historical source-path descriptions. Historical source paths identify files/interfaces for later reconciliation only. Any current implementation statement unavailable from the authoritative development copy is `NOT VERIFIED`.
