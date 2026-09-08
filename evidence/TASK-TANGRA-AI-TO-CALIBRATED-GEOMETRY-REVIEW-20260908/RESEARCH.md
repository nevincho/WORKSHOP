# RESEARCH — TANGRA AI GEOMETRY → CALIBRATED HQ GEOMETRY

TASK_ID: TASK-TANGRA-AI-TO-CALIBRATED-GEOMETRY-REVIEW-20260908
STATUS: REVIEW
MODE: RESEARCH / FORENSIC DESIGN REVIEW ONLY

## A. CURRENT_FORWARD_TRANSFORM

### VERIFIED
- Calibration coordinate space: 2028x1520.
- K = [[15756.86,0,1014],[0,15848.54,760],[0,0,1]], D=[0,0,0,0,0].
- Current application AI frame is 640x640.
- Prior trace found Picamera2 main requested as 640x640 BGR888 and Hailo input 640x640; application Hailo resize 640x640→640x640 is effectively identity.

### NOT_VERIFIED
The exact physical forward transform from the calibrated optical field to the current 640x640 runtime frame is not yet known because selected sensor mode, analogue crop, ScalerCrop, ISP scaling and any upstream crop remain unmeasured. Therefore the live transform must not be hard-coded as simple 2028x1520→640x640 stretch until the direct Picamera2/libcamera probe proves it.

### INFERRED mathematical baseline
If, only as a proof case, the complete calibrated field is anisotropically resized directly to 640x640 with no crop/pad/rotation:
- sx = 640/2028 = 0.3155818540
- sy = 640/1520 = 0.4210526316
- u_ai = sx*u_cal
- v_ai = sy*v_cal
This is a valid mathematical case, not a VERIFIED description of the current camera pipeline.

## B. MATHEMATICAL_MODEL

Use homogeneous image coordinates p=[u,v,1]^T.

For the common crop→resize→pad path:
- crop origin in calibrated coordinates: (x0,y0)
- crop size: (Wc,Hc)
- AI/content size after resize: sx,sy
- output padding/offset: (px,py)

Forward mapping:

p_ai = A p_cal

A = [[sx, 0, px - sx*x0],
     [0, sy, py - sy*y0],
     [0,  0, 1]]

Equivalent scalar form:
- u_ai = sx*(u_cal-x0)+px
- v_ai = sy*(v_cal-y0)+py

This covers direct resize, non-uniform stretch, centered/non-centered crop and letterbox padding. Rotation/flip can be incorporated by multiplying A by the corresponding invertible 2D homogeneous transform. A general perspective warp would use an invertible homography H instead of affine A. Nonlinear warps require an explicit nonlinear inverse and are not covered by a single 3x3 affine matrix.

## C. INVERSE_TRANSFORM

When sx != 0 and sy != 0 and the applied mapping is known:

p_cal = A^-1 p_ai

Scalar form:
- u_cal = (u_ai-px)/sx + x0
- v_cal = (v_ai-py)/sy + y0

### Fully invertible geometry, subject to visibility
- arbitrary point: YES
- bbox center: YES
- bbox corners: YES
- bbox width: w_cal = w_ai/sx, provided neither edge was clipped and both edges correspond to the same physical extent
- bbox height: h_cal = h_ai/sy, same condition
- tracker coordinates: YES if they are expressed in the same AI image coordinate system
- keypoints/markers: YES pointwise

### Hard limitation
The inverse mapping reconstructs coordinates only. It cannot reconstruct pixels or object extent that was never present in the AI-visible image. If crop, clipping, detector truncation or occlusion removed a required physical boundary, its location is non-observable and MUST NOT be invented.

## D. K_TRANSFORMATION

For a known image-coordinate transform p_ai=A p_cal, the camera matrix in AI coordinates is:

K_ai = A K_cal

For crop→resize→pad:
- fx_ai = sx*fx
- fy_ai = sy*fy
- cx_ai = sx*(cx-x0)+px
- cy_ai = sy*(cy-y0)+py

For the simple full-field anisotropic 2028x1520→640x640 proof case:
- fx_ai = 4972.5790927
- fy_ai = 6673.0694737
- cx_ai = 320
- cy_ai = 320

These are exactly the currently calculated scaled values for the simple full-field resize assumption. The unresolved issue is not the algebra; it is whether that assumed A matches the real capture geometry.

## E. EQUIVALENCE_PROOF

METHOD A:
1. AI geometry p_ai.
2. Back-project: p_cal=A^-1 p_ai.
3. Use original K_cal.

METHOD B:
1. Keep p_ai.
2. Use K_ai=A K_cal.

Proof for ray geometry:

K_ai^-1 p_ai
= (A K_cal)^-1 (A p_cal)
= K_cal^-1 A^-1 A p_cal
= K_cal^-1 p_cal.

Therefore both produce the same normalized camera ray when A is exact and invertible.

For class-size range along X:
- w_ai = sx*w_cal
- fx_ai = sx*fx
- R_ai = fx_ai*W_phys/w_ai
       = sx*fx*W_phys/(sx*w_cal)
       = fx*W_phys/w_cal = R_cal.

The same proof holds independently for Y with sy. Thus anisotropic resize is not intrinsically a problem if sx and sy are handled independently and the correct K_ai or inverse geometry mapping is used.

### Synthetic round-trip proof case
Assume simple full-field anisotropic resize and calibrated points:
- bbox TL=(900,600)
- bbox BR=(1100,800)
- principal point=(1014,760)

Forward to AI:
- TL=(284.0236686,252.6315789)
- BR=(347.1400394,336.8421053)
- principal point=(320,320)

Inverse using 1/sx and 1/sy recovers exactly:
- TL=(900,600)
- BR=(1100,800)
- principal point=(1014,760)

Floating-point round-trip error in this analytic case is effectively zero. Real errors are dominated by bbox/keypoint uncertainty and transform provenance, not floating-point scaling.

## F. CROP/RESIZE/LETTERBOX_CASES

### Case 1 — full-field anisotropic resize
A=diag(sx,sy,1). Fully invertible for all visible coordinates. Use separate fx/fy scaling. Object aspect ratio in AI is altered by sx/sy, but metric geometry remains recoverable.

### Case 2 — crop/ROI then resize
u_ai=sx*(u_cal-x0), v_ai=sy*(v_cal-y0). Principal point moves to (sx*(cx-x0), sy*(cy-y0)). Coordinates inside the crop are invertible. Anything outside the crop is unobservable.

### Case 3 — letterbox
For uniform scale s and padding (px,py):
- u_ai=s*(u_cal-x0)+px
- v_ai=s*(v_cal-y0)+py
Padding must be removed before inverse mapping. Detector boxes intersecting padded regions require clipping/validity checks.

### Case 4 — center crop to square
Same as crop case with x0/y0 defined by crop geometry. This narrows FOV. Inverse coordinates are valid only within that cropped calibrated rectangle.

### Case 5 — rotation/flip
Still invertible if transform is known and applied consistently; bbox corners should be transformed as points then re-bounded, rather than assuming width/height scalar scaling after 90-degree rotations.

### Case 6 — nonlinear warp / undocumented ISP geometry
NOT_VERIFIED / unsafe for simple affine back-projection until the exact mapping is established.

## G. ERROR_BUDGET

### Transform arithmetic
With float32/float64 scaling, numerical error is negligible relative to detector/tracker uncertainty for these image sizes.

### Quantization
Under simple full-field mapping:
- 1 AI pixel corresponds to 2028/640 = 3.16875 calibrated X pixels.
- 1 AI pixel corresponds to 1520/640 = 2.375 calibrated Y pixels.
- half-pixel AI quantization corresponds to ~1.584 calibrated X px and ~1.188 calibrated Y px.

This coordinate amplification does not by itself create a metric bias because K scales consistently, but it limits spatial precision.

### Bbox range sensitivity
For R=f*W/w, first-order relative range error from bbox-size error is approximately |dR/R|≈|dw/w|, ignoring focal/profile uncertainty.
For Object2-size bboxes (~78.7x86.8 px):
- 1 px width error ≈1.27% range error.
- 1 px height error ≈1.15% range error.
Detector jitter of several pixels can therefore dominate transform-rounding error.

### High-risk error sources
1. wrong A / wrong crop provenance — systematic error, potentially very large;
2. bbox clipping at AI frame boundary — invalid physical extent;
3. semantic bbox inflation/under-coverage — systematic class-size range error;
4. stale detector/tracker geometry applied to wrong frame — temporal/spatial error;
5. wrong physical dimension/profile or wrong axis correspondence — systematic error;
6. integer rounding too early in the pipeline — avoidable precision loss.

RECOMMENDATION: retain floating-point coordinates through transform/range calculations and round only for UI rendering.

## H. RANGE_INTEGRATION

### Coordinate reconstruction versus image reconstruction
RECOMMENDATION: do not generate a synthetic 2028x1520 image merely for class-size range or LOS. Transform the authoritative AI geometry mathematically.

### Method A — preferred for calibration traceability
- retain Hailo/NanoTracker/CA in AI coordinates;
- attach exact GeometryTransform A plus frame/config generation;
- transform authoritative bbox center/corners into calibrated HQ coordinates;
- use original calibrated K for LOS and class-size geometry.

### Method B — equally valid mathematically
- keep authoritative geometry in AI coordinates;
- derive K_ai=A*K;
- use K_ai directly.

RECOMMENDATION: Method A is easier to audit against the physical calibration and HOROS LOS provenance; Method B may be computationally simpler for some hot-path operations. They should be regression-tested against each other as an invariant.

### Existing authority
- NanoTracker: unchanged; remains authoritative tracker.
- CA Kalman: unchanged; remains authoritative image-space temporal estimator.
- CurrentTargetManager: unchanged authority; target geometry gains coordinate-space/frame provenance, not a second target state.
- range_estimator.py: smallest later boundary is accepting explicitly tagged geometry/K rather than assuming bare 640x640 scale.
- target_profiles.py: no profile changes; physical-size validity remains separate from coordinate transform validity.
- HOROS LOS_RANGE: consume LOS/range with timestamp, frame ID, calibration ID and uncertainty/provenance.

### Bbox semantic rule
A transformed bbox is metrically valid only to the extent that its edge corresponds to the physical dimension being used. Coordinate correctness does not make a semantically wrong bbox a correct physical measurement.
- width-based range: valid only when horizontal bbox extent corresponds to the selected physical width and both relevant edges are visible/unclipped;
- height-based: analogous for height;
- combined range: only when both axis measurements independently satisfy their semantic/visibility validity gates. Do not average one valid and one invalid axis merely to obtain a number.

## I. FAILURE_MODES

1. Wrong live A assumed from output dimensions alone.
2. Hidden sensor/ScalerCrop changes without transform-generation update.
3. Applying inverse transform from one configuration to another frame.
4. Bbox clipped by AI crop/frame edge but treated as full physical extent.
5. Letterbox padding interpreted as scene pixels.
6. Late Hailo result associated with newer metric timestamp/CurrentTarget generation.
7. Integer coordinate truncation before inverse mapping.
8. Semantic bbox extent not equal to physical profile extent.
9. Crop excludes part of target; inverse transform invents invisible boundary — forbidden.
10. Rotation/flip omitted from A.
11. Future distortion/rectification step added without updating transform contract.
12. Multiple competing coordinate-space assumptions in range/HOROS code.

## J. REQUIRED_CODE_TOUCHPOINTS

RECOMMENDATION / future only; NO IMPLEMENTATION AUTHORIZED:
1. camera/preprocess boundary: expose immutable per-configuration GeometryTransform metadata (source calibration space, crop, scale, pad, orientation, config generation).
2. Hailo submission/result envelope: carry frame_id, SensorTimestamp/config generation and coordinate-space ID.
3. target geometry object / CurrentTarget payload: explicitly tag coordinate space and transform provenance; do not duplicate target authority.
4. small geometry adapter: point/bbox/keypoint AI↔calibrated mapping with visibility/clipping validation.
5. range_estimator.py: consume calibrated geometry+original K or AI geometry+derived K_ai through explicit contract; remove implicit geometry assumptions only after tests.
6. HOROS LOS_RANGE ingress: persist frame/timestamp/calibration/geometry provenance and measurement age.
7. tests only: Method-A/Method-B equivalence and round-trip cases.

## K. MINIMUM_IMPLEMENTATION_PLAN

Future smallest bounded change, if authorized after the live geometry probe:
1. establish VERIFIED forward transform A for the active camera configuration;
2. represent A and A^-1 as a tested immutable geometry contract;
3. carry frame/config identity through detector→tracker→CA→CurrentTarget geometry;
4. add geometry-only AI→calibrated mapping adapter;
5. route range/LOS through calibrated geometry with original K, leaving tracking authority untouched;
6. reject clipped/out-of-visible-region physical extents rather than extrapolating them;
7. benchmark >25 FPS and regression-test Method A vs Method B.

No full-resolution image stream is required by this minimum plan.

## L. VALIDATION_PLAN

1. Geometry-probe gate: capture actual sensor mode, ScalerCrop, stream geometry and preprocessing; derive A from evidence.
2. Deterministic unit tests for direct resize, anisotropic resize, crop, letterbox, flip/rotation if used.
3. Round-trip test: calibrated points/bboxes→AI→calibrated; sub-pixel tolerance.
4. K-equivalence test: compare normalized rays and class-size ranges from Method A and Method B across thousands of synthetic points/bboxes.
5. Boundary tests: boxes touching/crossing crop/AI edges must flag invalid physical extent where appropriate.
6. Same-frame identity tests: stale/mismatched transform generation or frame ID must be rejected.
7. Physical known-distance test after geometry is proven; compare width/height separately and record semantic bbox validity.
8. HOROS ingress test: LOS/range result carries correct timestamp, calibration ID, uncertainty and age.
9. Performance regression: sustained operational FPS >25; no stale queue/backlog introduced; measure p95 latency/minimum FPS, not average only.

## M. COMPARISON_WITH_DUAL_STREAM

| Dimension | Geometry back-projection only | Separate calibration-preserving metric stream |
|---|---|---|
| Metric correctness | Equal when A is exact and required object geometry is visible | Strong when calibrated stream itself is proven; can retain pixels unavailable to AI |
| CPU/RAM/bandwidth | Lowest; transforms only points/bboxes | Higher, especially if full-resolution BGR is materialized/copied |
| Latency | Very low arithmetic cost | Potential ISP/copy/buffer latency |
| Complexity | Low-medium; transform provenance must be rigorous | Medium-high; multiple stream/buffer contracts |
| Calibration traceability | Excellent with Method A + original K | Excellent if stream geometry exactly matches calibration |
| Synchronization risk | Low if one AI frame carries A/frame ID | Higher if streams are consumed independently; mitigated if same request ID/timestamp |
| Lost-FOV recovery | Impossible; cannot reconstruct cropped-out scene | Possible only if metric stream actually preserves wider calibrated FOV |
| Pixel-level metric algorithms | Not available unless AI frame suffices | Supports ROI/keypoint/photometric algorithms needing calibrated pixels |
| Suitability for class-size range/LOS/HOROS | High when geometry/visibility gates pass | High but potentially unnecessarily expensive |
| Performance risk | Lowest | Higher, must benchmark memory/ISP/copy cost |

### Architectural decision rule
RECOMMENDATION: prefer geometry back-projection as the minimum solution if the direct camera probe proves a stable deterministic transform from calibration field to AI frame AND all required metric evidence is observable in that AI field. Escalate to a calibration-preserving secondary/main metric stream only if the AI path physically discards required FOV/pixels or future metric algorithms genuinely require calibrated image content rather than geometry.

## N. VERDICT

**VIABLE_WITH_CONDITIONS — RECOMMENDED AS THE MINIMUM ARCHITECTURE IF THE LIVE FORWARD TRANSFORM IS VERIFIED.**

VERIFIED:
- the mathematical equivalence of Method A and Method B for an exact invertible image-coordinate transform;
- anisotropic scaling is safe when sx/sy and K are transformed consistently;
- coordinate back-projection requires no synthetic pixels/full image;
- clipping/cropping cannot be inverted into information that was never observed.

INFERRED:
- geometry-only back-projection is likely the lowest-cost architecture for current class-size range + LOS/HOROS needs.

NOT_VERIFIED:
- the exact active TANGRA camera→640 transform A;
- whether current 640x640 preserves the full calibration FOV;
- whether hidden Hailo preprocessing changes geometry;
- whether all future metric functions can operate from geometry only.

RECOMMENDATION:
Do not implement until the direct Picamera2/libcamera geometry probe establishes the real sensor/crop/resize chain. Once A is evidence-backed, validate Method A and Method B as mathematical invariants and choose geometry back-projection unless a demonstrated pixel/FOV requirement justifies a second calibrated stream.

## External geometry provenance
Current libcamera documentation states that sensor configuration can be selected separately from output streams and that digital zoom/cropping uses ScalerCrop followed by scaling to output size. ScalerCrop is expressed in native sensor pixels. This supports treating crop+scale as explicit transform provenance rather than inferring it from 640x640 output dimensions alone.