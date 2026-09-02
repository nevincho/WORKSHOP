# INDEPENDENT REVIEW

TASK_ID: `TASK-059`  
Reviewer role: WORKSHOP Independent Reviewer  
Date: 2026-09-02  
Verdict: **PASS — PRE-CODEX FORENSIC PACKAGE / READY FOR FINAL HANDOFF**

## Independence statement

This review is a deliberate role-separated adversarial pass executed inside the current Control Room against persisted WORKSHOP artifacts and TANGRA-DOCS evidence. No separate external model/process was available in this execution context. Therefore independence is procedural/evidentiary, not an assertion of a different executor identity. No agent completion claim was accepted as proof.

## 1. Objective actually reviewed

The objective is **not** to prove or fix the current DroneGuard Vision defect. The reviewed objective is to prepare a bounded, evidence-based investigation package so that Codex can reconcile the authoritative development copy, protect the HQ baseline, trace first divergence, measure performance and execute one-change A/B experiments.

That objective is appropriate for the current phase because the authoritative development copy is intentionally unavailable to Workshop and production/runtime actions remain on hold.

## 2. Prerequisites

| Prerequisite | Review finding |
|---|---|
| TANGRA-DOCS historical repository accessible | PASS — repository evidence was directly read during campaign |
| WORKSHOP persistence available | PASS — package artifacts exist in dedicated handoff directory |
| current production/development implementation available to Workshop | NOT REQUIRED for preparation objective; explicitly `NOT VERIFIED` and deferred to Codex reconciliation |
| production/runtime modification authorization | NOT REQUIRED and not used |
| physical calibration | NOT REQUIRED for upstream forensic preparation; correctly retained as later metric gate |
| HOROS implementation | OUT OF SCOPE and not used as runtime authority |

## 3. Evidence-class discipline

### PASS

The package separates:

- historical documented evidence;
- current owner-supplied evidence;
- owner requirement;
- hypotheses;
- current implementation unknowns.

Current WIDE observations are not falsely represented as repository-verified implementation facts.

The package correctly distinguishes the two supplied WIDE observations:

1. raw detections exist but are rejected at a physical-size/class-area gate; and
2. a separate small target is heavily reduced by preprocessing and yields zero raw detection.

They are not merged into one root cause.

### PASS WITH EXPLICIT LIMIT

The exact historical artifact for the reported stale NanoTracker measurement reapplication/confirmation concern was not found in bounded TANGRA-DOCS searches. The package marks it `NOT VERIFIED / CHECK REQUIRED` and restricts any future repair to observation-freshness/update-eligibility unless evidence proves more. This is methodologically correct. Claiming the defect proven would have failed review.

## 4. FPS methodology review

### Critical issue identified and correctly handled

Historical records contain incompatible/undefined FPS metrics. The July-27 evidence explicitly proves a historical displayed counter excluded the configured 30 ms sleep, while controlled true end-to-end throughput was ~15–16 FPS. Earlier values around 29–41 therefore cannot be directly compared without counter equivalence.

The package does **not** average or rank these values as if they were one metric. The timeline records metric type/unknown state and marks non-comparable records accordingly.

The owner rule `<25 FPS normal tracking = PERFORMANCE FAIL` remains preserved. The package requires Codex to:

- identify the current owner-facing/normal-tracking metric semantics;
- report processing/pre-sleep and true end-to-end metrics simultaneously;
- establish a present-day matched HQ-only control;
- never pass an architecture on an unlabeled FPS number.

Reviewer finding: **PASS**. A test that applied 25 to an unspecified metric would be a validation-methodology failure, not an implementation failure.

## 5. Historical root-cause reconciliation

The package correctly distinguishes closed historical root causes from current hypotheses:

- Object Resolver object churn is a **proven historical root cause** for the July16 episode, with bounded post-fix recovery evidence. It is used only as a regression check for current work.
- July15 `world_map_3d`/JPEG/deep-copy/synthetic-view findings remain partial/candidate-level where the reports did not prove sole causality.
- July27 periodic Secondary HEF cost and replay Hailo inference stalls are treated as historically verified performance contributors, not explanations of current WIDE acceptance filtering.
- July22 harness RSS false-fail is correctly classified as methodology failure caused by expected shutdown memory release.

Reviewer finding: **PASS**.

## 6. HQ baseline protection review

The package makes an important distinction:

- HQ IMX477 + 50 mm **detection/tracking behavior** is protected; and
- HQ camera metric/world projection is **not physically calibrated end-to-end**.

This prevents false transfer of validation from tracking into 3D/range accuracy.

The proposed Mode C remains independently activatable, and Modes A/B are not allowed to make HQ operation depend on WIDE calibration/initialization/association.

Reviewer finding: **PASS**.

### NOT VERIFIED

Historical documentation names WIDE inside the official stable stack, but the package does not claim that a historically validated HQ-only startup mode already existed. It treats independent HQ fallback as a mandatory future protection requirement. This is the correct classification.

## 7. CA Kalman protection review

CA replay evidence supports protecting the current canonical mathematics from speculative retuning. The experiment plan checks freshness/update eligibility using a detection-gap trace without modifying Kalman equations.

Reviewer finding: **PASS**.

The later camera-profile/current-baseline notes contain differing descriptions of timing/state semantics across historical analyses. The package correctly requires current authoritative source reconciliation rather than selecting one historical description as current truth.

## 8. Vision trace completeness review

The trace covers all required boundaries from scene/camera through preprocessing, Hailo, parser/NMS, filtering, accepted detections, Resolver, NanoTracker, freshness, CA, projection/range, CURRENT_TARGET, Fusion input, telemetry/API and Dashboard/JPEG consumers.

For each boundary it distinguishes historical HQ behavior, WIDE/current evidence, assumptions and current unknowns.

HOROS is stopped at the upstream/Fusion boundary and is not included as a repair target.

Reviewer finding: **PASS**.

## 9. Performance profiling review

The profiling plan separates:

- capture cost;
- frame copy/format/preprocessing;
- Hailo queue wait and execution;
- primary/secondary costs;
- postprocessing/filtering;
- tracker/CA/Resolver/CURRENT_TARGET/Fusion preparation;
- telemetry/deep-copy/JSON/logging/JPEG/API;
- pacing/sleep;
- client load;
- GC/scheduler/I/O correlations.

It includes an instrumentation-overhead control and avoids writing per-frame profiler data through the production telemetry path being measured.

Reviewer finding: **PASS**.

## 10. Controlled experiment discipline

The Codex sequence obeys `NO FIX BEFORE TRACE` and does not bundle speculative fixes.

Important gate behavior is correct:

- E06 filter divergence must reproduce before a gate change.
- E07 small-target raw failure must independently reproduce before preprocessing work.
- E08 and E09 are conditional and separate.
- camera controls are isolated as their own experiment.
- Secondary HEF, telemetry/JPEG and dual-camera scheduling are measured separately after upstream correctness.
- Mode A is not attempted merely because it is feature-richer; Mode B is tested first after staged cost isolation.
- every failed candidate reverts before the next candidate.

Reviewer finding: **PASS**.

## 11. Dual-camera decision methodology

Mode A/B/C are treated as empirical candidates, with gate-first rather than weighted feature scoring. Functional benefit cannot compensate for performance failure. Cross-camera association/calibration is required only when the architecture actually consumes cross-camera metric/authority evidence.

The package does not claim calibration alone produces reliable stereo/3D and does not claim a 35.6 mm baseline is sufficient for operational-depth accuracy.

Reviewer finding: **PASS**.

## 12. Regression coverage

Final retained-candidate regression includes:

- HQ physical/replay path;
- detector/filter behavior;
- NanoTracker freshness/continuity;
- CA unchanged mathematics;
- Object Resolver bounded identity/state;
- CURRENT_TARGET;
- Fusion inputs/authoritative outputs;
- telemetry/API/Dashboard;
- camera/Hailo lifecycle;
- OFF/STANDBY;
- resource/performance metrics.

No WIDE improvement is allowed to hide an HQ regression.

Reviewer finding: **PASS**.

## 13. Scope / repository hygiene

- TANGRA-DOCS canonical files modified: **NO**.
- production source/runtime modified: **NO**.
- Pi5 probed/restarted/deployed: **NO**.
- TANGRA-2.0 used as current runtime authority: **NO**.
- HOROS implementation used as current runtime authority: **NO**.
- extra implementation/source code created: **NO**.
- substantive output persisted in one dedicated WORKSHOP package plus the canonical task file.

The user explicitly required 11 deliverables, so retaining all 11 is a Control Room requirement and an intentional exception to normal report-compaction preference. No additional narrative archive was created.

Reviewer finding: **PASS**.

## 14. Remaining NOT VERIFIED items — not blockers to handoff

1. Current authoritative development-copy implementation/files/config/hashes.
2. Current FPS counter semantics/pacing.
3. Current physical camera controls and stable camera identity mapping.
4. Exact current WIDE preprocessing/filter formula and profile selection.
5. Current matched HQ-only performance baseline.
6. Current dual-camera performance/resources.
7. Exact historical stale-NanoTracker evidence artifact.
8. Physical intrinsics/extrinsics and HQ infinity-focus quality.

These are exactly the first Codex reconciliation/measurement tasks; their absence is expected in a pre-Codex package and therefore does not block preparation completion.

## Final reviewer verdict

**PASS — READY FOR `VISION_RECOVERY_CODEX_HANDOFF.md`.**

The package reduces historical rediscovery and investigation-strategy cost without pretending the current root cause is known. The correct next engineering action is authoritative implementation reconciliation and measurement, not a Workshop-selected fix.
