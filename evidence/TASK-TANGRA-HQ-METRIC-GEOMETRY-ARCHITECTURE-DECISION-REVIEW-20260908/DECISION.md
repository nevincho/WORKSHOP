# DECISION — TANGRA HQ METRIC GEOMETRY: TASK A vs TASK B

TASK_ID: TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908
MODE: COMPARATIVE REVIEW ONLY
STATUS: REVIEW

## A. EXECUTIVE COMPARISON

**RECOMMENDATION: HYBRID_MINIMAL_FIRST.**

**FINAL ARCHITECTURAL POSITION:** implement the **Task B geometry-back-projection boundary first**, but do so inside the broader Task A architecture contract so that calibrated pixel/ROI consumers can be added later without changing the protected tracking authority.

This means:
- one HQ acquisition authority;
- one Hailo path;
- one NanoTracker;
- one CA Kalman;
- one CurrentTargetManager;
- one HOROS authority;
- explicit camera-geometry provenance;
- explicit `A` / `A^-1` calibration↔AI transform;
- project authoritative AI object geometry back into calibration coordinates for current range/LOS/HOROS;
- do **not** retain or duplicate a full calibrated metric image stream unless a future consumer proves it needs pixels/ROI rather than geometry only.

### Classification
- Task A and B are mutually exclusive: **NOT SUPPORTED**.
- B as the minimal current solution while A remains the extensible architecture: **SUPPORTED_BY_EXISTING_REVIEW**.
- Exact production implementation readiness today: **NOT_VERIFIED**, because the live forward transform remains unknown.

## B. A_VS_B_TABLE

| Criterion | Task A — calibration-consistent logical metric geometry + AI geometry | Task B — AI geometry back-projection only | Comparative decision |
|---|---|---|---|
| Metric correctness | **SUPPORTED_BY_EXISTING_REVIEW**. Strong traceability if metric representation is explicitly tied to calibration geometry. | **SUPPORTED_BY_EXISTING_REVIEW**. Equally correct for geometry-only consumers when exact forward transform `A` is VERIFIED; `AI -> A^-1 -> calibrated coordinates -> original K` is mathematically valid. | Tie on geometry correctness **if A is known**. |
| Additional assumptions | Needs explicit mapping between camera acquisition/calibration geometry and AI stream; if using multi-stream, stream-to-stream transform must be proven. | Needs exact invertible forward transform and required object extent to remain observable in AI domain. | B has fewer runtime data products but stronger dependence on visibility/invertibility. |
| Crop/ROI/letterbox | Can preserve calibrated geometry separately while AI path crops/pads, provided correspondence is explicit. | Handles crop/resize/pad mathematically inside the observable region; cannot recover cropped-away information. | A is more information-preserving; B is sufficient if current metric evidence remains visible. |
| Information retention | Can retain calibrated pixels/ROI if needed. | Retains only geometry/provenance; removed pixels/FOV are unrecoverable. | A wins only for future pixel-dependent consumers. |
| CPU | Potentially higher if application generates/retains calibrated stream and AI transform. ISP multi-stream may reduce cost but is NOT_VERIFIED. | Minimal arithmetic cost for coordinate transforms; no full-resolution reconstruction. | B preferred. |
| RAM | Potentially higher buffer footprint. | Minimal incremental state. | B preferred. |
| Memory bandwidth | Major A risk if full 2028x1520 BGR buffers are copied/retained; prior review estimated ~231 MB/s per extra full-frame copy at 25 FPS. | Coordinate transform cost negligible relative to image copies. | B strongly preferred. |
| Latency | Can remain low with shared request/bounded buffers, but extra streams/copies add risk. | Very low geometry-adapter latency; no extra image pipeline required. | B preferred. |
| Synchronization | Requires frame/timestamp/config identity across metric and AI products; multi-stream pairing must remain exact. | Requires same provenance contract for `A` and source frame; no stream pairing if no second metric image product exists. | B has smaller sync surface. |
| Implementation complexity | Camera configuration/representation + transform + bbox projection + potential stream/buffer management. | Geometry metadata + `A/A^-1` + AI→CAL adapter + existing metric path. | B smaller. |
| Failure modes | Buffer/copy pressure, stream mismatch, frame pairing, retaining unnecessary full-resolution images. | Wrong transform, wrong offsets/orientation, crop/FOV loss, clipping, semantic bbox mismatch. | Different risk classes; B is simpler but transform correctness is critical. |
| Maintainability | Strong if one canonical camera-geometry contract drives all streams; more components to maintain. | Strong if transform provenance is centralized and versioned by geometry/config generation. | B simpler today; A stronger for future pixel consumers. |
| HOROS extensibility | Can directly support future calibrated ROI/pixels, stereo/image patches/local mapping. | Excellent for current range/LOS/object geometry; insufficient if future HOROS requires pixel content absent from AI path. | B first, A as extension. |

## C. SHARED_PREREQUISITES

Both A and B share the same hard prerequisite and neither is implementation-ready until it is satisfied:

**VERIFIED requirement / current NOT_VERIFIED evidence:**
`sensor mode -> ScalerCrop -> ISP/output geometry -> 640x640 AI coordinates`

Must establish:
- actual sensor/readout mode;
- active crop/ScalerCrop;
- output/ISP scaling;
- resize/stretch/letterbox/padding/orientation;
- Hailo preprocessing geometry;
- geometry/config generation identity.

Both also require:
- `frame_id`;
- `SensorTimestamp`;
- geometry/config generation;
- CurrentTarget generation;
- measurement age;
- explicit class provenance in range path;
- >25 FPS validation.

**Conclusion:** shared forward-transform prerequisite = **VERIFIED BY REVIEW**.

## D. UNIQUE_RISKS_A

1. **SUPPORTED_BY_EXISTING_REVIEW:** unnecessary full-resolution retention/copies may consume large Pi 5 memory bandwidth and reduce FPS.
2. Stream pairing mismatch if metric and AI products are not from the same capture request/frame identity.
3. Multi-stream ISP geometry may differ in crop/aspect behaviour; dimensions alone do not prove correspondence.
4. Additional buffer lifetime can create camera/request backlog.
5. Architecture drift risk if a logical metric representation accidentally grows into a second tracker/target authority; explicitly forbidden.
6. More code/config surface for camera stream management and performance instrumentation.

## E. UNIQUE_RISKS_B

1. **SUPPORTED_BY_EXISTING_REVIEW:** a numerically perfect inverse of the wrong `A` produces systematic metric error.
2. Crop/FOV loss is irreversible; geometry outside AI-observable region cannot be invented.
3. Bbox intersecting crop/padding/boundary can invalidate class-size physical-extent assumptions.
4. Incorrect offset/scale/orientation/letterbox metadata directly biases LOS/range.
5. Detector bbox semantics remain independent of coordinate correctness: a correctly mapped bbox can still be a poor physical-size measurement.
6. Future pixel/ROI consumers cannot be satisfied from geometry alone if the relevant pixels were never preserved/exposed.

## F. CURRENT_INFORMATION_REQUIREMENTS

### Current class-size range
**SUPPORTED_BY_EXISTING_REVIEW:** requires calibrated object geometry (bbox width/height/centre), original K/calibration provenance, physical-size prior/class provenance and frame/time identity. It does **not** intrinsically require full calibrated image pixels.

### LOS
**SUPPORTED_BY_EXISTING_REVIEW:** requires calibrated point/centre coordinates + K, not a reconstructed image.

### Current HOROS LOS_RANGE ingress
**SUPPORTED_BY_EXISTING_REVIEW:** consumes spatial measurement/LOS/range with uncertainty/provenance/timestamp; no current evidence establishes a requirement for full calibrated HQ pixels.

### Therefore
For present requirements, **calibrated object geometry only is sufficient**. Full calibrated pixels/ROI are **NOT_VERIFIED as currently required**.

## G. FUTURE_EXTENSION_ANALYSIS

Future HOROS or adjacent metric consumers may eventually require:
- calibrated image patches/ROI;
- keypoints derived from higher-resolution pixels;
- segmentation/landmarks;
- stereo correspondence;
- local environment mapping;
- texture-based metric processing.

These future requirements are **INFERRED / NOT_VERIFIED**, not current requirements.

Candidate convergence statement:
> B may be the minimal first implementation, while A remains the extensible architecture if future metric consumers require real calibrated pixels/ROI rather than geometry only.

Classification: **SUPPORTED_BY_EXISTING_REVIEW**.

Reason: Task B review explicitly prefers geometry-only as minimum current boundary and reserves a calibration-preserving metric stream for cases where AI discards required FOV/physical boundaries or later algorithms require calibrated pixels/ROI. Task A independently states that current class-size range/LOS can operate from mapped calibration geometry and full pixels are required only by consumers that actually use them.

## H. VALIDATION_SEQUENCE

Preserve Task A six-domain decomposition. No global range PASS/FAIL.

1. **CAMERA GEOMETRY** — independently establish sensor mode/crop/FOV/output mapping using rigid measured geometry.
2. **COORDINATE TRANSFORM** — known calibration-space points → forward `A` → inverse `A^-1` → recovery error, including crop/letterbox/boundary cases.
3. **CLASS PRIOR** — fixed image geometry with deliberately varied class profiles; trace whether range consumes instantaneous detector class, stabilized CurrentTarget class or other provenance.
4. **SILHOUETTE VARIABILITY** — quantify E88 bbox/class variation separately; do not use E88 free-propeller silhouette as precision metric truth.
5. **FRAME IDENTITY** — verify detector result from frame N uses geometry/transform/config generation from frame N and correct CurrentTarget generation.
6. **PERFORMANCE** — complete authoritative HQ path must remain >25 FPS; measure minimum FPS, p95/p99 latency, stale age and buffer/copy cost.

Physical constraints retained:
- F450 at ~2.58 m did not fully fit narrow HQ view;
- F450 moved to exact 4.000 m; full visibility there remains NOT_VERIFIED;
- future F450 metric test must use measured rigid landmark span, not nominal frame/propeller dimensions;
- E88 class variation FPV/Orlan-10/Talay is not evidence against either geometry architecture;
- printed E88 and miniature Shahed tests remain invalid as direct calibration-failure evidence for the reasons already reviewed;
- snapshot 404 remains an observability limitation only.

## I. IMPLEMENTATION_RECOMMENDATION

**HYBRID_MINIMAL_FIRST**

Interpretation:
- Implement **Task B's minimal AI→CAL geometry adapter first** after the live forward transform is VERIFIED.
- Structure its camera-geometry/provenance contract so it is already compatible with Task A's broader logical architecture.
- Do not add a persistent calibration-preserving image stream until a real consumer requires calibrated pixels/ROI or B fails its visibility/information gate.

This is not simultaneous implementation of both designs. It is B-first inside an A-compatible contract.

## J. REASON_FOR_DECISION

1. **Current information needs are geometry-only.** Existing reviews do not establish a need for calibrated pixels for class-size range, LOS or current HOROS ingress.
2. **Metric correctness is not weaker under B** when the actual transform is known and required object extent remains visible; Task B mathematically proves equivalence to using transformed K / calibrated coordinates.
3. **B has the smallest implementation surface.** It avoids camera multi-stream management and full-resolution buffer/copy costs.
4. **B has the lowest Pi 5 performance risk** and best chance of preserving >25 FPS.
5. **A remains fully compatible as a later extension** and should define the provenance/data-contract philosophy, not force full metric-image retention today.
6. Both share the same decisive prerequisite, so choosing B does not bypass the camera-geometry proof.

## K. FALLBACK_PATH

Promote to the Task A calibrated metric stream/ROI architecture when **any** of the following is directly evidenced:

1. AI crop/FOV removes an object boundary/physical extent required by range or LOS and it cannot be recovered from AI geometry.
2. The required metric target/landmark is outside the AI-visible region but available in calibration-consistent camera output.
3. A future HOROS/metric algorithm demonstrably requires calibrated pixels, ROI texture, high-resolution keypoints, segmentation, stereo correspondence or local mapping input.
4. The AI→CAL transform is not stable/deterministic enough across the active sensor/config path to provide auditable geometry, while a calibration-consistent stream can provide a stable authority.
5. Validation shows B's metric quality fails despite a VERIFIED transform because information removed before AI representation is required for the metric measurement.

Do **not** fall back to A merely because detector class is unstable, E88 silhouette varies, or class priors are wrong; those are separate validation domains.

## L. CODEX_HANDOFF_BOUNDARY

No Codex prompt is authorized here. The minimal future implementation boundary, after explicit human approval and VERIFIED camera geometry, is:

1. **Camera geometry provenance**
   - capture/expose exact sensor mode, ScalerCrop/output transform/preprocess identity;
   - geometry/config generation ID.
2. **Frame provenance envelope**
   - frame_id;
   - SensorTimestamp;
   - CurrentTarget generation;
   - measurement age/source stage.
3. **Pure geometry transform component**
   - deterministic `A` and `A^-1`;
   - point/bbox/centre/width/height mapping;
   - clipping/observable-domain validity checks.
4. **AI→CAL metric adapter**
   - receive authoritative existing AI-space bbox/state after protected tracking chain;
   - project to 2028x1520 calibration coordinates;
   - pass original calibration identity/K and class provenance into existing range/LOS path.
5. **HOROS ingress provenance**
   - preserve source timestamp, measurement age, range/LOS provenance.
6. **Validation/instrumentation only as required**
   - geometry round-trip;
   - class-prior provenance trace;
   - frame-identity assertions;
   - >25 FPS/min-FPS/latency/stale-age measurement.

Explicit non-goals:
- no second Picamera2 capture loop;
- no second tracker/CA/CurrentTarget;
- no calibration change;
- no Hailo model/input change;
- no full 2028x1520 image reconstruction;
- no Task A full metric image stream unless fallback gate is met.

## M. FINAL_VERDICT

**HYBRID_PREFERRED**

Meaning:
- **B is preferred for the first minimal implementation boundary.**
- **A is preferred as the extensibility envelope/fallback for future calibrated-pixel/ROI requirements.**
- Neither is production-ready until the shared live forward transform is VERIFIED.

### Final classifications
- Protected tracking authority remains unchanged: **VERIFIED**.
- Current class-size range / LOS / current HOROS require calibrated geometry rather than full pixels: **SUPPORTED_BY_EXISTING_REVIEW**.
- B is mathematically metrically equivalent to calibrated-coordinate processing under a correct invertible transform: **SUPPORTED_BY_EXISTING_REVIEW**.
- B cannot recover cropped/clipped information: **VERIFIED BY REVIEW**.
- A and B are not mutually exclusive: **SUPPORTED_BY_EXISTING_REVIEW**.
- B-first, A-compatible architecture: **RECOMMENDATION**.
- Exact live transform: **NOT_VERIFIED**.
- Production readiness before that transform is proven: **NOT_VERIFIED**.

STOP — DO NOT IMPLEMENT.
