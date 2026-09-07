# REVIEW — TANGRA HQ 640x640 CAPTURE GEOMETRY FORENSIC

TASK_ID: TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907
VERDICT: PASS
STATUS: COMPLETE

## REVIEW FINDINGS

The forensic evidence satisfies the bounded read-only objective. No runtime/Pi5 access, code mutation, calibration change, detector-size change, class-size change, correction constant, or Codex use occurred.

### HYPOTHESIS VERDICT
**STRENGTHENED / MATHEMATICALLY CONSISTENT / NOT VERIFIED.**

The supplied code does not prove a sensor/ISP crop, but it does prove that 640x640 is both the Picamera2 main-stream request and Hailo canonical size. This means detector geometry and requested camera output geometry are coupled at configuration level.

That coupling is potentially unsafe for intrinsics provenance because current Picamera2/libcamera documentation distinguishes output-stream size from sensor-mode/readout/crop geometry. A specific sensor mode is only guaranteed when explicitly selected; `ScalerCrop` is a separate sensor-pixel rectangle scaled into the final output.

Therefore the premise required by `fx*640/2028`, `fy*640/1520` — that the runtime 640x640 frame preserves the calibrated 2028x1520 optical field under the assumed mapping — remains NOT VERIFIED.

### QUANTITATIVE REVIEW
Second-object arithmetic was rechecked against prior reviewed evidence:
- Rw = 1.200343 m, Rh = 1.230201 m at true 2.585 m.
- required scale/focal ratios = 2.153551 (X), 2.101283 (Y).
- required focal values = 10708.703 px, 14022.009 px.
- crop/scale-equivalent source geometry if that mechanism alone explains the error = ~941.700 x 723.367 px -> 640x640.

Thus a materially narrower upstream field mapped into 640x640 is quantitatively compatible with the observed ~2.1 under-range. The numbers do not prove physical ROI or a specific sensor mode.

### REFUTATION ATTEMPT
The central hypothesis is NOT refuted by current code evidence because no sensor mode, raw/readout geometry, ScalerCrop or metadata proving full calibrated FOV is present in the supplied trace.

However, several narrower explanations are weakened/refuted:
- CA smoothing: REFUTED as primary cause by sub-percent bbox change.
- explicit application Hailo resize: WEAKENED strongly because traced input is already 640x640 and resize is geometrically identity.
- simple application denominator typo/substitution: WEAKENED strongly; code uses 2028/1520 as traced.
- simple RAW->range/display bbox remap error: WEAKENED strongly by same-coordinate evidence and sub-pixel CA change.
- E88-only bbox pathology as sole cause: WEAKENED by independent Object2 reproduction.

### UPDATED LEADING RANKING
1. Picamera2/libcamera sensor-mode / analogue-crop / ScalerCrop / ISP geometry mismatch relative to calibration — STRENGTHENED, NOT VERIFIED.
2. General acquisition-geometry/detector-geometry coupling without intrinsics provenance — STRENGTHENED.
3. bbox semantics/inflation as contributor — MATHEMATICALLY CONSISTENT, WEAKENED as sole cause.
4. hidden detector/runtime preprocessing — NOT VERIFIED; explicit cv2.resize path itself is weak.
5. physical projected-dimension mismatch — NOT VERIFIED / WEAKENED by Object2 axis agreement.
6. calibration itself wrong — NOT VERIFIED; no evidence authorizes calibration change.

### SINGLE DECISIVE NEXT TEST
PASS recommendation: one read-only Picamera2/libcamera geometry probe on the actual HQ configuration, recording:
- `sensor_modes`;
- `camera_properties` / PixelArraySize and active areas if exposed;
- generated `create_video_configuration(...)` result before configure;
- `camera_configuration()` after configure;
- selected sensor output_size/bit_depth/raw mode;
- `ScalerCropMaximum`;
- same-frame `capture_metadata()` including live `ScalerCrop`;
- actual `frame.shape` and stream configuration;
- same-frame detector input shape, RAW bbox, range bbox, display bbox and actual fx/fy used.

This direct metadata observation is the highest-information discriminator. Another distance calculation alone cannot separate focal-scale, image-scale, bbox-scale and sensor/ISP crop hypotheses.

## DEFINITION OF DONE
- objective tested: PASS
- adversarial refutation attempted: PASS
- quantitative compatibility checked: PASS
- alternatives ranked/classified: PASS
- missing evidence explicit: PASS
- one decisive probe specified: PASS
- protected scope preserved: PASS
- repository hygiene: PASS; only canonical task/evidence/review artifacts created
- target runtime validation: NOT VERIFIED and not claimed

No checkpoint is required because no target implementation changed.