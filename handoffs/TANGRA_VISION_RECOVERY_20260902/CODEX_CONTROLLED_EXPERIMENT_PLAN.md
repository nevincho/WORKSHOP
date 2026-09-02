# CODEX CONTROLLED EXPERIMENT PLAN

TASK_ID: `TASK-059`  
Target: authoritative isolated DroneGuard development copy, after explicit human Codex approval.  
Rule: `COPY → VERIFY BASELINE → TRACE → MEASURE → FIRST DIVERGENCE → ONE CHANGE → A/B → REGRESSION → PERFORMANCE GATE → KEEP/REVERT → NEXT`.

## Global controls

Before any experiment:

- production is not modified;
- create/verify immutable HQ-centric snapshot and record hash/path/commit as pre-change checkpoint;
- preserve a separately activatable HQ-only mode;
- confirm command/actuation paths remain disabled for Vision testing;
- identify exact current runtime files rather than trusting historical paths in this package;
- record camera hardware identity and current capture modes;
- bind every FPS field to an explicit metric;
- use identical fixture/physical stimulus for A/B where possible;
- change one independent variable per experiment;
- after a failed candidate, restore checkpoint before testing the next candidate.

## E00 — Authoritative implementation reconciliation

**Purpose:** determine what actually exists now.

**Inspect:** current development-copy entrypoint; camera manager/acquisition; configuration; detector/Hailo wrapper; parser/NMS/filter modules; tracker; CA integration call sites; Object Resolver; projection/range; CURRENT_TARGET; Fusion input; telemetry/API; Dashboard request paths; service/controller/configuration.

**Measurement:** none beyond hashes/versions/config inventory.

**Expected evidence:** file/interface map, runtime graph, current config values, model hashes, camera mapping, pacing/sleep setting, PVF/Secondary states.

**PASS:** every boundary in `VISION_END_TO_END_TRACE.md` maps to a real current file/function or is explicitly absent; no unsupported historical path is carried forward.

**FAIL:** unresolved duplicate implementation, ambiguous entrypoint, ambiguous camera identity or missing source needed to trace authority.

**Rollback:** read-only.

**Protected:** production, HQ baseline, CA math, HOROS.

## E01 — Immutable HQ baseline snapshot

**Purpose:** preserve final known HQ-centric development state before modifications.

**Action:** create verified immutable snapshot/tag/archive according to actual repository/runtime mechanism; record hashes of entrypoint/config/models and rollback command.

**PASS:** snapshot can be restored or compared deterministically; HQ-only startup dependency graph does not require planned WIDE changes.

**FAIL:** no trustworthy rollback. Stop modification chain.

## E02 — Current FPS semantics audit

**Purpose:** prevent invalid performance comparison.

**Inspect:** all FPS calculations/counters and pacing/sleep/COMM interval.

**Measurement:** derive formulas from source; add no behavior-changing fix.

**PASS:** each current FPS field is labeled capture/inference/processing/pre-sleep/end-to-end/replay; owner gate measurement location is declared; independent monotonic end-to-end counter planned.

**FAIL:** any acceptance run would use an ambiguous `fps` field. Do not proceed to performance claims.

## E03 — Instrumentation overhead control

**Purpose:** ensure profiler does not become the regression.

**Action:** add/enable bounded stage timing in the development copy only, with monotonic frame/camera IDs; run identical short OFF/ON instrumentation controls.

**PASS:** overhead is characterized and acceptable under a predeclared tolerance; output bounded and outside hot telemetry path where practical.

**FAIL:** instrumentation materially distorts runtime; reduce sampling/buffering and repeat only this gate.

**Rollback:** instrumentation switch/off or restore E01.

## E04 — Matched HQ-only performance/functional baseline

**Purpose:** establish present-day control, not historical inference.

**State:** HQ only; WIDE unavailable/disabled; record primary/Secondary/PVF/Dashboard/pacing states exactly. Run no-browser baseline first; use locked replay plus bounded physical HQ target if available.

**Measure:** processing and end-to-end FPS, stage latency, CPU/RSS/temp/throttle, raw/accepted detections, tracks, CA updates, CURRENT_TARGET, Resolver state, Fusion input, payload size, lifecycle.

**PASS:** HQ pipeline operates independently; regression fixtures pass; stable resources; labeled normal FPS captured.

**FAIL:** current HQ baseline itself is degraded. Stop dual-camera promotion work and localize HQ regression first using the same trace discipline.

## E05 — Current full Vision trace capture

**Purpose:** prove per-boundary behavior before any WIDE fix.

**Action:** for selected HQ and WIDE diagnostic frames, record source dimensions/bbox, transform metadata, tensor dimensions, raw detector count/output summary, parser output, every filter reason, accepted detections, tracker freshness, CA update eligibility, CURRENT_TARGET, Fusion input, telemetry source/camera provenance.

**PASS:** first divergence is observable with one reason/code boundary; all camera/source IDs remain traceable.

**FAIL:** hidden transformation or aggregated rejection prevents attribution. Improve diagnostics only; do not change algorithm.

## E06 — Reproduce current WIDE acceptance divergence

**Purpose:** independently verify supplied `4 raw → 0 accepted` path.

**State:** same raw input/fixture where feasible; no HOROS dependency in verdict.

**Measure:** raw detections, class/confidence, bbox dimensions in coordinate spaces, each size/area gate input/value/result.

**PASS:** identical raw detections are reproduced and exact first differing predicate is named.

**FAIL-A:** raw outputs differ before filter. Move investigation upstream; do not change gate.

**FAIL-B:** all detections pass current gate. Supplied issue not reproduced; classify as stale/config-specific until evidence resolves it.

## E07 — Reproduce WIDE small-target raw-inference failure

**Purpose:** independently verify supplied source ~110×55 → preprocess ~15×14 → raw0 observation.

**Measure:** target bbox after each actual transform, source sharpness/focus/exposure metadata, model input, raw confidence/output.

**PASS:** scale loss and raw failure reproduced under controlled current settings.

**FAIL:** observation not reproducible; do not optimize for it.

## E08 — Filter hypothesis A/B (only if E06 localizes filter mismatch)

**Purpose:** determine whether a specific HQ-centric size/area/profile assumption causes valid WIDE detections to be rejected.

**Change:** one predicate input/profile/coordinate interpretation only. Do not globally lower all thresholds.

**PASS:** valid WIDE detections become accepted as predicted, no increase in invalid accepts on the same negative/control set, HQ raw→accepted results unchanged, performance gate passes.

**FAIL:** revert immediately. A different cause must be traced.

**Regression:** HQ replay/physical, rejection reason distribution, tracker/CURRENT_TARGET/Fusion, CPU/FPS.

## E09 — Preprocessing/scale A/B (only if E07 localizes upstream scale issue)

**Purpose:** test the smallest evidence-based preprocessing alternative.

**Candidates:** exact current transform versus one ROI/crop/scale strategy justified by the trace. No model replacement in same experiment.

**PASS:** raw localization/detection improves on positives without unacceptable false positives/localization errors on controls; HQ unaffected; resource gate passes.

**FAIL:** revert. Do not compound with threshold/model changes.

## E10 — Camera configuration A/B (only if source image quality is implicated)

**Purpose:** distinguish optics/capture from detector limitations.

**Change:** one focus/exposure/gain/mode variable at a time; log source image evidence.

**PASS:** source quality and raw detection improve repeatably with same downstream pipeline.

**FAIL:** restore original camera control.

## E11 — NanoTracker freshness / CA update eligibility check

**Purpose:** resolve the reported but not repository-located stale-measurement integration concern without reopening CA mathematics.

**Method:** use a known detection-gap fixture/controlled replay. Record for every CA update: detector observation time, tracker observation source/time/age, fresh flag, measurement used, CA update executed, confirmation/stability counters.

**PASS:** no retained/stale tracker measurement is presented as a new observation unless the current explicit contract intentionally defines that behavior and the downstream semantics identify it correctly.

**FAIL:** localize integration defect; fix class is observation-freshness/update-eligibility contract only. Do not retune Q/R/state equations.

## E12 — Secondary HEF current overhead A/B

**Purpose:** quantify current synchronous shadow cost after upstream correctness is stable.

**State:** matched HQ baseline; Secondary OFF versus current intended cadence, primary/PVF/scene/pacing fixed.

**Measure:** Hailo wait/run latency distribution, processing/end-to-end FPS, stalls, CPU/RSS.

**PASS:** overhead quantified; current architecture remains above owner normal-tracking gate and resource limits.

**FAIL:** Secondary architecture/cadence becomes a performance-recovery candidate, but functional authority remains primary. Any scheduling change is separate and reversible.

## E13 — Telemetry/API/JPEG cost isolation

**Purpose:** distinguish Vision hot-path cost from observability/presentation.

**Sequence:** no browser/no JPEG requests → telemetry client only → one Tactical browser → bounded preview requests. Change one client condition at a time.

**Measure:** telemetry build/deep-copy/serialization/JPEG/API times, request counts, payload bytes, FPS/CPU/RSS.

**PASS:** costs attributed without changing Vision behavior.

**FAIL:** if client state is uncontrolled, classify methodology failure and repeat.

## E14 — Dual-camera staged cost ladder

**Purpose:** isolate where dual-camera cost appears.

**A/B ladder:**

1. HQ-only control.
2. HQ + WIDE capture only.
3. + WIDE preprocess.
4. + WIDE inference shadow, no tracker.
5. Mode B asymmetric dual.
6. Mode A full dual, only if still justified.

At each step record incremental delta in stage ms, both FPS metrics, CPU/RSS/temp/throttle and tracking freshness.

**Stop rule:** if a step fails owner normal-tracking gate or destabilizes HQ, do not proceed to more expensive steps until the cause is resolved or that architecture is rejected.

## E15 — Mode B functional evaluation

**Purpose:** test whether WIDE provides useful wide-area acquisition/ROI/event/geometric observations while HQ remains authoritative.

**PASS:** repeatable acquisition/coverage benefit, source/time provenance valid, HQ track quality unchanged, performance passes.

**FAIL:** prefer Mode C unless a separately justified experiment exists.

## E16 — Mode A incremental-value evaluation

**Purpose:** determine whether a WIDE authoritative tracker adds material value beyond Mode B.

**Prerequisite:** Mode B PASS.

**PASS:** demonstrated tracking/continuity/coverage benefit requiring WIDE tracker, cross-camera association correct, performance/stability pass.

**FAIL:** reject Mode A and retain Mode B/C. Do not promote full dual because it is more feature-complete.

## E17 — Calibration boundary

**Purpose:** prepare metric dual use only after Vision functional/performance choice.

**Measure:** physical intrinsics/distortion for each camera, relative extrinsic pose/baseline, synchronized timestamps, known-distance/geometry evaluation. HQ long-range focus must pass first.

**PASS:** calibration/evaluation evidence supports stated metric errors. Does not itself prove reliable 3D.

**FAIL:** dual geometry remains advisory/not promoted; detection/tracking mode can still be evaluated independently.

## E18 — Retained-candidate full regression

Every retained change must pass:

- protected HQ physical-object path where available;
- locked historical/replay detector cases;
- raw/accepted filter distributions;
- NanoTracker continuity/freshness;
- CA behavior with mathematics unchanged;
- Object Resolver stable bounded identity/state;
- CURRENT_TARGET acquisition/reacquisition/reset behavior;
- Fusion inputs/authoritative outputs;
- telemetry/API/Dashboard compatibility;
- camera acquisition and Hailo release;
- OFF→STANDBY / start-stop lifecycle;
- labeled >=25 normal-tracking owner gate;
- end-to-end throughput and latency report;
- CPU/RSS/temp/throttling and bounded stability.

## Keep/revert rule

A candidate is kept only after its direct objective, regression suite and performance gates all pass. If any gate fails, revert to the pre-experiment checkpoint before proceeding. Never stack an unvalidated second fix on top of a failed/ambiguous first change.
