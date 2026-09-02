# PERFORMANCE PROFILING PLAN

TASK_ID: `TASK-059`  
Purpose: locate frame-time and resource cost without changing Vision behavior.

## 1. Measurement contract

Use `time.perf_counter_ns()` or the authoritative monotonic equivalent. Every frame receives a stable `frame_id`, `camera_id`, capture timestamp and monotonic trace root. Instrumentation must be bounded, switchable and non-authoritative.

For every stage report:

`STAGE | MEAN_MS | P50 | P95 | MAX | CALLS_PER_FRAME | CADENCE | CPU_EFFECT | FPS_EFFECT`

Also persist test-level:

- `FPS_VALUE`
- `FPS_METRIC_TYPE`
- `MEASUREMENT_LOCATION`
- `DURATION`
- `CAMERA_STATE`
- `DETECTOR_STATE`
- `TRACKING_STATE`
- `PRIMARY_HEF_STATE`
- `SECONDARY_HEF_STATE`
- `DASHBOARD_STATE`
- CPU process and system values with denominator semantics
- RSS / RAM
- temperature
- throttling flags
- Hailo queue/scheduling state where available
- pacing/sleep configuration
- source fixture/hash or physical-scene identity

Do not calculate one FPS value and label it generically.

## 2. Required FPS counters

### A. Processing-loop FPS

Measure from the start/end of processing work **excluding deliberate post-loop pacing/sleep**, if such pacing exists. This is the closest historical comparator to the documented Dashboard instantaneous counter, but Codex must verify current source semantics rather than assume continuity.

Report rolling 1 s and full-window mean/median/P95 frame-processing duration. Avoid `1 / last_frame_time` as the sole acceptance metric because it exaggerates periodic Secondary HEF jitter.

### B. End-to-end processed FPS

Measure completed authoritative frames per monotonic wall interval including capture wait, all processing, publication and configured pacing. This is the true delivered throughput.

### C. Camera capture FPS

Measure successful source frames delivered by each camera worker independently. Do not call this Vision FPS.

### D. Inference FPS / latency

Record primary and Secondary HEF invocation counts and latency. For dual-camera experiments also record model-camera scheduling order and queue wait separately from execution time.

## 3. Stage instrumentation matrix

| Stage | Timing boundary | Minimal method | Extra counters / interpretation |
|---|---|---|---|
| Camera acquire | immediately before request/read → frame available | monotonic delta around existing capture call | camera_id, source resolution/format, dropped/late frames, sensor timestamp if exposed |
| Camera worker queue | frame produced → frame consumed | timestamp frame at producer and consumer | queue depth, overwrite/drop count; separates sensor/capture from scheduler delay |
| Frame copy | before → after explicit copy/array conversion | wrap only explicit copies | bytes copied, shape/dtype; identify accidental multi-copy dual path |
| Colour conversion | before → after cv/array conversion | direct timer | source/destination formats and bytes |
| Crop / resize / letterbox | before → after each transform | independent timer per operation | input/output dimensions, interpolation, ROI, target bbox dimensions for diagnostic fixtures |
| Tensor preparation | preprocessed image → Hailo submit-ready tensor | timer | dtype/layout/normalization; bytes |
| Primary Hailo queue wait | submit intent → execution/start if API exposes | timestamp submit + start; otherwise bracket call and distinguish unavailable | camera_id/model_id; contention flag |
| Primary HEF inference | actual inference call | direct timer | raw output count; errors; Hailo status |
| Secondary HEF queue + inference | scheduler decision → completion | separate scheduled/skipped/wait/run timers | exact cadence, model_id, fail-open errors |
| Raw parser | raw output ready → parsed boxes | direct timer | raw tensor/object count |
| NMS / confidence | parsed candidates → post-NMS/confidence | timers around actual implementation boundaries | candidates in/out and threshold profile |
| Class/bbox/area/size filters | candidate input → accepted/rejected | aggregate timer plus per-reason counters | reason code counts; camera_id; bbox source/detector dimensions; avoid per-candidate heavy logging in sustained run |
| Object Resolver | accepted/track state → resolver output | timer | object count, association-history count, created/associated/expired counts; regression guard against July16 growth |
| NanoTracker | input detections → tracker output | timer | tracker count, new/update/lost, observation freshness/source/age |
| CA predict | pre-call → post-predict | timer | no mathematics change; state dimensionality/horizon metadata |
| CA update | eligible observation → post-update | timer | update executed yes/no; fresh-observation flag; measurement timestamp/age |
| Projection | pixel state → bearing/ray | timer | camera profile id; current vs predicted source |
| Range | bbox/class → range output | timer | profile id, uncertainty; duplicate-call count |
| CURRENT_TARGET | candidate states → target output | timer | acquisition/reacquisition/reset/no-change count |
| Fusion preparation | target/evidence → Fusion input | timer | payload size and source count; stop before HOROS-specific work |
| Fusion | Fusion input → output if in current Vision path | timer | selected source/state; no policy change |
| Telemetry build | runtime state → telemetry object | direct timer | payload field counts and approximate serialized bytes; dynamic-list sizes |
| Deep copy / snapshot | input object → copied state | direct timer around each known copy | payload bytes; copy count; historical July15 amplification candidate |
| JSON serialization | object → bytes | direct timer | byte count |
| Recorder / JSONL logging | enqueue/write boundary | preferably queue/enqueue time and actual write separately | bytes, flush/fsync behavior, queue depth, write stalls |
| JPEG encode | frame → JPEG bytes | direct timer | camera_id, resolution/quality, encode cadence |
| API publication | state/JPEG available → response built | request timer | endpoint, client count, response bytes, P50/P95; isolate browser load |
| Dashboard polling | external request cadence | access-log/request counters, not AI-loop instrumentation | `/telemetry`, health, frame/JPEG counts and latency |
| COMM/pacing/sleep | requested sleep start → wake | record configured and actual duration | historical 30 ms pacing consumed ~48% of live period; scheduler oversleep |
| GC / scheduler / I/O wait | sampled per bounded interval | process counters and GC callbacks where low overhead | correlate rare stalls; do not instrument every allocation |

## 4. Instrumentation overhead control

Before using timing data for acceptance:

1. Run a short `INSTRUMENTATION_OFF` control.
2. Run identical short `INSTRUMENTATION_ON` measurement with output buffered/bounded.
3. Compare FPS, CPU and RSS. If instrumentation changes normal FPS by more than the predeclared tolerance, reduce logging density or sample stages rather than accepting distorted data.
4. Do not stream per-frame JSON through the same production telemetry channel being measured.
5. Prefer local bounded ring buffer or append-only evidence file with periodic buffered flush.

The tolerance itself must be declared before the A/B; Workshop does not invent a numeric tolerance from absent evidence.

## 5. Baseline experiment set

Run on the authoritative isolated development copy in this order, using the same scene/replay and at least one repeat per state if time allows:

### P0 — HQ protected control

HQ only; primary HEF only if an authoritative historical-equivalent control is available; Dashboard closed/no client; preview/JPEG consumer disabled or unrequested; current required runtime logic otherwise unchanged.

Purpose: current matched HQ reference.

### P1 — HQ current operational feature set

HQ only with current PVF/Secondary/pacing states as intended for normal operation.

Purpose: quantify shadow/secondary overhead versus P0; do not change them yet.

### P2 — WIDE capture only

HQ authoritative Vision unchanged; WIDE capture worker active but no WIDE inference/tracker.

Purpose: isolate second-camera acquisition/copy/format cost.

### P3 — WIDE acquisition / preprocessing only

Add actual intended WIDE preprocess path but no WIDE Hailo inference.

Purpose: isolate CPU/memory preprocessing cost.

### P4 — WIDE inference shadow, no authoritative tracker

Run WIDE inference at declared cadence; retain HQ authority; no WIDE tracker.

Purpose: isolate Hailo scheduling/inference cost and functional raw-detection evidence.

### P5 — Mode B candidate

WIDE watch/acquisition/event/ROI/geometric observation at empirically justified cadence, HQ authoritative tracking.

Purpose: evaluate asymmetric architecture.

### P6 — Mode A candidate

Only after P5 and upstream filtering are understood: WIDE detection+tracking + HQ detection+tracking.

Purpose: evaluate full dual architecture. Do not run if earlier evidence already proves performance infeasible or functional value absent.

### P7 — Dashboard/client load

Repeat selected viable mode with zero browser client, one Tactical client, and on-demand preview requests at bounded known cadence.

Purpose: separate runtime Vision cost from observability/presentation cost.

## 6. Resource gates and failure classes

### Performance fail

- Owner-designated normal tracking FPS <25.
- Or matched HQ baseline materially regresses due to the candidate, even if a different unlabeled FPS counter remains >25.
- Or latency/freshness becomes incompatible with authoritative tracking despite average FPS passing.
- Or thermal throttling appears under a sustained bounded test where HQ control did not throttle.
- Or unbounded/monotonic RSS/object/queue growth appears.

### Functional fail

- WIDE still cannot produce useful accepted detections under the intended scene/range despite trace-correct rules.
- HQ detection/tracking/CA/CURRENT_TARGET/Fusion behavior regresses.
- camera identity or coordinate transforms become ambiguous.

### Methodology fail

- FPS metric unlabeled or changes between A/B.
- source fixture/scene changes materially.
- camera/HEF/Dashboard/pacing state differs unintentionally.
- test harness false-fails on resource release (historical July22 lesson).
- no instrumentation-overhead control exists when instrumentation cost is material.

A methodology fail is not a production implementation fail.

## 7. Sustained validation after a candidate passes

Short stage profiling finds hotspots; it does not establish stability. A retained candidate should receive a bounded sustained run sufficient to detect RSS/object/queue drift and thermal behavior, followed by clean OFF/STANDBY lifecycle validation. Workshop does not mandate a new 12/24-hour run at this pre-Codex stage; duration should be chosen after current short-run drift is measured.
