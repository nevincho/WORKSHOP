# LIVE / PHYSICAL ADDENDUM — TANGRA HQ DUAL-STREAM METRIC PATH

TASK_ID: TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908
DATE: 2026-09-08
MODE: EVIDENCE ADDENDUM / NO IMPLEMENTATION

## 1. HQ runtime observability

### VERIFIED — operator/runtime observation
- Current authoritative HQ application path remains `HQ Picamera2 -> CameraStream.read() -> main.py (~1494) -> 640x640 runtime frame`.
- Current telemetry reports HQ processing frame size 640x640.
- Existing attempted read-only HQ snapshot endpoint returned HTTP 404.
- No sufficiently recent dataset capture was available under the unchanged-runtime constraint.

### Interpretation
The inability to extract a current HQ image is an **observability limitation**, not evidence of camera failure. Current live sensor mode, ScalerCrop, ISP mapping and actual 640x640 FOV remain NOT_VERIFIED.

## 2. Calibration space versus AI space

### VERIFIED
Physical HQ calibration authority remains:
- calibration space: 2028x1520
- fx = 15756.86
- fy = 15848.54
- cx = 1014.00
- cy = 760.00
- D = [0,0,0,0,0]

Current runtime/AI geometry remains 640x640.

### Architectural consequence
Metric computation must preserve an explicit deterministic relationship between calibrated HQ space and AI 640x640 space. Either a logical calibration-consistent metric representation or pure AI->calibration geometry back-projection is acceptable in principle. No reconstructed 2028x1520 image is required merely to transform object coordinates.

## 3. Object-geometry back-projection clarification

### VERIFIED requirement
The required inverse operation is geometric only:
`AI bbox/centre/corners/keypoints -> inverse crop/resize/offset transform -> virtual coordinates in calibrated 2028x1520 space`.

No synthetic full-resolution pixel reconstruction is required.

### Hard validity limit
Geometry outside the AI-observable region is non-observable and MUST NOT be invented. If the physical extent used by class-size ranging is clipped outside the AI field/ROI, that dimension is invalid as direct metric evidence.

## 4. F450 physical setup

### VERIFIED physical observation
- F450 was initially positioned at approximately 2.58 m from the HQ camera.
- At that position the carrier did not fit fully within the narrow HQ + 50 mm view.
- It was moved to an exactly measured lens-to-F450 distance of 4.000 m.
- HQ focus was not changed.

### NOT VERIFIED
Full F450 visibility at 4.000 m is NOT_VERIFIED because no current HQ image could be extracted without violating the unchanged-runtime/read-only constraint.

### Measurement rule
Nominal `F450` dimensions are not automatically valid physical priors. Future range validation must use a directly measured rigid landmark-to-landmark span corresponding to the measured image extent. Irregular silhouette or propeller envelope is unsuitable unless mechanically fixed and explicitly measured.

## 5. E88 live classification observation

### VERIFIED operator observation
With the same physical E88 target in the restored desk scene at approximately 2.58 m, detector class changed among at least:
- FPV
- Orlan-10
- Talay

This observation alone MUST NOT be labelled detector failure.

## 6. E88 silhouette variability

### VERIFIED physical fact / observation
The E88 uses folding/free-moving propellers. Their orientation is not fixed, so visible width, height, diagonals and arm/rotor silhouette can change while the body remains stationary.

### HYPOTHESIS
Variable silhouette may materially contribute to the observed class changes. It is NOT VERIFIED as the sole cause.

### RECOMMENDATION
Use E88 primarily as a detection/classification/robustness stimulus. Do not use its unconstrained whole silhouette as a high-quality metric ground-truth target unless propellers and pose are mechanically fixed and the corresponding real dimensions are measured.

## 7. Class-size range provenance risk

### VERIFIED architectural property
Class-size range depends on both image geometry and the selected physical-size prior. Therefore the same target/bbox can produce different ranges when class identity changes and class profiles differ.

### REQUIRED FOLLOW-UP TRACE
Before metric promotion, trace whether existing range estimation consumes:
- instantaneous detector class;
- CurrentTarget-stabilized class;
- another temporally stabilized class identity;
- another provenance source.

Do not modify detector authority as part of Task A. This is a range-path robustness/provenance question.

## 8. Prior printed E88 stimulus

### VERIFIED prior evidence
For a test-only 17 cm x 11 cm physical-size calculation at measured 2.585 m:
- bbox width = 639.632535 px
- bbox height = 374.182209 px
- fx runtime = 4972.579093 px
- fy runtime = 6673.069474 px
- Rw = 1.321600 m
- Rh = 1.961712 m
- combined = 1.610155 m
- absolute error = 0.975 m
- percentage error = 37.72%

The formula was internally coherent, but the printed silhouette/box did not provide a trustworthy one-to-one mapping between bbox width/height and physical width/height.

### Consequence
This result is not evidence that camera calibration is wrong. It remains evidence of strong sensitivity to bbox-to-physical-dimension correspondence.

## 9. Prior tiny Shahed model test

### VERIFIED prior evidence
Tiny model dimensions:
- length = 0.019 m
- width = 0.016 m
- true range = 2.585 m

The target was classified as Shahed while the production full-size Shahed profile was intentionally retained, yielding mean range about 159.293 m and about 6062% error.

### Interpretation
This was a deliberate physical-size-prior mismatch. It does NOT demonstrate unstable camera geometry or calibration failure. Production Shahed dimensions remain protected/unchanged.

## 10. Updated Task A architecture disposition

The live/physical observations reinforce, rather than replace, the prior architecture verdict:

**VIABLE_WITH_CONDITIONS**

Preferred topology remains:
`ONE HQ acquisition authority -> explicit calibration-consistent geometry -> deterministic AI 640x640 geometry -> existing Hailo -> NanoTracker -> CA Kalman -> CurrentTargetManager -> project authoritative object geometry into calibration space -> class-size range/LOS -> HOROS`.

Metric processing remains downstream of the protected tracking/target authority.

Forbidden architecture drift remains:
- no second tracker;
- no second CurrentTarget authority;
- no duplicate independent HQ camera capture.

Minimum future boundary remains:
- camera geometry metadata;
- frame/timestamp identity;
- deterministic AI transform;
- inverse object-geometry projection;
- metric/class provenance.

## 11. Updated validation decomposition

Before metric promotion, validation MUST isolate these domains instead of combining them into one range PASS/FAIL:

### A. CAMERA GEOMETRY
Known rigid object span + known pixel span + known range. Establish sensor/crop/FOV geometry independently of class semantics.

### B. COORDINATE TRANSFORM
Known calibration-space points -> forward AI transform -> inverse transform -> recovery error.

### C. CLASS PRIOR
Hold image geometry fixed; vary class profiles deliberately; quantify range sensitivity and trace actual class provenance used by range_estimator.

### D. SILHOUETTE VARIABILITY
Use a fixed object with movable geometry such as E88 propellers; quantify bbox and class variation. Do not confuse this with camera calibration error.

### E. FRAME IDENTITY
Detector observation from frame N must remain associated with geometry/transform from frame N and correct CurrentTarget generation.

### F. PERFORMANCE
The complete authoritative HQ path must remain >25 FPS. Geometry correctness does not excuse performance regression.

## Updated evidentiary conclusion

- Camera calibration failure: NOT_VERIFIED.
- Current 640x640 optical provenance: NOT_VERIFIED.
- Explicit calibration<->AI geometry contract requirement: STRENGTHENED.
- E88 as unconstrained metric calibration target: WEAKENED / NOT RECOMMENDED.
- E88 as detection/classification robustness stimulus: RECOMMENDED.
- Class identity provenance as a range-risk variable: STRENGTHENED and requires direct code-path trace.
- Task A architecture verdict: unchanged — VIABLE_WITH_CONDITIONS.
