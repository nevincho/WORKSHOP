# SOURCE EVIDENCE MANIFEST

TASK_ID: `TASK-059`

## Authority model

- **Implementation/current-runtime authority:** authoritative DroneGuard development copy when Codex receives access. `NOT AVAILABLE TO WORKSHOP` in this campaign.
- **Historical architecture/validation authority:** `nevincho/TANGRA-DOCS`, default branch `main`.
- **Coordination/handoff authority:** `nevincho/WORKSHOP`.
- **Current supplied evidence:** owner-provided observations in the dedicated Control Room request. These are retained as supplied evidence and are not promoted to repository-verified current implementation facts.
- `TANGRA-2.0` and HOROS implementation artifacts were not used as current DroneGuard runtime authority.

## Evidence quality classes

- `HIGH`: report documents controlled measurement, method/state and bounded result sufficiently to support the cited claim.
- `MEDIUM`: documented result is useful but a key metric definition/configuration or immutable source identity is missing.
- `LOW`: operator report, static candidate ranking or incomplete comparability; useful for hypotheses only.
- `CURRENT_SUPPLIED`: direct owner-supplied current observation, awaiting Codex reconciliation.
- `NOT VERIFIED`: evidence unavailable or not found in bounded search.

## TANGRA-DOCS sources

| Source | Evidence quality | Material facts used | Limits / prohibited inference |
|---|---|---|---|
| `REPORTS/DRONEGUARD_1_0_OFFICIAL_BASELINE_PROMOTION_20260710.md` | MEDIUM/HIGH | DroneGuard 1.0 promoted protected stable baseline; validated stack; 360 frames/356 detections/0 drops; FPS40.706863; CPU/RAM/temp | FPS metric type not stated; historical runtime path is not current development-copy proof |
| `ARCHITECTURE/DRONEGUARD_1_0_OFFICIAL_STABLE_BASELINE.md` | MEDIUM/HIGH | protected stable comparison line; baseline stack and performance references | architecture document historical, not authoritative current code |
| `CURRENT_BASELINE.md` | MEDIUM/HIGH, section-dependent | July11 thread-limit correction; baseline protection; LRDDv3/local-media/fixed-wing boundaries; LRDD small-target scale evidence; calibration status | appended sections use different methodologies; detector-linked residuals not absolute GT; LRDD not TANGRA camera calibration authority |
| `CAMERA_PROFILE_NOMINAL_MANUFACTURER_SPEC_2026-07-12.md` | MEDIUM | HQ IMX477+50mm nominal 10°×7°; historical 640×640 detector/tracker/CA space; runtime historically 7.2°×5.4° uncalibrated; CA state contract | nominal derived values are not physical calibration; current camera config not proven |
| `REPORTS/CAMERA_METRIC_CHAIN_AUDIT_20260713.md` | HIGH for audited historical wiring | incomplete metric chain; projection used current centre rather than future pixel; range current bbox; no explicit local XYZ/extrinsics/attitude; multiple timestamp owners; physical calibration none | does not invalidate HQ detection/tracking; current development-copy wiring may differ |
| `REPORTS/KALMAN_RUNTIME_COMPARISON_2026-07-08.md` | HIGH for stated replay harness | CA ~5.628/5.649 px vs CV ~505.49/486.894 px; five-video comparison; CA recommended | detector-linked replay proxy, no absolute positional GT; do not retune based on this package |
| `REPORTS/tangra_12h44m_runtime_evidence_20260704.md` | MEDIUM for endurance state, LOW for FPS comparability | 12h44m runtime, camera/AI/Hailo/tracking live, CPU24–28%, RAM~6.7%, temp~56C, FPS20.2; historical owner acceptance of longer runs | FPS counter semantics unknown; historical development dashboard not present-day architecture proof |
| `REPORTS/DASHBOARD_2_1_DEVELOPMENT_HISTORY_PRE_PERFORMANCE_20260715.md` | MEDIUM/HIGH | chronology of Dashboard recovery, Detection/Tracking/Kalman pages, camera calibration metadata, geographic telemetry changes | documents accepted development state, not causal performance proof |
| `REPORTS/DASHBOARD_RUNTIME_PERFORMANCE_AUDIT_20260715.md` | HIGH for measured degradation; LOW/MEDIUM root attribution | 15-min CPU58.6→69.9, FPS24.77→19.95, RSS392→434; no thermal evidence; world-map/deep-copy and JPEG candidates | exact root cause not proven; no immutable last-known-good source revision |
| `REPORTS/DASHBOARD_RUNTIME_PERFORMANCE_AB_TEST_20260715.md` | HIGH | world-map publication + Tactical JPEG polling disabled; CPU52.0→53.1, FPS31.40→28.63, RSS284.9→316.6; API payload grew without world_map | combined A/B does not isolate individual contribution; remaining decline persisted |
| `REPORTS/DASHBOARD_RUNTIME_FORENSIC_DIFF_20260715.md` | MEDIUM | historical static ranking: per-telemetry `synthetic_view` allocation + deep-copy amplification high-probability non-excluded candidate; historical source trees not Git-managed | static code-risk conclusion only; not benchmark proof; excluded paths were intentionally not ranked in that audit |
| `REPORTS/OBJECT_RESOLVER_MEMORY_CAP_FIX_20260716.md` | HIGH | proven historical resolver object-churn root cause; 29,138 objects; FPS14.59–17.52; post-fix counts1–2 and FPS30.06–40.96 | does not establish current recurrence; metric type not explicitly labeled |
| `REPORTS/FPV_PREPROCESS_NMS_CPU_HAILO_AB_20260722/FPV_PREPROCESS_NMS_CPU_HAILO_AB_REPORT.md` | HIGH for locked synthetic fixture | target-scale/preprocess/model-domain sensitivity; raw near-full-frame boxes originated before parser; crops restored class activation but not localization | synthetic render/domain; not current WIDE proof; no production fix applied |
| `REPORTS/PVF_HEF_SHUTDOWN_FIX_AND_1H_LIVE_20260722/PVF_HEF_SHUTDOWN_FIX_AND_1H_LIVE_REPORT.md` | HIGH for shadow stability/resource evidence | 1h live dual cameras + both HEFs, primary processing24.542ms, secondary contribution8.365ms, CPU mean54.309%, RSS +2.399%, clean shutdown | production service inactive; detection quality not scored; no directly reported FPS; no single-camera control |
| `REPORTS/PVF_HEF_OFFICIAL_1_0_LIVE_UNTIL_1400_20260722/PVF_HEF_OFFICIAL_1_0_LIVE_UNTIL_1400_REPORT.md` | HIGH | 86.79min live dual cameras+both HEFs; CPU/RSS bounded; raw harness memory delta false-fail correctly classified as methodology error | no direct FPS; no detection-quality scoring; not a full authoritative dual-tracking benchmark |
| `REPORTS/PVF_HEF_OFFICIAL_OPERATIONAL_ACTIVATION_20260726.md` | HIGH | official PVF passive + Secondary informational 1:3 activation; 300s smoke; stable FPS/CPU/RSS; no errors; primary remained authority | exact FPS metric type not explicitly named in report |
| `REPORTS/OBJECT_RESOLVER_FUSION_TARGET_UPDATE_DETERMINISTIC_REGRESSION_20260726.md` | HIGH | Resolver/Fusion/Target Update deterministic PASS; ON/ON vs OFF/OFF authoritative outputs identical; integration replay 240 frames at27.301 | runner FPS semantics not stated; short replay not endurance |
| `REPORTS/FPS_RUNTIME_INVESTIGATION_20260727.md` | HIGH | explicit proof Dashboard fps was per-loop/pre-sleep instantaneous; true throughput15.879; Secondary1:3 adds24.029ms; rare stalls initially unattributed | first investigation lacked stage timing for rare stalls |
| `REPORTS/FPS_LIVE_VS_REPLAY_TWO_MINUTE_DIAGNOSTIC_20260727.md` | HIGH | controlled true E2E live15.973/replay14.927; processing-only reconstructed40.51/20.61/30.65; sleep30ms ~47.95%; Hailo inference caused deep replay stalls | live minor hooks partly failed to attach, but primary/secondary/camera/sleep/resource accounting remained valid per report; exact current config must be rechecked |
| `REPORTS/DG_TEST_FINAL_ACCEPTANCE_2026-08-14.md` | HIGH for replay/software acceptance | 3098 frames, raw2918, accepted2799, REJECT_SIZE119, CURRENT_TARGET continuity PASS, avg FPS32.129, clean lifecycle | controlled live target absent; live validation deferred; FPS semantics not explicit |
| `REPORTS/DRONEGUARD_1_0_CURRENT_TARGET_PRODUCTION_PROMOTION_2026-08-14.md` | HIGH for historical promotion | verified rollback; FPV two-axis pre-track size gate and CURRENT_TARGET promoted; replay accepted2799, FPS31.725, no detector/CA regression | live controlled target deferred; does not establish current WIDE behavior |

## WORKSHOP governance sources

| Source | Use |
|---|---|
| `AGENTS.md`, `README.md` | repository-first bootstrap, evidence/persistence and reviewer requirements |
| `policies/AUTONOMY_POLICY.md` | target repo authority, smallest justified change, no unsupported completion |
| `policies/VALIDATION_POLICY.md` | acceptance methodology, prerequisites, failure classification |
| `policies/EXECUTION_ROUTING_POLICY.md` | TANGRA audit/report default; no autonomous implementation |
| `policies/CODEX_BUDGET_POLICY.md` | complete Workshop preparation before a consolidated human-gated Codex run |
| `policies/REPOSITORY_COMMUNICATION_POLICY.md` | substantive output persisted in WORKSHOP |
| `projects/TANGRA.md`, `status/WORKSHOP_STATE.yaml` | global TANGRA runtime OFFLINE_HOLD; preserved during this documentation-only campaign |
| `schemas/TASK_SCHEMA.md`, `schemas/HANDOFF_SCHEMA.md` | TASK-059 and final handoff structure |

## Current supplied evidence retained separately

### CS-01 — Hardware

- WIDE: IMX708 Camera Module 3 Wide, autofocus capable, supplied current `camera0`, `/dev/media2`, full 4608×2592 verified.
- HQ: IMX477 HQ + 50 mm manual-focus lens, supplied current `camera1`, `/dev/media3`, full 4056×3040 verified.
- physical baseline 35.6 mm.
- both operational.
- physical calibration incomplete; HQ long-range/infinity focus remains a gate.

Classification: `CURRENT_SUPPLIED`.

### CS-02 — Raw-to-acceptance divergence

- standard: 4 raw → 3 accepted → 3 tracks → CA updates → TRACKING.
- WIDE/HOROS shadow: identical raw Hailo outputs → 0 accepted.
- supplied rejection reason: WIDE physical-size/class-area gate rejected all four.

Classification: `CURRENT_SUPPLIED`; first observed divergence before HOROS, at acceptance filtering.

### CS-03 — Small-target raw failure

- WIDE full resolution 4608×2592.
- target graphic approximately110×55 source px.
- after current preprocessing approximately15×14 px.
- raw detector result0.

Classification: `CURRENT_SUPPLIED`; first exact upstream boundary not yet verified.

### CS-04 — performance gate

Normal tracking runtime `<25 FPS = PERFORMANCE FAIL`.

Classification: `OWNER REQUIREMENT`. FPS metric must be labeled/reconciled before using the gate.

## Evidence not found / NOT VERIFIED

1. Exact TANGRA-DOCS artifact proving the reported historical stale-NanoTracker measurement reapplication to CA in a shadow integration was **not located** in bounded searches for `stale tracker`, `freshness` and related repository terms. The concern remains an owner-supplied integration risk and a mandatory Codex check, not a proven defect.
2. Exact current authoritative development-copy file tree/config/hashes are unavailable to Workshop by campaign design.
3. A matched historical single-camera versus full-resolution dual-camera benchmark with identical Vision/HEF/Dashboard configuration was not found in the bounded evidence set. Historical dual-camera shadow runs provide resource/stability data but do not isolate camera-only cost.
4. Current dual-camera normal-tracking FPS, CPU, RSS, temperature and throttle state are not supplied/verified.
5. Current physical calibration values for both cameras are not verified.

## Search boundary

The campaign intentionally avoided uncontrolled repository discovery. Evidence was limited to canonical baseline, camera/metric, performance, Hailo/shadow, tracking/Kalman, Resolver/Fusion/CURRENT_TARGET, endurance and detector-scale reports materially related to the requested Vision recovery scope.
