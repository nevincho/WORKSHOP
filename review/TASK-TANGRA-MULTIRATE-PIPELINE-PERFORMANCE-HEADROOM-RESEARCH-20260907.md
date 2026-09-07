# REVIEW — TANGRA MULTI-RATE PIPELINE / PERFORMANCE HEADROOM RESEARCH

TASK_ID: TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907
VERDICT: PASS
STATUS: COMPLETE

## Independent review conclusion

The research correctly treats the source note as an IDEA / FUTURE VALIDATION artifact rather than an implementation decision. The multi-rate detector+tracker pattern is externally established, including detector-frame skipping with tracker continuation, but TANGRA-specific safe cadence remains NOT VERIFIED and requires benchmark evidence.

### Evidence-backed conclusions

1. **Detector decimation is architecturally legitimate, not automatically safe.** NVIDIA DeepStream explicitly supports inference intervals with tracking continuing on uninferenced frames. This supports the general architecture pattern, not a specific TANGRA cadence.

2. **Fixed every-N cadence should be a characterization sweep, not the assumed final scheduler.** Published detect-or-track research finds fixed frame skipping suboptimal when tracking difficulty changes and supports quality-dependent scheduling. Adaptive cadence is therefore a justified later experiment, after safe fixed bounds are measured.

3. **Bounded latest-frame semantics are mandatory for real-time correctness.** GStreamer documentation directly warns that slow consumers can accumulate queues/memory and documents bounded/leaky dropping. The research correctly converts this into a TANGRA invariant: expensive branches must not create stale FIFO backlog.

4. **Asynchronous Hailo execution is technically plausible.** HailoRT exposes asynchronous inference APIs/examples. However, async execution does not itself solve stale-result ordering, provenance, or backpressure; the research correctly requires frame IDs/timestamps and stale-result handling.

5. **The module cadence matrix preserves protected authority.** NanoTracker remains frame-rate while tracking, CA prediction remains high-rate/time-aware, CurrentTarget semantics remain protected, and HOROS prediction is not conflated with lower-rate measurement updates.

6. **No numeric compound FPS gain is claimed without profiling.** This is correct. Amdahl-like reasoning is appropriate: halving detector invocation frequency only reduces the detector share of total frame time and may be offset by increased HQ acquisition/memory cost.

## Adversarial checks

### Potential overreach checked
- The proposed 4-10 Hz Dashboard range is explicitly marked as a test range, not a production recommendation: PASS.
- WIDE and HOROS cadence reductions are not presumed safe: PASS.
- Range estimation is not blindly decimated because the arithmetic may be cheap and freshness semantics are not yet fully traced: PASS.
- Telemetry/control timing is not changed by research inference: PASS.
- Adaptive scheduler confidence is not assumed truthful; correlation with actual error is required: PASS.

### Important caveat
A higher-resolution calibration-consistent HQ acquisition stream may itself consume additional ISP/memory/copy bandwidth. Therefore the geometry-correction architecture and detector-cadence optimisation must be benchmarked together after the camera-geometry probe. A performance gain inferred from current 640x640 acquisition cannot be transferred directly to a future 2028x1520 acquisition configuration.

## Recommended experiment gate

The research order is accepted:
1. camera-geometry correctness probe;
2. timestamp/queue/freshness instrumentation;
3. N=1 baseline;
4. N=2..6 fixed detector sweep;
5. isolated Dashboard/logging/WIDE tests;
6. integrated compound benchmark;
7. adaptive scheduler only after safe detector-gap bounds are known.

## Definition of Done / hygiene

- Research output A-K present: PASS.
- External evidence references included: PASS.
- No implementation/code/calibration/model/tracker changes: PASS.
- No correction constants: PASS.
- No Codex invocation: PASS.
- No runtime/Pi5 action: PASS.
- No duplicate intermediate reports beyond authoritative task + consolidated research + final review: PASS.

FINAL VERDICT: **PASS / COMPLETE FOR RESEARCH ONLY.**

Production architecture, detector cadence, adaptive trigger policy, and expected headroom remain **NOT VERIFIED** until the defined benchmark campaign is executed.
