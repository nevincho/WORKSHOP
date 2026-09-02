# VISION RECOVERY CODEX HANDOFF

Mode: Token conservation. No long reasoning. No extra architecture discussion. Do the task and report only facts.

- `TASK_ID`: TASK-059
- `FROM_ROLE`: WORKSHOP Control Room / reviewed pre-Codex forensic campaign
- `TO_ROLE`: Codex integration/runtime investigator
- `PROJECT`: TANGRA — DroneGuard Vision recovery
- `STATUS`: **READY_FOR_CODEX_REVIEW — HUMAN GATE REQUIRED BEFORE EXECUTION**
- `OBJECTIVE`: Reconcile the authoritative development copy, preserve the HQ IMX477 + 50 mm baseline, trace current Vision end-to-end, measure labeled performance, locate the first current divergence and execute controlled one-change fixes with rollback/regression gates. Do not implement HOROS in this task.

## 1. Absolute rules

1. `NO FIX BEFORE TRACE`.
2. Production stays untouched. Work only on the isolated authoritative development copy after verifying its identity.
3. Before changes, create/verify an immutable snapshot of the current proven HQ-centric line and a usable rollback path.
4. HQ IMX477 + 50 mm detection/tracking must remain independently activatable without WIDE/dual dependencies.
5. Do not reopen/retune CA Kalman mathematics without new direct evidence. Freshness/update-eligibility integration may be tested.
6. Do not treat TANGRA-2.0 or HOROS Workshop artifacts as current DroneGuard runtime architecture.
7. Do not assume WIDE must become a full tracker and do not assume it must be abandoned.
8. Functional pass without performance pass is architecture fail for promotion.
9. Never compare unlabeled FPS values.
10. One change per A/B. If a candidate fails, revert before the next candidate.

## 2. Evidence classification

### VERIFIED FACT — historical/documented

- DroneGuard 1.0 was promoted as official protected stable baseline on 2026-07-10. The promotion report lists 360 frames, 356 detections, zero track drops and FPS `40.706863`; that report does not define the FPS metric type.
- CA Kalman historical replay comparison strongly outperformed the OpenCV/CV alternative: official CA overall mean detector-linked error approximately `5.649 px` versus `486.894 px`. This supports protection of CA math; it is not absolute positional ground truth.
- July16 Object Resolver regression was proven historically: new object each frame, ~29,138 objects retained, FPS ~14.59–17.52; validated cap/reuse correction restored stable object counts and reported FPS ~30.06–40.96. Treat as regression check, not current assumed cause.
- July27 source/measurement audit proved the then-current displayed `fps` was current-loop processing rate calculated before a configured 30 ms sleep, not true end-to-end throughput.
- Controlled July27 tests measured true end-to-end live `15.973 FPS`, replay `14.927 FPS`; reconstructed processing-only live rates were approximately `40.51` primary-only, `20.61` primary+secondary and `30.65` amortized.
- Secondary HEF exact 1:3 synchronous execution historically added ~24 ms every third loop. Controlled replay deep stalls were traced to Hailo inference latency in both primary and Secondary HEFs.
- July15 degradation: FPS 24.77→19.95, CPU58.6→69.9%, RSS392→434 MB. Combined removal of world-map publication and global Tactical JPEG polling improved CPU trend and produced31.40→28.63, but RSS growth and smaller decline remained; neither was proven sole cause.
- Historical camera metric-chain audit found no complete physical calibration: runtime/nominal FOV models differed; physical intrinsics/distortion/principal point absent; extrinsics/attitude absent; projection/range/time ownership incomplete. Do not transfer HQ detector/tracker validation to metric 3D accuracy.
- August14 replay/software acceptance: 3098 frames, 2918 raw, 2799 accepted, `REJECT_SIZE=119`, CURRENT_TARGET continuity PASS; controlled live target validation deferred. Production promotion documented FPV two-axis pre-track size gate and CURRENT_TARGET continuity layer.

### CURRENT SUPPLIED EVIDENCE — MUST RECONCILE

- WIDE IMX708 supplied current camera0 `/dev/media2`, full 4608×2592; HQ IMX477 + 50 mm supplied camera1 `/dev/media3`, full4056×3040; physical baseline35.6 mm; both operational; physical calibration incomplete.
- Bounded standard path: `4 raw → 3 accepted → 3 tracks → CA updates → TRACKING`.
- Bounded WIDE/HOROS shadow: **identical raw Hailo outputs → 0 accepted**, supplied reason: WIDE physical-size/class-area gate rejected all four.
- Separate WIDE test: source target approximately110×55 px at 4608×2592 → approximately15×14 px after current preprocessing → raw detector result0.

These are two separate diagnostic observations. Do not merge them.

### OWNER REQUIREMENT

`NORMAL TRACKING RUNTIME <25 FPS = PERFORMANCE FAIL`.

The metric must be explicitly identified before applying the gate. Report both processing/pre-sleep (or authoritative equivalent) and true end-to-end processed FPS. No promotion on a generic `fps` field.

### HYPOTHESIS — NOT PROVEN CURRENT

Ranked starting points:

1. WIDE physical-size/class-area acceptance assumption mismatch or coordinate/profile error.
2. WIDE target-scale loss through preprocessing / detector small-target limit.
3. WIDE camera focus/exposure/mode issue.
4. camera identity/profile propagation error.
5. current Secondary HEF synchronous overhead.
6. current pacing/sleep throughput limit.
7. telemetry/deep-copy/JPEG/client cost.
8. Object Resolver regression recurrence.
9. Hailo latency stalls.
10. NanoTracker retained/stale observation presented as fresh to CA.
11. model/HEF domain/scale limitation.
12. dual-camera resource/Hailo contention.

Do not fix in this order automatically. The current trace chooses the first experiment.

### NOT VERIFIED

- authoritative development-copy file tree/current source behavior;
- current camera mode/controls/profile mapping;
- current preprocessing/filter constants;
- current FPS semantics/pacing;
- matched present-day HQ-only baseline;
- current dual-camera performance;
- physical intrinsics/extrinsics;
- exact historical TANGRA-DOCS artifact for the reported stale-NanoTracker-to-CA shadow freshness defect. Bounded search did not locate it; treat the freshness concern as a check, not a proven defect.

## 3. Protected components

- HQ IMX477 + 50 mm detection/tracking behavior and independent fallback.
- CA Kalman mathematics/state equations unless new direct evidence authorizes a separate change.
- Object Resolver validated bounded identity behavior.
- CURRENT_TARGET mission continuity.
- Fusion authoritative input/output behavior.
- telemetry/API/Dashboard compatibility.
- Runtime Controller and OFF/STANDBY/start-stop behavior.
- Hailo clean ownership/release.
- production tree and canonical TANGRA-DOCS.
- command/actuation paths remain outside Vision repair.

## 4. Files/interfaces to reconcile — names are historical navigation only

Locate the actual current equivalents before action:

- runtime entrypoint historically `main.py`;
- camera acquisition / historical `camera_manager.py`, Picamera2/libcamera configuration and any camera workers;
- runtime/config/profile files including camera identities, detector thresholds, size/area gates and pacing/sleep;
- Hailo primary wrapper/model hash/output parser/NMS;
- Secondary HEF scheduler/wrapper/model hash and cadence;
- detection filter functions: confidence, class, full-frame, bbox ratio/edge, area, physical/two-axis size;
- NanoTracker creation/update/output and observation timestamp/freshness ownership;
- CA predict/update call sites and measurement eligibility;
- historical `object_resolver.py` equivalent and retained-state bounds;
- projection/range modules historically `camera_projection.py`, `range_estimator.py`;
- `current_target_manager.py` equivalent;
- Fusion input preparation/runtime;
- telemetry build/publisher, historical `pi_api_server.py`, deep copies/serialization;
- recorder/JSONL/logging;
- JPEG/live-frame path and Dashboard/API polling/client behavior;
- Runtime Controller/service/start-stop configuration.

If current architecture differs, document the difference. The current implementation wins.

## 5. Required current trace

For one diagnostic frame in HQ and WIDE modes, record with `frame_id`, `camera_id` and monotonic timestamps:

`physical/fixture identity`
→ `camera model + source mode`
→ `source frame dimensions`
→ `source target bbox pixels`
→ `crop/resize/colour transform`
→ `post-preprocess target bbox pixels`
→ `Hailo tensor shape/order`
→ `primary inference latency`
→ `raw model outputs`
→ `parser/NMS output`
→ `confidence/class/bbox/area/size decision with explicit reason per rejection`
→ `accepted detections`
→ `NanoTracker input/output`
→ `observation source/time/age/freshness`
→ `CA update yes/no + predict`
→ `Resolver/CURRENT_TARGET`
→ `projection/range if present`
→ `Fusion input`
→ `telemetry build/copy/serialize`
→ `Dashboard/API consumers`.

Stop and identify the **first** incorrect/different boundary. Do not skip directly to the most plausible hypothesis.

## 6. Performance record contract

Every performance experiment must record:

- FPS_VALUE
- FPS_METRIC_TYPE
- MEASUREMENT_LOCATION
- DURATION
- CAMERA_STATE
- DETECTOR_STATE
- TRACKING_STATE
- PRIMARY_HEF_STATE
- SECONDARY_HEF_STATE
- DASHBOARD_STATE/client count
- pacing/sleep/COMM state
- CPU with denominator semantics
- RSS/RAM
- temperature
- throttling
- source fixture/hash/physical scene
- Hailo scheduling state

Stage output:

`STAGE | MEAN_MS | P50 | P95 | MAX | CALLS_PER_FRAME | CADENCE | CPU_EFFECT | FPS_EFFECT`.

At minimum time capture, copies, colour conversion, resize/crop, tensor prep, primary queue/inference, secondary queue/inference, parser/NMS/filter, Resolver, tracker, CA predict/update, projection/range, CURRENT_TARGET, Fusion preparation, telemetry build/deep-copy/JSON, recorder, JPEG, API publication and deliberate sleep/pacing.

Use a bounded monotonic profiler and run instrumentation OFF/ON overhead control before accepting measurements.

## 7. Exact ordered experiment sequence

### E00 — reconcile current implementation

Read-only. Produce current file/interface/config/model/camera/pacing map. PASS only when every required trace boundary is mapped or explicitly absent.

### E01 — snapshot/rollback

Create/verify immutable HQ-centric development snapshot and restoration method. No further modification if rollback is untrusted.

### E02 — FPS semantics

Map every current FPS counter and deliberate pacing. Declare the normal-tracking metric used for the owner >=25 gate and add independent true end-to-end measurement.

### E03 — profiler overhead control

Enable bounded profiler and compare identical instrumentation OFF/ON control. Reduce profiler if it materially distorts runtime.

### E04 — present-day HQ-only baseline

WIDE disabled/unavailable. Measure functional/replay and available physical HQ path, processing FPS, E2E FPS, stage latency, CPU/RSS/temp/throttle, Resolver counts, CURRENT_TARGET, Fusion, lifecycle. If HQ baseline itself is degraded, stop dual promotion and trace HQ first.

### E05 — full current Vision trace

Capture per-boundary evidence for HQ and WIDE diagnostic frames with explicit rejection reasons and camera provenance.

### E06 — reproduce `4 raw → 0 accepted`

If reproduced, identify exact filter predicate/input/profile causing first divergence. If raw outputs differ before filtering, move upstream and do **not** edit filter.

### E07 — reproduce source110×55 → preprocess15×14 → raw0

Record bbox after every transform plus focus/exposure/mode. If not reproducible, do not optimize for it.

### E08 — one filter A/B, conditional on E06

Change only the proven predicate/profile/coordinate input. PASS requires expected WIDE recovery, negative/control behavior acceptable, HQ unchanged and performance pass. Else revert.

### E09 — one preprocessing/ROI A/B, conditional on E07

Current transform versus exactly one evidence-based alternative. No threshold/model change in same experiment. PASS requires raw detection/localization benefit plus false-positive/localization controls, HQ regression pass and performance pass. Else revert.

### E10 — camera-control A/B, conditional

One focus/exposure/gain/mode variable at a time only if source image quality is implicated.

### E11 — NanoTracker freshness / CA eligibility

Use known detection gap. For every CA update record detector observation time, tracker source/time/age/fresh flag, measurement used and update executed. If stale retained state is treated as fresh, repair only integration/freshness contract; do not retune CA.

### E12 — Secondary HEF overhead

Matched HQ control with Secondary OFF vs current cadence. Primary/PVF/scene/pacing fixed. Quantify Hailo wait/run, stalls, both FPS metrics and resources.

### E13 — telemetry/JPEG/Dashboard cost

No browser → telemetry-only client → one Tactical browser → bounded preview requests. Attribute telemetry build/deep-copy/JSON/JPEG/API cost. Keep Vision algorithms unchanged.

### E14 — dual cost ladder

`HQ only → +WIDE capture → +WIDE preprocess → +WIDE inference shadow/no tracker → Mode B → Mode A only if justified`.

Stop before next step if owner FPS gate, HQ freshness, resource stability or Hailo lifecycle fails.

### E15 — Mode B functional decision

WIDE advisory watch/acquisition/ROI/event/geometric observation; HQ authoritative tracker/CA. PASS requires repeatable functional benefit, valid time/source provenance, HQ unchanged and performance pass.

### E16 — Mode A incremental-value decision

Only after Mode B PASS. Full WIDE tracker must demonstrate material incremental value requiring tracker authority, correct association and full performance/stability pass. Otherwise reject Mode A and retain B/C.

### E17 — calibration boundary

After upstream Vision mode selected: physical intrinsics/distortion both cameras, relative extrinsics, synchronized timestamps, HQ infinity focus and held-out known-geometry evaluation. Calibration does not automatically prove reliable 3D.

### E18 — final retained-candidate regression

Run HQ physical/replay, filters, tracker freshness/continuity, CA unchanged behavior, Resolver bounds, CURRENT_TARGET, Fusion, telemetry/API/Dashboard, camera/Hailo lifecycle, OFF/STANDBY and full performance/resource gates.

## 8. Dual-camera decision

### Mode C — mandatory HQ fallback

Must always remain available. Use as control and operational fallback.

### Mode B — first dual candidate

WIDE watch/acquisition/event/ROI/geometric observation; HQ authoritative detection/tracking/CA. Prefer when WIDE adds useful coverage but a WIDE authoritative tracker is unnecessary or too expensive.

### Mode A — conditional full dual

Both cameras detect/track. Accept only if it adds material benefit beyond Mode B, association is correct and normal runtime remains >=25 on the owner-designated metric with no HQ/resource regression.

Do not use weighted feature scoring. Apply gates in this order:

`HQ preservation → WIDE functional benefit → performance/stability → association/calibration prerequisites`.

## 9. Acceptance criteria for any retained Vision change

PASS requires all applicable:

- direct target defect reproduced before change;
- first divergence measured;
- one-change A/B supports predicted effect;
- protected HQ physical/replay behavior unchanged;
- raw/accepted detector regression acceptable;
- NanoTracker continuity/freshness correct;
- CA mathematics unchanged and behavior not regressed;
- Object Resolver state bounded/stable;
- CURRENT_TARGET continuity preserved;
- Fusion input/output compatibility preserved;
- telemetry/API/Dashboard compatible;
- camera/Hailo start/stop/release clean;
- Runtime OFF→STANDBY behavior preserved;
- owner normal tracking FPS >=25 with metric explicitly named;
- true end-to-end throughput and latency also reported;
- CPU/RSS/temp/throttling stable versus matched HQ control;
- rollback remains available.

If functional PASS but performance FAIL: **REVERT / ARCHITECTURE FAIL FOR PROMOTION**.

## 10. Non-goals

- no production change;
- no HOROS implementation/fix;
- no general TANGRA redesign;
- no Kalman retuning;
- no speculative model replacement before preprocessing/filter/camera trace;
- no lowering thresholds globally just to make WIDE detect;
- no claiming calibrated 3D from camera baseline alone;
- no refactor/deduplication that couples HQ fallback to WIDE;
- no unrelated Dashboard, flight-control, comms or hardware work.

## 11. Pre-change checkpoint / rollback

`PRE_CHANGE_CHECKPOINT`: must be created/verified by Codex from the authoritative development copy before implementation. Historical backup paths in TANGRA-DOCS are evidence only and must not be assumed to match the current development copy.

`ROLLBACK_METHOD`: exact repository tag/commit/archive restore plus configuration/model hashes, verified before first change. Each experiment gets its own reversible checkpoint/diff. Failed/ambiguous experiments revert before the next experiment.

## 12. Execution access state / Codex justification

- Workshop repository analysis: COMPLETE and reviewed.
- current authoritative development-copy access: reserved for Codex / NOT VERIFIED by Workshop.
- Pi5/production runtime actions: remain outside Workshop execution and human-gated.
- Codex is justified only for authoritative source reconciliation, instrumentation in the isolated development copy, hardware/runtime measurements and controlled fixes that Workshop cannot verify from documentation.

## 13. Package references

Read these only as needed; this handoff is the execution entrypoint:

- `VISION_RECOVERY_EXECUTIVE_SUMMARY.md`
- `HISTORICAL_PERFORMANCE_TIMELINE.md`
- `VISION_END_TO_END_TRACE.md`
- `HQ_WIDE_ASSUMPTION_MATRIX.md`
- `PERFORMANCE_PROFILING_PLAN.md`
- `ROOT_CAUSE_HYPOTHESIS_REGISTER.md`
- `DUAL_CAMERA_MODE_DECISION_MATRIX.md`
- `CODEX_CONTROLLED_EXPERIMENT_PLAN.md`
- `SOURCE_EVIDENCE_MANIFEST.md`
- `INDEPENDENT_REVIEW.md`

Do not rediscover broad historical documentation unless a specific contradiction in the authoritative current implementation requires it.
