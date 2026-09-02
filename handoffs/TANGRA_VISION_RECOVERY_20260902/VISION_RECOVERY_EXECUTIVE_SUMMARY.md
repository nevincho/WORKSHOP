# VISION RECOVERY EXECUTIVE SUMMARY

TASK_ID: `TASK-059`  
Campaign: TANGRA Vision / Dual-Camera / Performance Recovery  
Date: 2026-09-02  
Status: PRE-CODEX FORENSIC PREPARATION

## 1. Executive conclusion

The available documentation does **not** support a single current Vision root cause. It supports several bounded conclusions that must remain separate until the authoritative development copy is inspected and measured.

### VERIFIED / DOCUMENTED HISTORICAL EVIDENCE

1. DroneGuard 1.0 was promoted as the protected stable comparison baseline on 2026-07-10. Its historical stack included camera acquisition, Hailo/YOLO, detection filters, NanoTracker, CA Kalman, Object Resolver, Fusion, metric projection, telemetry and Dashboard. The baseline benchmark reported 360 frames, 356 detections, zero track drops and `40.706863 FPS`, but that report did not define the FPS metric type.
2. CA Kalman has strong detector-linked replay evidence and remains the canonical protected primary predictor. The direct July comparison reported approximately `5.649 px` overall mean error for official CA versus `486.894 px` for the OpenCV/CV comparison. These are proxy/replay metrics, not absolute positional ground truth.
3. A real July-16 performance regression was traced to Object Resolver telemetry churn: new object IDs were created continuously, object count reached 29,138 and reported FPS fell to approximately 14.59–17.52. Reusing stable objects and capping retained state stopped accumulation and restored reported FPS to approximately 30.06–40.96. This proves one historical regression mechanism, not the current WIDE issue.
4. July-15 performance work reproduced another degradation episode: reported FPS 24.77→19.95, CPU 58.6%→69.9%, RSS 392→434 MB. A combined A/B that disabled `world_map_3d` publication and global Tactical JPEG polling improved CPU behavior and produced 31.40→28.63 FPS, but RSS growth and a smaller decline remained. Those paths were therefore not sufficient sole causes.
5. July-27 instrumentation proved that the Dashboard/runtime `fps` field then in use was a processing-only instantaneous value computed before a configured 30 ms sleep. It was not true end-to-end throughput. A controlled two-minute test measured true end-to-end live throughput at 15.973 FPS and replay at 14.927 FPS, while reconstructed processing-only rates were about 40.51 FPS on primary-only frames, 20.61 FPS on primary+secondary frames and 30.65 FPS amortized.
6. Synchronous Secondary HEF execution at exact 1:3 cadence added about 24 ms on every third frame in the July-27 investigation. Controlled replay deep stalls were attributable to Hailo inference latency affecting both primary and secondary HEFs.
7. The HQ metric/world chain was **not physically calibrated**. Documentation explicitly records mismatched nominal/runtime camera models, missing physical intrinsics/distortion/principal point, missing camera-to-carrier extrinsics/attitude and incomplete time ownership. Therefore validated HQ detection/tracking behavior must not be conflated with validated metric 3D/world positioning.
8. August-14 replay/software validation processed 3,098 frames with 2,918 raw and 2,799 accepted detections; `REJECT_SIZE=119`; CURRENT_TARGET continuity passed, but live controlled-target validation was deferred. Production promotion added an FPV two-axis pre-track size gate and CURRENT_TARGET layer; historical replay FPS was about 31.7–32.1, metric type not explicitly defined.
9. Dataset-specific evidence supports a general small-target risk: LRDD evidence reported no useful matches for small/medium target strata at the 640 detector input, while large samples performed materially better. A separate locked synthetic-FPV test found strong preprocessing/model-domain/target-scale sensitivity. Neither proves the current WIDE failure.

### CURRENT SUPPLIED EVIDENCE — NOT REPOSITORY-VERIFIED CURRENT IMPLEMENTATION

- Current hardware: WIDE IMX708, HQ IMX477 + 50 mm, 35.6 mm physical baseline, both operational; physical calibration incomplete.
- Bounded current diagnostic: standard path `4 raw → 3 accepted → 3 tracks → CA updates → TRACKING`; WIDE/HOROS shadow path received identical raw Hailo outputs but `0 accepted` because its physical-size/class-area gate rejected all four. This localizes one current divergence **after raw Hailo output and before accepted detection**.
- Separate WIDE test: an approximately 110×55 px full-resolution drone representation became approximately 15×14 px after current preprocessing and produced zero raw detector result. This is a separate possible small-target/preprocessing/detector-scale problem.

These two observations must not be merged into one root cause.

## 2. Protected baseline

The protected asset is specifically the **HQ IMX477 + 50 mm detection/tracking behavior** and its ability to operate independently as an HQ-only fallback. Future dual-camera work must not make HQ-only operation depend on WIDE initialization, WIDE calibration, WIDE filtering, cross-camera association, stereo geometry or a dual-camera scheduler.

Protection does **not** mean every historical metric-chain assumption is validated. Physical projection/range/world calibration remains incomplete.

CA Kalman mathematics is also protected. Investigation may test whether fresh observations, retained NanoTracker measurements and update eligibility are correctly distinguished, but must not retune/rewrite Kalman mathematics without new direct evidence.

## 3. Performance interpretation

Owner requirement: **normal tracking runtime below 25 FPS is a PERFORMANCE FAIL**.

The acceptance methodology has one mandatory prerequisite: every FPS observation must identify its metric. Historical `29–35`, `30–41` and `40.706863` values are not automatically comparable with the later measured `~15–16` true end-to-end values.

For Codex, record both:

- `PROCESSING_LOOP_FPS_PRE_SLEEP` (or the verified equivalent in current code), and
- `END_TO_END_PROCESSED_FPS` measured from completed-frame timestamps.

The owner’s >=25 gate remains binding to the campaign’s normal-tracking FPS metric after authoritative metric semantics are reconciled. No promotion decision may use an unlabeled FPS value. The matched HQ-only baseline under the same current instrumentation is the required comparison control.

Historical preferred processing region with meaningful evidence is approximately the high-20s through mid-30s under several post-restart/runtime tests; the official replay baseline reached ~40.7, but metric equivalence is not documented. This is a historical operating region, not a newly defined acceptance criterion.

## 4. Current first-divergence map

There are at least two independent current diagnostic questions:

- `DIVERGENCE-B`: identical raw Hailo output reaches the standard path but is rejected by a WIDE-specific/physical-size/class-area acceptance gate. First observed divergence: **raw detection → acceptance filtering**.
- `DIVERGENCE-A`: a WIDE source target loses substantial pixel scale through preprocessing and produces no raw detector output. First divergence is somewhere between **source frame → Hailo input → raw inference**, exact boundary NOT VERIFIED.

The campaign does not assert that either is the only defect.

## 5. Dual-camera architectural stance

Three modes remain valid candidates until measurement:

- **Mode A — Full Dual Vision:** both cameras detect/track. Highest functional scope and compute risk. Promote only if benefit is demonstrated and performance gate passes.
- **Mode B — Asymmetric Dual:** WIDE performs watch/acquisition/event/ROI/geometric observation; HQ remains authoritative detection/tracking/CA source. This is a first-class architecture, not a degraded fallback.
- **Mode C — HQ Fallback:** independent protected HQ-only operation; mandatory regardless of A/B outcome.

No evidence currently justifies pre-selecting A or abandoning WIDE.

## 6. First Codex actions

Codex must not begin with a fix. Required sequence:

1. Create/verify an immutable snapshot of the proven HQ-centric development line and rollback reference.
2. Reconcile actual current files, services/configuration, camera identities and runtime control against this package. Historical file paths are navigation clues only.
3. Verify the complete current Vision trace and camera identity propagation.
4. Instrument stage timing with monotonic timestamps and explicitly labeled FPS metrics.
5. Establish matched HQ-only baseline with Dashboard client state, Secondary HEF state, pacing/sleep, camera mode and resource counters recorded.
6. Reproduce current WIDE tests and capture per-boundary counts/sizes: source target pixels, preprocessed target pixels, Hailo input, raw outputs, each rejection reason, accepted detections, tracker input.
7. Locate the first reproducible divergence.
8. Make exactly one bounded change; A/B against unchanged control; run HQ regression and performance gate; keep or revert.
9. Only after upstream Vision is stable, evaluate Mode A versus Mode B. Mode C must remain intact.

## 7. Current unknowns that matter

- Authoritative development-copy file layout and exact current implementation: `NOT VERIFIED`.
- Exact current camera capture modes, stream formats, exposure/gain/focus controls: `NOT VERIFIED`.
- Exact WIDE preprocessing chain and filter constants in the authoritative development copy: `NOT VERIFIED`.
- Current FPS field semantics and pacing configuration: must be re-verified; historical semantics cannot be assumed current.
- Exact historical repository evidence for the reported stale-NanoTracker-to-Kalman shadow freshness defect was not located in the bounded TANGRA-DOCS searches performed for this package. The integration risk is retained as `NOT VERIFIED / CHECK REQUIRED`, not as a proven defect.
- Physical HQ/WIDE intrinsics/extrinsics and HQ long-range focus: calibration gates remain open.

## 8. Promotion principle

`FUNCTIONAL PASS + PERFORMANCE FAIL = ARCHITECTURE FAIL` for dual-camera promotion.

No WIDE improvement may conceal an HQ regression. Every retained change must preserve HQ-only behavior, tracking continuity, CA semantics, Object Resolver, CURRENT_TARGET, Fusion inputs, telemetry/API, Dashboard compatibility, lifecycle/OFF-STANDBY behavior and rollback capability.
