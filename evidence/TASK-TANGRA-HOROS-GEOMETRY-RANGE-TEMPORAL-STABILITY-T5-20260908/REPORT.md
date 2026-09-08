# TASK 5 — Temporal Stability Report
Evidence: SYNTHETIC / HOST ONLY
Seed: 20260908

## Decision
EVERY_FRAME_RECOMPUTE_ACCEPTABLE: YES
TEMPORAL_PROPAGATION_REQUIRED: NO
DECISION: TEMPORAL_PROPAGATION_NOT_REQUIRED_FOR_CURRENT_CANDIDATE

## Key metrics
- A_STATIC_NOISE: center RMS 0.676 px; LEFT 0.803 px; RIGHT 0.809 px; LR span CV 0.288%; sparse range CV 0.170%; fused range CV 0.159%; range bias +0.0029 m; error jitter 0.0317 m; max transient 0.0823 m; invalid 0; NOSE/TAIL valid 100%.
- B_TRANSLATION: center RMS 0.747 px; LR span CV 0.300%; fused range CV 0.177%; bias -0.0049 m; error jitter 0.0354 m; max transient 0.0811 m.
- C_SCALE_CHANGE: raw fused-range CV 17.055% because ground-truth range intentionally changes; error jitter is 0.0400 m; bias -0.0007 m; max error 0.1140 m; monotonic-trend test PASS.
- D_ROTATION: fused range CV 0.157%; bias +0.0011 m; max transient 0.0835 m.
- E_FORESHORTEN: fused range CV 0.331%; bias +0.1766 m; error jitter 0.0667 m; max transient 0.2939 m. This is model/viewpoint bias, not temporal divergence.
- F_CORRUPT: corrupted RIGHT point produces 15.081 px point RMS excursion but fused-range CV remains 0.154%; max fused error 0.0646 m; no temporal carry-over.
- G_WEAK_CONTRAST: 5 INVALID frames; range returns on first clean frame (frame 35); no carry-over.
- H_AXIAL_AMBIGUITY: NOSE/TAIL valid rate 93.75%; degraded class-size evidence continues without fabricating axial geometry.
- I_PARTIAL_SILHOUETTE: degraded sparse evidence is bounded; fused error jitter 0.0356 m.
- J_RECOVERY: 5 INVALID frames; first clean-frame recovery; post-gap state is independent of prior invalid frames.

## Tests
15/15 PASS.

## Benchmark
TASK5 stateless measurement-domain harness only, n=100000:
- mean 0.018120 ms
- median 0.015984 ms
- p95 0.021212 ms
- max 14.437042 ms

This is NOT a measured production T1→T4 image-stage benchmark and must not be converted into Pi5 FPS.

## Production gates
UNCHANGED / NOT_VERIFIED:
- production AI→CAL transform;
- physical TASK 1 point↔real-span correspondence;
- physical metric accuracy;
- Pi5 end-to-end impact.

## Temporal architecture
No smoothing, propagation, optical flow, template tracking, second tracker, second Kalman filter, or motion prediction was added.
