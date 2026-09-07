# SCOUT / INDEPENDENT CAMERA-GEOMETRY FORENSIC

TASK_ID: TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907
STATUS: REVIEW
SCOPE: Repository-safe/read-only analysis only. No TANGRA/Pi5 runtime access. No code/calibration/config changes.

## HYPOTHESIS_VERDICT

VERDICT: STRENGTHENED / MATHEMATICALLY CONSISTENT / NOT VERIFIED.

The hypothesis cannot be refuted from the supplied code. The code VERIFIEDLY couples the requested Picamera2 main-stream dimensions to the same 640x640 canonical dimensions used by Hailo. That establishes a 640x640 acquisition *request*, not the optical provenance/FOV of that frame.

Current official Picamera2 documentation states that the reliable way to request a particular sensor mode is to provide the `sensor` configuration (`output_size`, `bit_depth`), and that Picamera2 tries to choose the best matching sensor mode when the exact mode is not fixed. libcamera defines `ScalerCrop` as the native-sensor rectangle scaled to form the final output image, with maximum value exposed by `ScalerCropMaximum`. Therefore a 640x640 main stream can be produced through sensor/readout/crop/scaler choices not encoded by the application-level `main={size:(640,640)}` request alone.

This does NOT verify that such a crop actually occurs in TANGRA. The actual selected sensor mode, analogue crop, ScalerCrop and ISP mapping remain NOT VERIFIED until direct metadata is captured.

## CODE_EVIDENCE

### VERIFIED from supplied trace
- `FRAME_WIDTH = 640`, `FRAME_HEIGHT = 640`.
- `CAMERA_RESOLUTION = (FRAME_WIDTH, FRAME_HEIGHT)`.
- `HAILO_INPUT_SIZE = (640, 640)`.
- CameraStream sets `self.frame_size=(frame_width,frame_height)`.
- Picamera2 `create_video_configuration(main={"size": self.frame_size, "format":"BGR888"})` requests 640x640.
- No explicit `sensor={...}`, raw sensor mode, `ScalerCrop`, crop rectangle, binning or full-sensor geometry is configured in the supplied application trace.
- `capture_array()` returns the configured main frame.
- Hailo path applies `cv2.resize(frame,(640,640))`; when the incoming application frame is already exactly 640x640, this explicit resize is geometrically identity apart from interpolation implementation details and cannot by itself create a ~2.1 linear scale factor.
- Range code scales calibrated K from 2028x1520 to 640x640 using denominators 2028/1520.

### VERIFIED from current Picamera2/libcamera documentation
- Output stream dimensions and sensor mode selection are distinct concepts.
- Picamera2 exposes `sensor_modes`.
- To ensure a specific sensor mode, the documented method is to provide `sensor={'output_size': mode['size'], 'bit_depth': mode['bit_depth']}`.
- libcamera `ScalerCrop` is a sensor-pixel rectangle that is scaled to form the complete output image; `ScalerCropMaximum` bounds it.

### Implication
Using `fx*640/2028`, `fy*640/1520` is valid only if the actual 640x640 frame is geometrically derived from the same calibrated 2028x1520 optical field by the assumed mapping. That premise is currently NOT VERIFIED.

The config comment stating that FOV values remain uncalibrated until measured in the active 640x640 capture geometry is additional code-level evidence that runtime 640x640 geometry was not yet physically established as equivalent to the calibration geometry. It supports caution; it does not prove a mismatch.

## QUANTITATIVE_COMPATIBILITY

Second object, orientation W=0.019 m H=0.016 m, RAW bbox 78.71x86.79 px, true range 2.585 m:
- current fx640 = 4972.579093 -> Rw = 1.200343 m.
- current fy640 = 6673.069474 -> Rh = 1.230201 m.
- required multiplicative focal/image-scale factors to hit truth: X = 2.153551, Y = 2.101283.
- exact focal values required: fx_required = 10708.703 px, fy_required = 14022.009 px.
- source-equivalent calibrated geometry, if interpreted solely as crop/scale: ~941.700 x 723.367 px mapped to 640x640.

Therefore an upstream optical/image transform producing approximately 2.1x larger detector-space target projection than assumed by the current K scaling is MATHEMATICALLY CONSISTENT with Object2.

This does not identify the mechanism. In the monocular size equation, the following are algebraically confounded for a single object/frame:
- effective focal length being ~2.1x larger than assumed;
- source field/crop being ~2.1x narrower in linear image coordinates before scaling to 640;
- bbox dimensions being uniformly ~2.1x larger than the physical silhouette expected by the assumed class-size geometry.

Cross-experiment evidence from prior reviewed task:
- E88 reverse-solved source-equivalent geometry was ~1006.5x886 px.
- Object2 reverse-solves to ~941.7x723.4 px RAW.
- Thus one exact fixed source rectangle is not supported by both experiments if all physical/bbox measurements are exact.
- A common capture/effective-scale problem plus an E88-specific semantic/clipping/measurement contribution remains MATHEMATICALLY CONSISTENT and STRENGTHENED.

The close Object2 X/Y agreement is compatible with a common approximately isotropic error, but does not distinguish sensor crop from focal error or uniform bbox inflation. A sensor/ISP crop can be anisotropic after final output scaling, and calibration/focal mismatch can also produce similar axis ratios. Direct metadata is required.

## ALTERNATIVES_RANKED

1. **H2/H3 — Picamera2/libcamera sensor-mode crop, analogue crop, ScalerCrop or ISP scaling relative to calibrated field**: STRENGTHENED / leading mechanism class / NOT VERIFIED. Code leaves mode/crop unspecified; official camera stack supports exactly these geometry stages; ~2.1 scale is quantitatively compatible.

2. **Camera acquisition geometry coupled to detector geometry without provenance accounting**: STRENGTHENED. VERIFIED that both requests are 640x640; NOT VERIFIED that this caused a FOV mismatch. This is the central configuration-risk hypothesis.

3. **H6 — detector bbox semantic inflation/padding**: WEAKENED as sole root cause because Object2 has a normal-sized bbox and independently reproduces ~2.1 under-range with close X/Y agreement. Still MATHEMATICALLY CONSISTENT as contributor, especially for E88.

4. **H4 — Hailo preprocessing transform not represented in range intrinsics**: WEAKENED for the explicit application `cv2.resize(640x640 -> 640x640)`, which is effectively identity. Hidden/runtime-internal detector preprocessing remains NOT VERIFIED.

5. **H5 — bbox coordinate transform error**: WEAKENED strongly for the traced RAW -> CA/range -> display chain because RAW and CA dimensions differ sub-percent and DISPLAY_BBOX=RANGE_BBOX. Any hidden internal detector coordinate remap remains NOT VERIFIED.

6. **H8 — physical-dimension/orientation error**: WEAKENED for Object2 because the stated orientation produces close X/Y agreement, while swapped orientation produces strong disagreement. Exact projected silhouette under pose remains NOT VERIFIED.

7. **H9 — calibration itself wrong or no longer representative of current optical state**: NOT VERIFIED / mathematically possible. No evidence currently justifies changing calibration. A mismatch between calibration capture geometry and runtime sensor geometry is distinct from bad intrinsic calibration and is presently more directly supported by the configuration evidence.

8. **CA Kalman smoothing as cause**: REFUTED for the ~2.1 discrepancy by the <0.5% bbox change.

9. **Simple application denominator typo/substitution**: WEAKENED strongly. The traced implementation actually uses 2028 and 1520. The remaining issue is whether those denominators describe the optical field feeding runtime 640x640, not whether the literals are 1014/760.

## MISSING_EVIDENCE

NOT VERIFIED:
- actual IMX477 sensor mode selected for this configuration;
- sensor mode output size and bit depth;
- actual raw/readout geometry;
- camera active array / PixelArraySize;
- analogue crop associated with the chosen mode;
- `ScalerCropMaximum` after configuration;
- current live `ScalerCrop`;
- whether default ScalerCrop equals full calibrated field, selected sensor-mode crop, or another rectangle;
- ISP scaling mapping from sensor/crop rectangle to 640x640 main stream;
- any binning/skipping behavior in the selected mode;
- exact generated configuration before configure and applied `camera_configuration()` after configure;
- whether the active 640x640 stream has the same FOV as the 2028x1520 calibration images;
- hidden Hailo/runtime preprocessing beyond the supplied application trace.

## DECISIVE_PROBE

SINGLE highest-information next action: one read-only Picamera2/libcamera geometry probe on the actual HQ runtime configuration, before any change, capturing both the generated/applied configuration and one live-frame metadata record.

Record exactly:
1. `picam2.sensor_modes` (all modes, including size, bit_depth, fps, crop_limits if exposed).
2. `picam2.camera_properties`, especially `PixelArraySize`, `PixelArrayActiveAreas` if present, and `ScalerCropMaximum` before/after configure where exposed.
3. the exact object returned by `create_video_configuration(main={'size':(640,640),'format':'BGR888'})` BEFORE configure, including `sensor` and `raw` entries if generated.
4. `picam2.camera_configuration()` AFTER configure, including main/raw/sensor fields.
5. actual selected sensor/readout `output_size` and `bit_depth` if exposed.
6. live `picam2.capture_metadata()` from the same frame, especially `ScalerCrop` and any sensor/analogue crop metadata.
7. exact `frame.shape` from `capture_array()`.
8. stream configuration/stride/format for main and raw if present.
9. same-frame detector input shape, RAW bbox, range bbox, display bbox, and actual fx/fy used by range.

Decisive interpretation:
- If the selected mode/ScalerCrop shows that 640x640 is produced from a field materially smaller than the calibrated 2028x1520 field, the capture-geometry mismatch becomes VERIFIED and current simple K scaling premise is REFUTED for runtime.
- If metadata demonstrates that the complete calibrated optical field is preserved into the 640x640 stream under the expected mapping, H2/H3 and the central capture-geometry hypothesis are WEAKENED/REFUTED, shifting priority to hidden detector preprocessing, bbox semantics, physical-dimension correspondence, or calibration representativeness.
- If frame geometry is full-field but detector input/bbox is scaled differently, H4/H5 becomes VERIFIED.

No correction factor, calibration edit, detector-size change or class-dimension change is authorized from this analysis.

## SOURCES / PROVENANCE
- Owner-supplied current TANGRA code trace and physical measurements, 2026-09-07.
- WORKSHOP prior review: `review/TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907.md`.
- Raspberry Pi Picamera2 Manual, current 2026 edition: sensor configuration section states explicit sensor mode selection uses `sensor.output_size` and `sensor.bit_depth`, and exact mode requires exact values.
- libcamera control definition: `ScalerCrop` is the sensor-pixel rectangle scaled to form the final output; maximum is `ScalerCropMaximum`.