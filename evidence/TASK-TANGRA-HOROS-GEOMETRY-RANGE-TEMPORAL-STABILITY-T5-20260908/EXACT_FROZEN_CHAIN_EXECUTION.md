# TASK 5 exact frozen-chain execution report

TASK_ID: TASK-TANGRA-HOROS-GEOMETRY-RANGE-TEMPORAL-STABILITY-T5-UNBLOCK-20260908
EXECUTION_MODE: HOST / SYNTHETIC / EXACT_FROZEN_MODULES
EXACT_CHAIN: TASK1 -> TASK2 -> TASK3 -> TASK4
FRAMES: 600 total / 10 deterministic sequences / 60 frames each

Frozen identity:
- T1 c7b378841979f82b037c47be3571fa72a7b70e51 / sparse_target_geometry.py / blob 91f81e882af557f2d2106a8648ee283bfbdee81e / SHA256 7c5aa770d7928a8fcc2de665f58b0b25d38c8ba74d7eb7fb8994d086b1948cfb
- T2 4bd4b5d38357db501de07511aeabaa4c0ae058e1 / ai_calibrated_geometry_adapter.py / blob 83202583f93ca43b134132f84d5cd51d7b59bcbe / SHA256 9c1bec7f2347dd4eff9ae231c89d35ad6656e1b83500d7cf6d95f15b2b0188e5
- T3 c121ce25dbba84520c6f8e644281a7cb2bf3ee73 / sparse_geometry_range_source.py / blob d15e09dc63384d93719fdab30b50634750cfd65c / SHA256 697e59bee439c1e4c9bebeb393c6c0b1f987113e5a440e1600c2d6655433b2cf
- T4 7f628a727b89599ea6977053ea12211b10e0ffcd / horos_range_fusion_contract.py / blob af995bdaab486b0c677bcd35c6166d90d253bbfb / SHA256 01b3677584b449660421c57a744ce8bc81302408cf739fa6ec13db673c4b2471
- All four blob identities matched reviewed frozen artifacts before execution and after execution.

Synthetic fixture boundary:
- 640x640 AI/CAL identity transform; status SYNTHETIC, production_verified=false.
- fx=fy=5000 test calibration only; production_verified=false.
- physical LR/NT spans derived once from the rendered synthetic baseline at known 20 m solely to separate temporal jitter from rasterization bias.
- MONOCULAR_CLASS_SIZE input is independent SYNTHETIC evidence around known truth with deterministic 0.4% noise and remains NOT_VERIFIED.

Sequence metrics:
A_STATIC_NOISE: center 0.794695 px; left/right 0.802538/0.802538 px; LR CV 0.000000; NT CV 0.002711; candidate range CV 0.002270; sparse CV 0.001560; fused CV 0.001760; bias +0.020358 m; error jitter 0.035238 m; max error 0.099829 m; invalid 0; degraded 60; conflict 0.
B_TRANSLATION: center 0.853158 px; left/right 1.065642/1.065642 px; candidate CV 0.002318; sparse CV 0.001631; fused CV 0.001420; bias +0.022999 m; jitter 0.028429 m; max error 0.096728 m.
C_SCALE_CHANGE: raw fused CV 0.137298 reflects true range trend; bias -0.017022 m; error jitter 0.059125 m; max error 0.156976 m. Trend monotonicity test PASS.
D_ROTATION: center 0.800145 px; left/right 3.233825/3.321731 px; LR CV 0.049482; NT CV 0.010346; candidate CV 0.040686; sparse CV 0.026319; fused CV 0.007556; bias +0.002736 m; jitter 0.151150 m; max error 0.299441 m.
E_FORESHORTEN: candidate CV 0.036377; sparse CV 0.014494; fused CV 0.002931; bias +0.172677 m; jitter 0.059118 m; max error 0.337204 m. Bias is viewpoint/model accuracy, not temporal instability.
F_CORRUPT: right-point RMS jitter 8.422126 px versus static 0.802538 px; candidate CV 0.029325 and sparse CV 0.035228; fused CV remains 0.001604, demonstrating outlier containment rather than hidden averaging.
G_WEAK_CONTRAST: 5 INVALID frames; 55 DEGRADED; recovery 1 frame; nose/tail valid rate 0.9167; fused CV on usable frames 0.001565.
H_AXIAL_AMBIGUITY: nose/tail valid rate 0.9167; fused CV 0.001503; no temporal carry-over.
I_PARTIAL_SILHOUETTE: left RMS jitter 6.253135 px; LR CV 0.092148; candidate CV 0.093837; sparse CV 0.001508; fused CV 0.001695.
J_RECOVERY: 5 INVALID frames; recovery on first clean frame; fused CV 0.001576.

Confidence:
- Static geometry confidence mean 0.892272; range confidence mean 0.896136.
- Weak-contrast interval geometry/range confidence minima 0.0, with first-clean-frame recovery.

Performance over all 600 exact-chain frames:
- T1: mean 0.958856 ms; median 0.934582; p95 1.082235; max 12.794984.
- T2: mean 0.420573 ms; median 0.403445; p95 0.548782; max 1.593486.
- T3: mean 0.101018 ms; median 0.088379; p95 0.132153; max 3.858247.
- T4: mean 0.047802 ms; median 0.037096; p95 0.063868; max 3.225111.
- Complete chain including fixture render/adaptation overhead: mean 2.713561 ms; median 2.633503; p95 3.200142; max 31.039559; n=600.

Validation: 13/13 PASS.
Decision: EVERY_FRAME_RECOMPUTE_ACCEPTABLE=YES; TEMPORAL_PROPAGATION_REQUIRED=NO.
Production gates remain NOT_VERIFIED. No T1-T4 source modified. No production integration. No TASK 6 work.
