# SCOUT / INDEPENDENT GEOMETRY FORENSIC

TASK_ID: TASK-TANGRA-HQ-RANGE-SECOND-OBJECT-FORENSIC-20260907
STATUS: REVIEW

## A. CALCULATION CHECK

Given current runtime intrinsics:
- fx640 = 4972.579093
- fy640 = 6673.069474
- Rtrue = 2.585 m

RAW bbox:
- W = 78.71 px
- H = 86.79 px

CA/range bbox:
- W = 78.356897 px
- H = 86.656647 px

### Orientation A: horizontal=0.019 m, vertical=0.016 m
RAW:
- Rw = 4972.579093*0.019/78.71 = 1.200343 m — VERIFIED FROM GIVEN DATA / arithmetic reproduced
- Rh = 6673.069474*0.016/86.79 = 1.230201 m — VERIFIED FROM GIVEN DATA / arithmetic reproduced
- Required distance multipliers: X=2.153551, Y=2.101284 — MATHEMATICALLY CONSISTENT

CA/range bbox:
- Rw = 1.205752 m — MATHEMATICALLY CONSISTENT
- Rh = 1.232094 m — MATHEMATICALLY CONSISTENT
- CA-vs-RAW change is sub-percent and cannot explain the discrepancy — VERIFIED FROM GIVEN DATA

### Orientation B: horizontal=0.016 m, vertical=0.019 m
RAW:
- Rw = 1.010815 m
- Rh = 1.460863 m
CA/range:
- Rw = 1.015370 m
- Rh = 1.463111 m
This mapping produces strong X/Y disagreement and is therefore WEAKENED by the observed data, though exact object pose/orientation remains NOT VERIFIED.

## B. SECOND-OBJECT RESULT

- With the stated first-axis mapping, both axes under-range by approximately a factor of 2.10–2.15 — VERIFIED FROM GIVEN DATA.
- X/Y agreement is close: RAW axis ranges differ by ~2.5% relative to their mean — VERIFIED FROM GIVEN DATA.
- The normal-sized ~79x87 px bbox reproduces the large range error seen previously with the near-full-width E88 bbox — STRENGTHENED evidence for a common image-geometry/effective-focal or equivalent bbox-scale issue.
- This materially WEAKENS the proposition that the primary range error is only an E88-specific near-saturation/full-width bbox artifact.
- It does NOT identify the upstream mechanism; image scale, effective focal scale, sensor/ISP crop, detector-preprocess geometry, and uniform bbox scaling remain mathematically confounded from range equations alone — NOT VERIFIED.

## C. CROSS-EXPERIMENT COMPARISON

Prior E88 reverse-solved source-equivalent geometry was approximately 1006.5x886 px.
Second object, Orientation A, reverse-solves to approximately:
- RAW: 941.70x723.37 px
- CA/range: 945.94x724.48 px

Therefore:
- Both experiments imply materially smaller effective source geometry than 2028x1520 if interpreted solely as a focal/image-scale transform — MATHEMATICALLY CONSISTENT.
- The implied geometries are not equal, especially in Y — VERIFIED FROM GIVEN DATA.
- ONE exact fixed crop/resize geometry cannot simultaneously explain both experiments if all physical extents, axis mappings, and bboxes are exact — WEAKENED / effectively REFUTED for the exact single-transform values currently reverse-solved.
- A common approximately 2x geometric-scale problem PLUS an E88-specific semantic/clipping/measurement error remains STRENGTHENED and MATHEMATICALLY CONSISTENT.

## D. EFFECTIVE FX/FY AND IMPLIED SOURCE GEOMETRY

Formulae:
- fx_required = Rtrue * bbox_width / physical_width
- fy_required = Rtrue * bbox_height / physical_height
- equivalent_source_width = fx_native * 640 / fx_required
- equivalent_source_height = fy_native * 640 / fy_required

Orientation A, RAW:
- fx_required = 10708.703 px
- fy_required = 14022.009 px
- implied source geometry = 941.700 x 723.367 px

Orientation A, CA/range:
- fx_required = 10660.662 px
- fy_required = 14000.465 px
- implied source geometry = 945.944 x 724.481 px

Orientation B, RAW:
- fx_required = 12716.584 px
- fy_required = 11808.008 px
- implied source geometry = 793.011 x 858.999 px

Orientation B, CA/range:
- fx_required = 12659.536 px
- fy_required = 11789.865 px
- implied source geometry = 796.585 x 860.321 px

Comparison with E88 ~1006.5x886:
- Orientation A X differs by ~6.4%; Y differs by ~18.4%.
- Orientation B is farther from E88 in X and closer in Y but produces poor same-object X/Y range agreement.
- No exact common fixed source rectangle is supported by both experiments from current evidence — VERIFIED FROM GIVEN DATA.

## E. UPDATED HYPOTHESIS RANKING

1. H7 — E88-specific clipping/saturation/semantic measurement issue PLUS a separate common geometry/effective-scale error: STRENGTHENED / leading composite hypothesis.
2. H2/H3 — Picamera2/libcamera sensor-mode crop or ScalerCrop/ISP crop/digital zoom: STRENGTHENED as classes of common upstream geometry error; specific crop values NOT VERIFIED.
3. H4 — detector preprocessing transform not represented in range intrinsics: STRENGTHENED / MATHEMATICALLY CONSISTENT.
4. H5 — bbox coordinate transformation error: MATHEMATICALLY CONSISTENT but WEAKENED as a simple post-detector display/range mismatch because RAW and CA/range bboxes differ only sub-pixel and DISPLAY_BBOX=RANGE_BBOX in the trace.
5. H6 — bbox semantic mismatch / detector padding: WEAKENED as sole root cause, but remains MATHEMATICALLY CONSISTENT as a contributor, especially for E88.
6. H1 — application focal-scaling denominator bug: WEAKENED strongly by traced denominators 2028 and 1520; NOT fully refuted for untraced alternate paths, but no positive evidence remains.
7. H8 — physical dimension/orientation error: swapped orientation is WEAKENED by poor X/Y agreement; measurement correspondence and exact projected extents remain NOT VERIFIED.
8. H9 — calibration itself wrong: MATHEMATICALLY CONSISTENT in the abstract but NOT VERIFIED and not supported by current evidence; do not change calibration.

## F. WHAT THE NEW EVIDENCE WEAKENS OR REFUTES

- Primary-error-is-only-E88-bbox hypothesis: WEAKENED materially.
- Exact 1014x760 ROI explanation: WEAKENED; second-object reverse solution is not 1014x760.
- Exact one-fixed-transform explanation using the two current reverse-solved rectangles: REFUTED under the assumption that both experiments' physical extents and axis mappings are exact.
- CA Kalman bbox modification as cause: REFUTED by sub-pixel RAW-to-range difference.
- Swapped 0.016/0.019 axis mapping as the best explanation: WEAKENED.
- Application denominator substitution 1014-for-2028: strongly WEAKENED by direct implementation trace.

## G. WHAT REMAINS NOT VERIFIED

- Actual Picamera2 sensor mode and sensor active-array geometry.
- libcamera ScalerCrop/current crop metadata.
- Whether the 640x640 BGR stream represents the full calibrated FOV or a sensor/ISP-selected subregion.
- Any analogue crop/binning/skipping/scaler behavior upstream of application code.
- Exact Hailo preprocessing geometry beyond the traced direct 640x640 application handoff.
- Whether bbox coordinates are transformed internally by Hailo/runtime before exposure.
- Exact projected physical extents of the miniature object under pose/perspective; 0.019x0.016 are measured object dimensions, not independently verified image-plane silhouettes.
- Exact semantic support of detector bbox versus physical edges.
- Calibration as root cause.

Close X/Y agreement on the second object does NOT distinguish image-scale error from focal-scale error, uniform bbox-scale error, or sensor/ISP crop. Those mechanisms are algebraically equivalent in the monocular size equation for a single frame. Direct geometry metadata is required.

## H. SINGLE DECISIVE NEXT TEST

Capture ONE live HQ frame and persist one same-frame geometry ledger with Picamera2/libcamera metadata and all bbox stages:

1. camera sensor mode / sensor resolution / active-array or raw/full sensor dimensions;
2. current ScalerCrop (or equivalent crop rectangle) metadata and any analogue/sensor crop exposed by libcamera;
3. configured stream output geometry = 640x640 and ISP scaling relation from crop rectangle to output;
4. exact 640x640 frame delivered to application;
5. exact detector input geometry/preprocess metadata;
6. RAW detector bbox;
7. range bbox;
8. display bbox;
9. actual fx/fy values used for that frame.

Decisive criterion:
- If metadata shows a crop/scaler rectangle smaller than the calibrated optical field, H2/H3 becomes VERIFIED and effective intrinsics can be derived from the observed transform.
- If metadata shows full calibrated field mapped to 640x640 with no crop, H2/H3 are weakened/refuted and attention shifts to H4/H5/H6 or calibration.
- If detector input/bbox scaling differs from the application 640x640 frame geometry, H4/H5 becomes VERIFIED.
- No empirical correction factor is authorized.