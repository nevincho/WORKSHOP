# TANGRA-RESEARCH-LAB-03 — Worker Evidence

TASK_ID: TANGRA-RESEARCH-LAB-03

ROLE: WORKER

DATE: 2026-10-06

STATUS: REVIEW_REQUIRED

TARGET_CHANGES: NONE

PI_OR_RUNTIME_ACCESSED: NO

CODEX_USED: NO

## 1. Result boundary

The retained evidence establishes several bounded throughput, stage-duration, stale-policy and uptime observations, but it does **not** establish synchronized end-to-end perception age. Current aggregate FPS cannot be promoted to sensor-to-state latency, freshness, synchronization or physical accuracy. Exact source timestamps, cross-host clock provenance, queue residence, complete frame lineage and truth-aligned output times remain incomplete or `NOT VERIFIED`.

The current evidence does not show a qualifying present headroom failure: the bounded 180 s tracking run averaged 36.016 FPS and remained above the historical absolute 25 FPS floor, although 4 samples were below 30 FPS. This is not a guarantee under airborne or full concurrent load. Optimization remains **HOLD** until a current, semantically correct measurement fails a preregistered criterion.

## 2. Exact refs and source ledger

Qualified refs, rechecked 2026-10-06:

- `nevincho/TANGRA-DOCS@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba` (tree `ec100918...`);
- `nevincho/TANGRA-CL@7a720af7fe5b4321b1ba47c8d2be58c815677fd7` (tree `791fbb79e2b484b6c7571f70d40eb76b4347c0dd`).

| ID | Exact source at qualified ref | Date | Principal use |
|---|---|---:|---|
| S01 | TANGRA-DOCS `CURRENT_SYSTEM.md` (blob `b8ca493...`) and `CURRENT_BASELINE.md` (`3e2ee909...`) | through 2026-10-04 | current chain and bounded current performance statements |
| S02 | `REPORTS/TANGRA_GEOMETRY_FPS_REMEDIATION_20260913.md` (`ba962c9...`) | 2026-09-13 | no-target/tracking FPS, sample counts and remediation scope |
| S03 | `TESTS/TANGRA_STATIC_TARGET_RUNTIME_TRACKING_20261005.md` (`07c2138...`) | 2026-10-05 | 3 h 36 m uptime, five recent FPS samples and same-ID limitation |
| S04 | `REPORTS/FPS_RUNTIME_INVESTIGATION_20260727.md` (`b527459...`) | 2026-07-27 | displayed-vs-end-to-end FPS semantic mismatch and old-stage gaps |
| S05 | `REPORTS/FPS_LIVE_VS_REPLAY_TWO_MINUTE_DIAGNOSTIC_20260727.md` (`c61fe57...`) | 2026-07-27 | historical per-stage/frame-period distribution and stalls |
| S06 | `REPORTS/TANGRA_CALIBRATION_AND_HOROS_VALIDATION_2026-09-05.md` (`1988348...`) | 2026-09-05 | static paired sensor timestamp deltas |
| S07 | `REPORTS/TANGRA_RUNTIME_HOROS_CHECKPOINT_2026-09-04.md` (`3cf6245...`) | 2026-09-04 | secondary-HEF cost and bounded primary-only runtime FPS |
| S08 | `REPORTS/HB-00_CURRENT_TELEMETRY_SURFACE_INVENTORY_20260910.md` (`f14b3e5...`) and `REPORTS/TANGRA_TELEMETRY_SIGNAL_REFERENCE_20260912.md` (`3a3c555...`) | 2026-09-10/12 | telemetry fields, freshness and queue/source gaps |
| S09 | `REPORTS/OBJECT_RESOLVER_FUSION_TARGET_UPDATE_DETERMINISTIC_REGRESSION_20260726.md` (`afe9668...`) | 2026-07-26 | deterministic out-of-order handling and replay cadence |
| S10 | TANGRA-CL `integration/COGNITIVE_ENDURANCE_VALIDATION_20260927.md` (`2714d79...`) and `integration/COGNITIVE_MISSION_COEXISTENCE_20260927.md` (`d0bb3e7...`) | 2026-09-27 | asynchronous Cognitive latency/endurance and coexistence |
| S11 | TANGRA-CL `architecture/COGNITIVE_PERFORMANCE_AND_STAGING_VALIDATION_PLAN_20260922.md` (`21de031...`) and `integration/CURRENT_INTEGRATION_STATE.md` (`0af63a6...`) | 2026-09-22/2026-10-03 | critical-path boundary and superseded/current chronology |
| S12 | WORKSHOP JOB-01 and JOB-02 Worker evidence, reviews and checkpoints | 2026-10-05 | independently reviewed chain/geometry/time gaps |

Fresh production source, Pi/runtime, live cameras and clock state: **NOT VERIFIED**. Repository evidence is authoritative for this qualification; no live access was attempted.

## 3. Perception-to-output stage, timestamp and clock map

| Stage/edge | Evidenced timing/freshness surface | Timestamp semantics / clock | Queue/identity | Qualification |
|---|---|---|---|---|
| HQ/WIDE capture | `capture_ms` can expose host-side stage duration; paired sensor timestamps exist in one static calibration set | Sensor timestamp fields exist in S06; epoch, timebase, reset and relation to host monotonic clock are not fully documented | HQ source frame ID and full dual-stream pairing lineage incomplete | Duration is not source age; current sensor-to-host latency `NOT VERIFIED` |
| preprocess + primary Hailo | `yolo_ms`; current reports include Hailo means/ranges | Host duration clock implied; exact timer API/clock provenance `NOT VERIFIED` | per-frame request ID/error/last-success incomplete | Stage-duration evidence only; not end-to-end freshness |
| NanoTracker / NumPy tracker | `tracker_ms`, active tracker state; current 180 s tracking cadence | measurement timestamp consumed by tracker and prediction epoch are not fully exposed | same-ID span exists but is not continuous truth | State epoch/age and dropout propagation `NOT VERIFIED` |
| range / projection | included in current path; JOB-02 establishes missing measurement-age/pose time | range evaluation time and input observation time are not both evidenced | bbox/class/frame/config lineage incomplete | physical state freshness unbounded |
| HOROS shadow | shadow timestamp allows observation-age derivation as `server_time - timestamp` | clock comparability and freshness threshold absent | authoritative state remains upstream; shadow is fail-open/non-authoritative | Age is derivable only if clocks/semantics match; threshold `NOT VERIFIED` |
| Object Resolver / Fusion / Target Update | deterministic replay retains caller timestamps | fixed test timestamps, not current runtime clock qualification | out-of-order timestamp is accepted deterministically; no ordering gate evidenced | Determinism supported; temporal correctness under reordering not established |
| WIDE latest-only path | `last_age_s`, `last_fresh`, `max_age_s=0.5`, stale/input/output drops | age semantics are WIDE-specific; exact source clock relation incomplete | `LATEST_ONLY_NO_BACKLOG`; actual queue occupancy absent | useful WIDE stale policy evidence, not system-wide freshness proof |
| telemetry/dashboard | `dashboard_ms`, serialization surfaces, runtime FPS/loop metrics | last-valid observation age and dashboard receive/render clock absent | end-to-end frame lineage and delivery queue residence absent | display age and sensor-to-display latency `NOT VERIFIED` |
| Cognitive observer | ~9.4 s asynchronous model latency, stable in bounded 2 h endurance | service timing evidenced in its own domain | deliberately off mission critical path; heavy work deferred to standby | Must not be added to perception-loop latency; separate service SLO |

No source proves that every stage shares one monotonic clock. Cross-host timestamp subtraction is therefore invalid unless clock identity/synchronization or measured offset uncertainty is supplied.

## 4. Evidence-quality and metric-fit audit

| Observation | Actual property measured | Does not establish | Verdict |
|---|---|---|---|
| no-target 41.28 FPS average; tracking 36.016 average, 28.368 min, 39.059 max over 180 s | bounded loop throughput/sample cadence in current dated configuration | source measurement age, stage latency distribution, synchronized output age | **SUPPORTED for bounded throughput only** |
| 11 samples below 32 and 4 below 30 in the tracking run | tail-count evidence against selected thresholds | full percentile distribution or root cause | **SUPPORTED, bounded** |
| five recent FPS samples mean 41.10, min 36.96, max 43.58 during 3 h 36 m session | five endpoint-adjacent samples | full-session cadence distribution | **INSUFFICIENT for session-wide performance** |
| zero systemd restarts over 3 h 36 m | process/service continuity | frame continuity, state freshness or same-target continuity | **UPTIME only** |
| same ID observed across 6314 s | first/last occurrence span | continuously tracked target or absence of reacquisition | **NOT continuous-tracking proof** |
| historical live 15.973 and replay 14.927 true FPS | 2026-07-27 old configuration end-to-end throughput | current runtime throughput | **VALID historical diagnostic; superseded configuration** |
| historical frame-period p95 79.528/84.119 ms and rare ~478 ms stall | old-configuration cadence/stall distribution | current tail latency | **VALID historical diagnostic; not current** |
| displayed FPS computed before 30 ms sleep | processing-only reciprocal metric | true throughput | **SEMANTICALLY INVALID as end-to-end FPS** |
| paired sensor deltas 4.807/44.751/50.691 ms | time separation for static calibration pairs | moving-target alignment or end-to-end age | **SUPPORTED static-pair timing only** |
| WIDE 0.5 s stale threshold/counters | component-local freshness decision/counter semantics | HQ/system freshness or physical accuracy | **SUPPORTED for WIDE policy only** |
| 240-frame deterministic replay at 27.301 FPS, queue high-water 1/32, no drops | one test workload/queue observation | production load or safe out-of-order semantics | **SUPPORTED for fixture only** |
| Cognitive ~9.4 s mean/median and no growth over bounded 2 h | asynchronous persistent-service latency/stability | mission-loop latency or indefinite endurance | **SUPPORTED in separate domain** |

FPS and uptime are therefore explicitly rejected as proxies for latency, age or synchronization.

## 5. Deterministic sensitivity

Artifacts:

- `temporal_sensitivity.py` SHA-256 `1cd84d1e6427212052930906c6259f7ee2f0a733c8aa3cf6610cbbec506dbdc3`;
- `temporal_sensitivity.json` SHA-256 `f9218a983625ab27ccf6de3a71a6c613162a797dcb8c9b666f2603923e3fbe14`.

Command: `python3 evidence/TANGRA-RESEARCH-LAB-03/temporal_sensitivity.py`.

The only equation used is `unobserved distance = speed × elapsed time`. It is dimensional sensitivity, not a TANGRA physical-error estimate. Velocity grids (1, 5, 10, 25 m/s), age, jitter and missed-frame counts are explicitly **synthetic**; they are not asserted target distributions.

### 5.1 Cadence conversions from evidenced FPS

| FPS observation | Reciprocal period |
|---|---:|
| no-target average 41.28 | 24.224806 ms |
| tracking average 36.016 | 27.765438 ms |
| tracking minimum sample 28.368 | 35.250987 ms |
| tracking maximum sample 39.059 | 25.602294 ms |
| five-sample static mean 41.10 | 24.330900 ms |

These reciprocals are nominal sample intervals implied by aggregate FPS values, not measured frame-age distributions.

### 5.2 Evidenced time coefficients

The static pair deltas imply 4.807, 44.751 and 50.691 mm of relative displacement per 1 m/s. At the WIDE-local 500 ms threshold, the coefficient is 0.5 m per 1 m/s. Neither calculation says that the target had that velocity or that displacement became estimation error.

### 5.3 Synthetic age, jitter and dropout examples

| Scenario | 1 m/s | 10 m/s | 25 m/s |
|---|---:|---:|---:|
| 50 ms age | 0.05 m | 0.50 m | 1.25 m |
| 100 ms age | 0.10 m | 1.00 m | 2.50 m |
| 500 ms age | 0.50 m | 5.00 m | 12.50 m |
| 25 ms incremental jitter | 0.025 m | 0.25 m | 0.625 m |
| 3 missed frames at 36.016 FPS average (83.296 ms) | 0.0833 m | 0.8330 m | 2.0824 m |
| 10 missed frames at 36.016 FPS average (277.654 ms) | 0.2777 m | 2.7765 m | 6.9414 m |

The dropout table converts missed nominal intervals into unobserved-motion distance only. It assumes no tracker extrapolation law, reacquisition, acceleration model, latency compensation or physical truth. Actual state error can be smaller, equal, larger or differently directed.

## 6. Missing-observability register

| Gap | Prevented conclusion | Minimum field/observation |
|---|---|---|
| source capture timestamp semantics | measurement age | `source_timestamp_ns`, `source_clock_id`, reset/wrap semantics |
| host receive and stage boundaries | transport + stage residence | monotonic begin/end timestamps for capture, preprocess, inference, tracking, range and publish |
| cross-host clock relation | sensor-to-dashboard/HOROS subtraction | synchronized UTC/PTP evidence or measured offset/error bound plus host monotonic clocks |
| immutable frame lineage | stale/mismatched component attribution | session ID, source frame ID, observation ID and parent IDs at every output |
| queue entry/exit/depth | queue age, backlog and drop consequence | entry/exit monotonic time, depth before/after, capacity and drop reason |
| tracker measurement/prediction epochs | state-age interpretation | last accepted measurement time, state epoch, output/prediction horizon |
| ordering gate semantics | effect of late/out-of-order inputs | accepted/rejected decision and reason keyed to observation timestamp |
| freshness policy generation | reproducible stale decision | threshold, config generation, clock and actual computed age |
| output delivery/render time | sensor-to-user age | serialize/send/receive/render timestamps with clock provenance |
| independent motion truth | physical temporal error | synchronized truth trajectory with declared uncertainty |

## 7. Smallest closure experiment

Add one bounded, non-authoritative per-frame trace at existing stage boundaries without changing scheduling or decisions. Each record should carry:

`session_id`, `source_frame_id`, `observation_id`, parent IDs, config generation, source timestamp and clock ID, host monotonic capture-receive/preprocess/inference/tracker/range/publish timestamps, tracker measurement epoch and prediction horizon, queue entry/exit/depth/capacity/drop reason, freshness threshold/age/decision, HOROS/Fusion ingest-output IDs/times, and telemetry/dashboard receive-render times.

Run three preregistered read-only captures:

1. stationary controlled target, to detect clock/lineage inconsistencies without motion confounding;
2. controlled known-motion target with synchronized independent truth, to bin residual by actual measurement age and dropout;
3. matched live/replay input from the identical recorded observation stream, to verify replay scheduling and ordering without camera variability.

Report distributions, not only averages: count, median, p95, p99, maximum, dropout/reorder count and explicit coverage. A run fails temporal integrity if any stage lacks lineage/clock provenance, produces negative/impossible residence, silently reorders beyond declared policy, or violates the preregistered age/drop criterion. Physical accuracy requires the independent truth run; the trace alone is observability evidence.

## 8. JOB-04 fair replay prerequisites

JOB-04 must not compare CV and CA until both consume the exact same immutable observation sequence with:

1. identical source frame/observation IDs, source timestamps, coordinate frame and calibration/config generation;
2. one declared timebase or evidenced clock conversion and uncertainty;
3. identical warm-up and initial state;
4. identical accepted/dropout/out-of-order input set, or explicit paired reporting of policy-caused coverage differences;
5. prediction horizon defined relative to the source observation epoch, not wall-clock completion;
6. outputs sampled at the same evaluation epochs and matched to synchronized independent truth;
7. availability/coverage reported separately from conditional error;
8. residuals stratified by age, horizon, dropout and reorder condition;
9. NIS/NEES used only if covariance definitions, noise assumptions and sufficient independent truth exist;
10. deterministic replay hash, ordering ledger and no hidden real-time sleep that changes logical timestamps.

Without these prerequisites, a lower residual may only reflect newer input, different coverage, a different horizon or a different dropout policy.

## 9. Headroom and optimization decision

The bounded current results support continued operation of the documented baseline for research purposes: 36.016 FPS average tracking over 180 s, zero lost samples in the cited 89/89 tracking series and no evidenced violation of the historical absolute 25 FPS floor. The more recent 3 h 36 m report establishes process continuity, not a full performance distribution. The coexistence reference was not a controlled tracking A/B (`active_trackers=0`), and the later 60 s observation is not a controlled comparison.

Historical diagnostics prove that metric semantics matter and that the former secondary-HEF/30 ms-sleep configuration had real ~15 FPS throughput and synchronous Hailo stalls. That configuration is superseded and cannot justify current optimization.

Decision: **OPTIMIZATION HOLD**. First establish current end-to-end semantic timing and a preregistered failure threshold. Absence of a current failure is not proof of airborne/full-load headroom.

## 10. Execution ledger and hygiene

| UTC date | Action | Result |
|---|---|---|
| 2026-10-06 | Read mandatory policies, schemas, canonical backlog, registry/project/state and JOB-01/02/03 task/evidence/review/checkpoints | eligibility and read-only boundary confirmed |
| 2026-10-06 | Reconciled stale `WORKSHOP_STATE` against newer canonical JOB-03 and JOB-01/02 PASS/checkpoints | JOB-03 selected; no duplicate task created |
| 2026-10-06 | Rechecked qualified target branch refs through GitHub connector | refs unchanged; fresh runtime still not accessed |
| 2026-10-06 | Inspected exact timing, telemetry, performance, calibration, deterministic replay and Cognitive sources | measured/synthetic/current/historical domains separated |
| 2026-10-06 | Ran deterministic script repeatedly and inspected generated JSON | stable hash and record counts 24 age / 20 jitter / 40 dropout |
| 2026-10-06 | Inspected task-local repository artifacts | only Worker report, justified script/JSON and review request retained; no disposable artifacts |

No target repository, source, runtime, service, model, firmware, configuration or scheduling behavior changed. No Codex gate was invoked.

## 11. Worker acceptance self-check

| Criterion | Result |
|---|---|
| exact source/ref/date and synthetic labels | PASS |
| FPS not used as latency/freshness proof | PASS |
| timestamp/clock semantics explicit or `NOT VERIFIED` | PASS |
| reproducible measured/synthetic separation | PASS |
| no physical accuracy claim absent truth | PASS |
| exact JOB-04 prerequisites | PASS |
| optimization HOLD absent present failure | PASS |
| read-only TANGRA boundary | PASS |
| hygiene | PASS at Worker stage |

## 12. Reviewer request

Independently re-run the deterministic artifact; recompute sampled reciprocal-period, age, jitter and dropout values; inspect exact-ref provenance; challenge current-versus-historical configuration separation, FPS/latency semantics, cross-clock claims, Cognitive critical-path exclusion, JOB-04 fairness requirements, protected boundaries and repository hygiene.
