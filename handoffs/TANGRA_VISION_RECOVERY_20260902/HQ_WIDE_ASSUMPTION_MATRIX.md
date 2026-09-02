# HQ / WIDE ASSUMPTION MATRIX

TASK_ID: `TASK-059`

## Rule

A rule that worked for HQ is not automatically valid for WIDE. A WIDE rejection is not, by itself, evidence that WIDE hardware is defective. Camera-dependent assumptions must be made explicit and measured.

| Assumption / interface | HQ IMX477 + 50 mm | WIDE IMX708 | Evidence status | Failure mode if shared blindly | Codex check |
|---|---|---|---|---|---|
| Product role | Historically central protected detection/tracking path | Historically situational/wide view; deeper Vision role now under evaluation | HQ role documented; current WIDE role supplied | WIDE forced into HQ-centric thresholds or HQ made dependent on WIDE | Identify authoritative mode/config and dependency graph. |
| Physical camera identity | supplied current camera1 `/dev/media3` | supplied current camera0 `/dev/media2` | CURRENT SUPPLIED EVIDENCE | Linux index/order drift silently applies wrong profile | Bind persistent camera identity to model/profile; log sensor model + media path at startup. |
| Native/full resolution | supplied current 4056×3040 | supplied current 4608×2592 | CURRENT SUPPLIED EVIDENCE | incorrect source-to-detector scale calculations | Record actual configured capture resolution, crop and scaler output. |
| Lens/focus | 50 mm manual focus; long-range/infinity quality remains gate | wide lens with autofocus capability | current hardware supplied; HQ nominal docs | focus failure may mimic detector/model failure; autofocus may alter repeatability | Lock/record focus state during controlled A/B; independently verify HQ infinity sharpness. |
| FOV/intrinsics | nominal analysis 10°×7°; historical runtime config 7.2°×5.4° uncalibrated | physical/current intrinsics not calibrated | documented HQ; WIDE NOT VERIFIED | wrong bearing/range and any physical-size conversion | Keep detection recovery independent of metric calibration; later calibrate both. |
| Distortion/principal point | no physical calibration in audited chain | NOT VERIFIED | DOCUMENTED / NOT VERIFIED | wide lens distortion especially can bias off-axis geometry | Calibrate intrinsics/distortion before metric 3D claims. |
| Extrinsics | camera-to-carrier transform absent in historical audited metric chain | 35.6 mm supplied physical baseline but orientation/translation calibration incomplete | PARTIAL current supplied | stereo/world geometry wrong even if detections are correct | Measure rigid relative pose after mounting; baseline length alone is insufficient. |
| Source target pixel scale | telephoto optics intended to keep distant target larger in frame | wide FOV necessarily produces smaller target pixel footprint at same range | engineering geometry + supplied observation | thresholds/model input designed around HQ target scale reject/miss WIDE targets | Measure source bbox by camera/range/target before preprocessing. |
| Detector input space | historical docs: 640×640 runtime coordinate space | current transform `NOT VERIFIED`; supplied target ~15×14 after preprocessing | historical + current supplied | small-target information lost before inference | Log resize/crop transform and resulting target pixels; compare controlled ROI strategies only after trace. |
| Resize policy | exact current policy NOT VERIFIED | current policy NOT VERIFIED; synthetic evidence shows letterbox/stretch sensitivity on another fixture | PARTIAL historical | aspect ratio/interpolation changes class activation/localization | Compare current exact preprocessing first; no speculative replacement before reproduction. |
| Raw detector scale floor | project-specific large targets performed much better in LRDD; no reliable universal threshold | likely more exposed to small-target floor | dataset-specific historical only | assuming detector can localize a 10–20 px target because it detects larger HQ targets | Run matched target-scale sweep; keep dataset/domain distinction. |
| Confidence thresholds | historical configured global/class confidence existed | current WIDE confidence behavior not implicated by supplied gate evidence | HQ historical; WIDE unknown | lower confidence to rescue WIDE could inflate false positives and degrade HQ | Count raw outputs by confidence before changing threshold. Threshold change requires precision/false-positive regression. |
| Bbox/full-frame rules | historical rules recovered in Dashboard | current parity unknown | historical | coordinate-space mismatch causes valid WIDE bbox rejection | Log normalized and pixel bbox dimensions with coordinate space. |
| Two-axis/physical-size gate | Aug14 FPV two-axis pre-track size gate promoted; replay had 119 REJECT_SIZE | supplied current WIDE path rejects identical raw outputs at physical-size/class-area gate | historical + current supplied | HQ-tuned expected dimensions reject wide-view target | Trace exact formula/profile/camera input. Test camera-aware rule only as a bounded candidate after evidence. |
| Area gate | historically configured area/edge filters | supplied current WIDE class-area rejection | PARTIAL | wide target area shrinks quadratically with pixel scale | Record area in source and detector spaces; identify whether gate uses normalized or absolute area. |
| Camera identity through detections | not explicitly proven as part of historical detection schema | critical for camera-aware thresholds/geometry | NOT VERIFIED | a shared detection object loses camera provenance, making safe dual behavior impossible | Require `camera_id/source_frame_id` through accepted detection, tracker observation and telemetry. |
| Tracker initialization | historically accepts filtered detections | supplied WIDE has no accepted detections in bounded test | HQ validated; WIDE blocked upstream | tracker blamed for absence of tracks when it never received WIDE detections | Verify tracker input count before tracker debugging. |
| Tracker identity | NanoTracker low-level IDs historically allowed to change; CURRENT_TARGET absorbs mission continuity | WIDE authoritative identity not yet justified | historical | cross-camera IDs treated as same target without association evidence | Keep camera-local identity distinct until association proven. |
| Tracker freshness | exact historical/current retained-measurement semantics not located in bounded docs | same concern would be more acute with intermittent WIDE detections | NOT VERIFIED / CHECK REQUIRED | stale retained bbox re-used as a fresh Kalman measurement | Add observation source/age/fresh flag and assert Kalman update eligibility. |
| CA Kalman | validated canonical primary in historical HQ-centric replay | no evidence yet for authoritative WIDE CA track | protected | retuning CA to compensate for WIDE upstream errors damages HQ | Do not tune math. Verify coordinate/time input contract first. |
| Prediction timestep | historical profile document states dt=0.033 s; later baseline appendix questions real timing in another proxy context | current per-camera cadence could differ | historical / current NOT VERIFIED | fixed dt mismatches actual asynchronous camera/dual schedule | Codex verify current timestamp/dt ownership without changing filter until measured. |
| Projection | historical current-centre projection, uncalibrated camera model | WIDE projection profile NOT VERIFIED | historical | wrong FOV/profile causes bearing errors | Camera-specific calibrated profile required for metric use. |
| Monocular range | class-size + bbox/focal model, absolute accuracy unverified | same equation more sensitive to small bbox and wide calibration | historical nominal | noise/size assumptions become dominant at small bbox | Report uncertainty; do not use as proof of dual 3D accuracy. |
| Cross-camera association | not required for protected HQ-only mode | required if WIDE geometry/dual tracking influences same target | NOT VERIFIED | unrelated targets fused because views overlap only partially | Define time/epipolar/appearance/geometry association validation before authority. |
| Stereo depth | not part of validated HQ baseline | potential after both cameras calibrated | future candidate | assuming 35.6 mm baseline alone yields reliable long-range depth | Compute measurable disparity regime after calibration and actual target range; reject if disparity below useful noise floor. |
| Secondary HEF scheduling | later primary + shadow secondary synchronous 1:3 documented | shared Hailo device may contend with additional WIDE inference | historical | full-dual inference serializes and breaches performance gate | Instrument Hailo queue/start/end per model/camera; evaluate scheduling separately from capture cost. |
| Dashboard preview | historical HQ JPEG could encode in AI loop; Tactical poller 250 ms was a cost candidate | WIDE preview worker historically existed at 4 FPS | historical | dual preview load mistaken for Vision inference cost | Profile no-browser, preview-off, then controlled preview client. |
| Telemetry payload | historical deep copies amplify new nested payloads | dual-camera payload may multiply detections/images/metrics | historical risk | CPU/RSS regression from observability layer, not Vision algorithm | Measure payload bytes, build/copy/serialize times and bounded retention. |
| Fallback independence | mandatory protected mode | must be optional from HQ fallback perspective | OWNER REQUIREMENT | WIDE init/calibration failure prevents HQ runtime | Start/test HQ mode with WIDE physically/logically unavailable; no WIDE imports/workers required on hot path unless proven safe and optional. |

## Key conclusion

The strongest current evidence for WIDE is **not** “WIDE is broken.” It is:

1. one bounded path receives valid raw detector outputs and loses them at an acceptance gate; and
2. another test shows a target becomes very small after preprocessing and produces no raw detection.

Both are compatible with HQ-centric assumptions, detector scale limits, current preprocessing choices, or other upstream details. Only the trace can distinguish them.

## Calibration boundary

Physical calibration is required for metric use in all modes, including asymmetric Mode B. It is not a prerequisite for proving that raw detections are being incorrectly rejected, nor should calibration be used as a speculative fix for an upstream detector/filter defect.
