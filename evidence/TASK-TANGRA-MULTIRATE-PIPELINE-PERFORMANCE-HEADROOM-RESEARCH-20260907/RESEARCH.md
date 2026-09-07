# RESEARCH — TANGRA MULTI-RATE PIPELINE / PERFORMANCE HEADROOM

TASK_ID: TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907
STATUS: REVIEW
MODE: RESEARCH / FORENSIC DESIGN REVIEW ONLY

## A. OVERALL_VERDICT

**VERDICT: RESEARCH-SUPPORTED ARCHITECTURAL DIRECTION; PRODUCTION SAFETY NOT VERIFIED.**

Separating HQ optical/metric acquisition geometry from 640x640 detector geometry is architecturally sound **if and only if** the camera-geometry probe establishes the actual acquisition transform and bbox mappings are explicit. The wider multi-rate principle is well established in real-time vision systems: expensive detector inference can run at a lower cadence while a tracker processes intermediate frames. NVIDIA DeepStream explicitly supports detector inference intervals larger than zero while the tracker continues to receive uninferenced frames. Published work also shows that fixed frame skipping is a baseline and that adaptive detect-vs-track scheduling can outperform uniform skipping when tracking quality varies.

For TANGRA, this means the concept is **STRENGTHENED**, not validated. The decisive risk is not nominal detector Hz; it is the age and quality of the last trustworthy observation during fast motion, occlusion, target scale change, or tracker uncertainty growth.

A TANGRA multi-rate architecture should therefore be designed around four invariants:
1. camera/authoritative temporal state must not block behind expensive work;
2. expensive asynchronous branches must consume the newest admissible frame/state, not a stale FIFO backlog;
3. all cross-rate data must carry capture timestamps/frame IDs and freshness/age;
4. cadence reductions are accepted only if tracking, reacquisition, CA error, range/HOROS freshness, and worst-case latency remain within baseline envelopes.

## B. MULTI_RATE_ARCHITECTURE_ASSESSMENT

### HQ acquisition / detector split
The source idea is architecturally beneficial because camera calibration belongs to optical acquisition geometry, whereas a detector's 640x640 tensor is a model contract. Coupling them unnecessarily can constrain metric geometry and performance. Separation permits a calibration-consistent acquisition stream and a deterministic detector transform without changing the model.

**Benefits:**
- removes detector tensor size from camera optical-geometry authority;
- allows metric/range/HOROS to use calibration-consistent coordinates;
- allows Hailo cadence to be tuned independently of camera FPS;
- creates a clean place to record detector transform provenance;
- permits performance experiments without changing NanoTracker/CA algorithms.

**Failure modes / hidden costs:**
- higher-resolution HQ acquisition can increase ISP, memory-bandwidth, copy, resize, and cache pressure even if detector Hz is reduced;
- asynchronous inference can increase latency if frames queue rather than being dropped/replaced;
- detector results can arrive after the tracker has advanced several frames, requiring frame-ID/time-aware association;
- a detector result computed on an old frame must not overwrite a newer authoritative track state naively;
- lower detector cadence increases drift/reacquisition exposure under occlusion, high angular acceleration, rapid scale change, or target appearance change;
- decimating measurement updates can make range and HOROS observations stale even when tracker position remains continuous.

### Queue architecture
Real-time vision should prefer **bounded latest-frame/latest-value semantics** on expensive branches. GStreamer explicitly documents bounded queues and leaky/drop-old-buffer behaviour to prevent memory growth and real-time degradation when consumers cannot keep up. The architectural principle is applicable to TANGRA even if TANGRA does not use GStreamer directly: expensive branches must have a bounded queue, normally depth 1 or another explicitly justified small bound, with stale age instrumentation.

### Asynchronous inference
HailoRT provides asynchronous inference APIs and examples, so Hailo itself does not require the entire application pipeline to be synchronous. However, async execution is useful only if result ordering, frame provenance, backpressure, and stale-result rejection are explicit.

## C. FIXED_VS_ADAPTIVE_INFERENCE_CADENCE

### Fixed cadence N=1..6
**Recommended as the first benchmark methodology, not as the presumed production policy.**

Advantages:
- deterministic and easy to compare;
- exposes the knee where quality begins to degrade;
- establishes detector-Hz sensitivity of NanoTracker, CA, CurrentTarget, range, and HOROS;
- gives reproducible performance/quality curves.

Weaknesses:
- wastes detector cycles during easy/stable tracking;
- can skip the exact frames where manoeuvre/occlusion/reacquisition requires detector support;
- frame-count cadence changes effective time interval when camera FPS varies.

### Adaptive cadence
Published detect-or-track work explicitly reports that uniform frame skipping is suboptimal because required detection frequency depends on tracking quality. Confidence-guided approaches similarly use lightweight tracking until confidence degrades, then invoke the expensive method.

For TANGRA, adaptive cadence is **RESEARCH-SUPPORTED / REQUIRES TEST** and should be evaluated only after the fixed sweep establishes safe bounds.

Potential triggers, in priority order:
1. tracker confidence/quality drop if NanoTracker exposes a reliable metric;
2. CurrentTarget lost/occlusion/reacquisition transition;
3. CA innovation/residual growth at detector measurement updates;
4. covariance/uncertainty growth or elapsed detector-observation age;
5. bbox centre velocity/acceleration increase;
6. bbox scale/aspect change rate;
7. high angular-rate/manoeuvre signal if a reliable carrier-motion signal is available;
8. periodic maximum-skip watchdog regardless of confidence.

A safe adaptive scheduler should have hard bounds: minimum detector cadence, maximum detector gap in milliseconds, immediate inference trigger for reacquisition/uncertainty events, and stale-result rejection.

## D. MODULE_BY_MODULE_CADENCE_MATRIX

| Module/path | Classification | Research assessment |
|---|---|---|
| HQ camera acquisition | MUST_RUN_EVERY_FRAME | Source of temporal truth; dropping at acquisition loses information. Acquisition rate itself may be configured separately but runtime frames should be timestamped continuously. |
| Calibration/deterministic coordinate transform metadata | MUST_RUN_EVERY_FRAME | Transform provenance/frame ID must accompany every frame used downstream; arithmetic may be cheap/static but mapping authority cannot be stale. |
| Hailo object detection | SAFE_TO_DECIMATE / UNKNOWN_REQUIRES_TEST | Strong candidate for N sweep; established detector+tracker pattern supports decimation, but TANGRA-specific safe cadence is unverified. |
| Hailo input resize/preprocess | EVENT_DRIVEN with detector | No need to execute on frames not sent to detector, unless shared elsewhere. |
| NanoTracker | MUST_RUN_EVERY_FRAME while target tracking is authoritative | Primary bridge between detector updates; skipping tracker frames would erase the core benefit of detector decimation. Do not redesign tracker. |
| CA Kalman prediction | MUST_RUN_EVERY_FRAME or every authoritative tracking timestep | Temporal prediction must advance with actual timestamps. Detector measurement correction can remain event-driven. Do not replace CA. |
| CA detector-measurement update | EVENT_DRIVEN | Only when a valid fresh detector observation is associated with the correct frame/track. |
| CurrentTargetManager | EVENT_DRIVEN + PERIODIC freshness/timeout evaluation | Arbitration events on detections/tracks; age/lost/expiry semantics must continue independently of detector cadence. Exact current implementation needs benchmark validation. |
| Class-size range calculation | UNKNOWN / REQUIRES TEST | Formula is cheap; if tracker bbox is accepted as authoritative for range, every-frame update may be preferable. If range requires detector-class measurement, measurement freshness becomes detector-rate. Do not decimate merely for CPU savings without profiling. |
| HOROS state prediction | MUST_RUN_EVERY_STATE_TIMESTEP | Prediction should remain temporally continuous with timestamps. |
| HOROS measurement update | EVENT_DRIVEN / ASYNC_LATEST_VALUE | Fresh spatial measurements can update at their native cadence; expensive measurement derivation may be decimated only after accuracy testing. |
| WIDE environment perception/mapping | SAFE_TO_DECIMATE / ASYNC_LATEST_VALUE / REQUIRES TEST | Likely strong candidate if not in control-critical loop. Must use bounded latest-frame semantics and explicit age. |
| Fusion/Object Resolver secondary expensive analysis | ASYNC_LATEST_VALUE / EVENT_DRIVEN / REQUIRES TEST | Suitable if authoritative target path remains protected; exact dependencies must be traced before experiment. |
| Dashboard telemetry publish | PERIODIC / ASYNC_LATEST_VALUE | Human UI does not require camera-frame rate. 4-10 Hz is a test range, not a production recommendation. |
| Dashboard live preview | EVENT_DRIVEN / on demand | Existing design intent already favours preview only when requested; keep outside core loop. |
| Radio/telemetry reporting | PERIODIC independent bounded rate | Must be independent of vision backlog. Safety/control messages must retain their own required cadence; do not infer a safe Hz without protocol tests. |
| Command/actuation path | MUST NOT BE COUPLED TO EXPENSIVE VISION QUEUES | Protected. No cadence change proposed. |
| Logging | ASYNC_LATEST_VALUE / EVENT_DRIVEN / PERIODIC batching | High-volume diagnostic logging is a common performance sink. Bounded async logging and selective high-rate traces are candidates; critical events must not be lost. |
| Dataset frame capture | EVENT_DRIVEN / bounded | Disable or decimate outside explicit capture campaigns. Must not silently contend with production bandwidth. |
| Diagnostics/profiling | EVENT_DRIVEN / PERIODIC | Keep off hot path except during bounded benchmark runs. |

## E. TOP_PERFORMANCE_OPPORTUNITIES

Priority uses qualitative EXPECTED_GAIN / IMPLEMENTATION_RISK / QUALITY_RISK / VALIDATION_COST.

1. **Hailo detector cadence** — Gain HIGH; implementation risk MEDIUM; quality risk HIGH; validation cost HIGH. Largest obvious compute candidate, but only acceptable after full tracking/reacquisition benchmark.
2. **WIDE environment cadence + latest-frame async** — Gain MEDIUM-HIGH; implementation risk MEDIUM; quality risk MEDIUM; validation cost MEDIUM-HIGH. Strong candidate if it is not authoritative for target lock/control.
3. **Remove stale-frame queuing / enforce bounded latest-frame branches** — Gain may be indirect but latency benefit HIGH; implementation risk MEDIUM; quality risk LOW-MEDIUM; validation cost MEDIUM. Prevents throughput optimisation from becoming latency regression.
4. **Dashboard publish/render cadence** — Gain LOW-MEDIUM; implementation risk LOW; quality risk LOW; validation cost LOW. Cheap early experiment.
5. **Logging/diagnostic cadence and batching** — Gain LOW-MEDIUM but can become HIGH under verbose modes; implementation risk LOW-MEDIUM; quality risk LOW if evidence paths remain intact; validation cost LOW-MEDIUM.
6. **HOROS expensive measurement-update cadence** — Gain UNKNOWN-MEDIUM; implementation risk MEDIUM; quality risk MEDIUM-HIGH; validation cost HIGH. Prediction must remain high-rate; only expensive measurement derivation is a candidate.
7. **Telemetry publish cadence** — Gain LOW; risk depends on path. Do not touch safety/control frequencies without protocol-specific evidence.

## F. FAILURE_MODES

1. **Stale inference result:** detector finishes frame F while tracker is at F+k; result applied without temporal alignment.
2. **FIFO latency spiral:** processing cannot keep up, queue grows, throughput looks acceptable while observation age becomes unacceptable.
3. **Tracker drift:** skipped detector updates allow visual tracker error to accumulate.
4. **Missed manoeuvre:** fixed N happens to skip sharp acceleration/turn/scale change frames.
5. **Occlusion/reacquisition delay:** detector unavailable when tracker loses target.
6. **Identity/target authority error:** late detection is associated with wrong CurrentTarget generation.
7. **Range staleness:** track remains visually continuous while physical size/range measurement is older than assumed.
8. **HOROS stale measurement:** prediction continues but covariance/measurement age is hidden from consumers.
9. **Timestamp error:** algorithms assume constant frame step even with skipped/dropped/async frames.
10. **High-resolution acquisition regression:** geometry is corrected but memory bandwidth/ISP/copies reduce system headroom more than detector decimation recovers.
11. **Adaptive scheduler oscillation:** inference rapidly toggles between rates and adds jitter.
12. **Confidence false security:** tracker confidence remains high during systematic drift.
13. **Benchmark blind spot:** average FPS passes while p95/p99 latency, minimum FPS, or stale-frame age fails.
14. **Instrumentation overhead:** benchmark logging itself changes performance; instrumentation cost must be measured.

## G. BENCHMARK_PLAN

### Phase 0 — Geometry correctness gate
Before performance optimisation, complete the planned Picamera2/libcamera dual-mode geometry probe. Do not benchmark an architecture whose metric geometry is still ambiguous.

### Phase 1 — Baseline profile N=1
Record synchronized timestamps/frame IDs at capture, detector submit, detector complete, tracker update, CA update, range update, HOROS update, CurrentTarget changes, and publish points.

Minimum metrics:
- camera FPS and inter-frame jitter;
- Hailo inference Hz and inference latency distribution;
- end-to-end observation age/latency distribution;
- minimum FPS plus p1/p5/median/p95 where useful, not average only;
- detector misses / confidence distribution;
- NanoTracker continuity and failure events;
- CurrentTarget resets/reacquisitions;
- CA prediction error/innovation on detector frames;
- sharp-manoeuvre error and recovery time;
- range update age/freshness/error;
- HOROS state and last-measurement age;
- CPU per process/thread where available;
- Hailo utilization/throughput where observable;
- RAM and memory bandwidth proxy/copy cost where measurable;
- queue depth, dropped frames, and maximum stale-frame age;
- logging/dashboard/WIDE time shares.

### Phase 2 — Fixed cadence sweep
Run N=2,3,4,5,6 under the same deterministic/replay and live test scenarios. Cadence must be time-aware: record actual milliseconds between detector observations, not N alone.

Use at least:
- stable lock;
- target crossing / background clutter;
- rapid lateral motion;
- rapid scale change/approach;
- sharp manoeuvre;
- partial occlusion;
- full short occlusion + reacquisition;
- low-confidence/small-target segment;
- target entry/new acquisition.

### Phase 3 — Isolated non-detector savings
Hold N=1 and independently test Dashboard, WIDE, logging/diagnostic, and other candidate cadence changes so gains are attributable.

### Phase 4 — Compound configuration
Combine only individually accepted savings and re-run the full benchmark. Do not sum isolated gains as if they were independent.

### Phase 5 — Adaptive scheduler research benchmark
Only after fixed safe bounds are known, compare adaptive policy against the best fixed N at matched compute budget and matched quality envelope.

## H. ACCEPTANCE_CRITERIA

The goal is **headroom with no material regression**, not peak FPS.

A candidate cadence/configuration is acceptable only if all are true against N=1 validated baseline:
1. sustained core FPS remains >25 FPS and no test segment falls to <=25 FPS under the defined operational benchmark;
2. a separate design-reserve target is established from measured future-module budget rather than guessed. Research recommendation: report margin above 25 as `reserve_fps` and `reserve_frame_time_ms`; do not yet freeze a numeric reserve without profiling;
3. end-to-end p95/p99 latency and maximum stale-frame age do not materially regress beyond explicit limits;
4. tracker continuity is non-inferior within agreed statistical tolerance;
5. CurrentTarget reset/reacquisition count and reacquisition latency are non-inferior;
6. CA prediction/innovation error on manoeuvre segments remains within validated tolerance;
7. detector miss behaviour does not create longer unobserved intervals than the allowed maximum detector gap;
8. range freshness/error and HOROS measurement age remain within required operational bounds;
9. no unbounded queue growth; bounded queue depths remain within configured maximum and stale frames are dropped/rejected;
10. CPU/RAM/Hailo/memory-bandwidth metrics demonstrate actual recovered capacity, not only redistributed bottlenecks.

**Design reserve:** >25 FPS is a survival gate, not necessarily adequate future headroom. Establish reserve as remaining frame-time budget at the worst relevant percentile. Example reporting form at 30 FPS camera rate: 33.3 ms frame budget; measure p95 core work and preserve a defined unused fraction for future modules. The fraction must be selected from actual roadmap load, not research guesswork.

## I. EXPECTED_COMPOUND_HEADROOM

No defensible numeric FPS gain can be claimed before profiling. Gains are governed by Amdahl-like behaviour: reducing a module that consumes fraction `p` of frame time by factor `r` changes total time approximately to `T_new = T_total * ((1-p) + p/r)` before secondary effects. Therefore detector cadence N=2 does **not** imply 2x system FPS; it at most halves detector-invocation contribution, and higher-resolution acquisition may add new cost.

Several modest savings can compound materially if they attack independent portions of frame time and do not add synchronization overhead. The correct research expectation is:
- detector cadence: potentially largest single saving;
- WIDE + logging + dashboard: smaller independent savings;
- bounded latest-frame async: primarily latency/headroom protection rather than guaranteed throughput gain;
- HOROS measurement decimation: possible further saving only if profiling shows it is expensive.

Compound benefit must be measured from the integrated configuration because memory bandwidth, thread scheduling, Hailo/CPU overlap, and cache effects are non-linear.

## J. RECOMMENDED_ORDER_OF_EXPERIMENTS

1. **Complete HQ camera-geometry probe first.** Metric correctness precedes performance optimisation.
2. Instrument frame IDs/timestamps, detector submit/complete, queue depth, observation age, CurrentTarget events, CA/range/HOROS freshness.
3. Establish N=1 baseline with latency distributions and minimum-FPS data.
4. Run fixed detector cadence sweep N=2..6 with unchanged NanoTracker/CA.
5. Identify first quality knee and maximum safe detector gap in milliseconds.
6. Independently test Dashboard publish and logging/diagnostic cadence reductions.
7. Independently test WIDE asynchronous/decimated cadence with latest-frame semantics.
8. Profile HOROS to determine whether any expensive measurement path is worth decimating; keep prediction high-rate.
9. Combine only PASSed isolated changes and re-benchmark for compound headroom.
10. Only then test adaptive detector scheduling within the safe min/max cadence envelope using confidence/innovation/motion/occlusion triggers.
11. Compare adaptive policy to best fixed cadence at equal or lower compute and equal quality, including worst-case manoeuvre/reacquisition tests.

## K. WHAT_NOT_TO_CHANGE

- Do not redesign or replace NanoTracker.
- Do not replace CA Kalman or change its validated authoritative role.
- Do not change HQ calibration based on performance research.
- Do not change 640x640 Hailo model input as part of this research.
- Do not change CurrentTarget authority semantics without a separate task.
- Do not couple command/actuation timing to decimated vision branches.
- Do not use unbounded queues or process stale FIFO frames merely to avoid drops.
- Do not accept average FPS as sufficient evidence.
- Do not use a fixed empirical detector cadence without benchmark evidence.
- Do not assume adaptive confidence is trustworthy until correlated with actual tracking error.
- Do not decimate cheap metric calculations simply because they are present; profile first.

## External research basis

- NVIDIA DeepStream `gst-nvtracker` documentation: detector inference may be skipped on intervals while tracker continues on uninferenced frames: https://docs.nvidia.com/metropolis/deepstream/7.1/text/DS_plugin_gst-nvtracker.html
- Luo et al., AAAI 2019, "Detect or Track: Towards Cost-Effective Video Object Detection/Tracking": fixed frame skipping is a baseline; detection frequency should depend on tracking quality: https://ojs.aaai.org/index.php/AAAI/article/view/4906
- GStreamer appsink/queue documentation: bound queues and drop/leak buffers to prevent memory/backlog and real-time blocking: https://gstreamer.freedesktop.org/documentation/app/appsink.html and https://gstreamer.freedesktop.org/documentation/coreelements/queue.html
- HailoRT asynchronous inference examples/discussion: async inference is supported and queue capacity/backpressure exists: https://community.hailo.ai/t/hailort-minimal-working-example-for-python-and-hailo8/7685 and https://community.hailo.ai/t/handling-input-and-output-for-asynchronous-inference-with-hailort/13948
- Lee, Sensors 2024, confidence-guided frame skipping: expensive processing invoked based on tracking confidence rather than uniformly: https://www.mdpi.com/1424-8220/24/24/8120

STOP
