# TASK 5 — Temporal Stability Architecture / Evidence Note

## Boundary
TASK 5 adds no temporal estimator. The harness is deliberately stateless: each frame is evaluated independently. It creates no object identity, motion prediction, optical flow, landmark propagation, template state, Kalman state, or tracker state.

## Every-frame model
Synthetic frame fixture -> sparse-point measurement representation -> calibrated span geometry -> sparse range candidates -> class-size comparison evidence -> TASK-4-equivalent uncertainty/conflict fusion -> temporal metric aggregation.

The harness measures independent per-frame measurements and does not alter frozen TASK 1-4 contracts.

## Evidence limitation
This execution environment does not contain the authoritative local DroneGuard checkout and cannot execute the complete production image acquisition/detector/TASK-1 ROI path end-to-end. Sequence evidence is therefore SYNTHETIC/HOST. The harness uses frozen TASK 1 point semantics and T2/T3/T4 contract/math boundaries. Its benchmark is not a full production T1→T4 runtime benchmark. Prior stage timings are not summed into a claimed measured pipeline latency.

## Stability interpretation
Raw coefficient of variation is meaningful only for stationary quantities. For commanded scale/range trend, raw CV reflects the intended trend; stability is assessed using error relative to known synthetic truth and monotonic trend behavior.

## Acceptance gates fixed before decision
- static center RMS jitter <= 1.5 px;
- stable span CV <= 2%;
- stable fused-range CV <= 3%;
- recovery <= 1 frame after degraded interval;
- no cross-target state leakage.

## Decision rule
Propagation may be proposed only if every-frame measurement recomputation violates these gates in a way not bounded by existing invalid/degraded/conflict behavior.
