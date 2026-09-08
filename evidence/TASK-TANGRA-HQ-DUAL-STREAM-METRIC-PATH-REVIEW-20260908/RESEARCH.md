# RESEARCH — TANGRA HQ DUAL-STREAM / CALIBRATION-PRESERVING METRIC PATH

TASK_ID: TASK-TANGRA-HQ-DUAL-STREAM-METRIC-PATH-REVIEW-20260908
STATUS: REVIEW
MODE: RESEARCH + FORENSIC DESIGN REVIEW ONLY

## A. CURRENT_PIPELINE

### VERIFIED
From prior WORKSHOP forensic evidence:
- HQ application requests Picamera2 `main` BGR888 at 640x640.
- Hailo input contract is 640x640.
- Application Hailo preprocessing includes `cv2.resize(frame, (640,640))`; with a 640x640 source this explicit operation is geometrically identity.
- Current monocular range intrinsics are derived from the 2028x1520 calibration by direct scale factors 640/2028 and 640/1520.
- NanoTracker and CA Kalman remain protected authoritative temporal tracking components; CurrentTargetManager remains target authority.
- Display bbox and range bbox were traced as the same post-CA geometry in the prior bounded forensic.

### NOT_VERIFIED
- Actual IMX477 sensor/readout mode chosen by Picamera2/libcamera for the current 640x640 request.
- Live ScalerCrop/analogue crop/binning/ISP geometry.
- Whether the current 640x640 stream preserves the calibrated 2028x1520 optical field.
- Whether the calibrated 2028x1520 geometry is available as an application stream before the current 640x640 output. The sensor has one optical source, but current application configuration does not expose a calibration-consistent second stream.

### INFERRED
The current application has coupled camera output dimensions to the detector canonical dimensions. This is a configuration coupling, not proof of a geometry error. Prior physical evidence makes a geometry/effective-focal mismatch plausible, but the direct camera metadata probe remains required.

## B. PROPOSED_DUAL_STREAM_TOPOLOGY

### RECOMMENDATION
Use **one camera acquisition authority and two logical geometry products**, not two independent capture loops and not two target states:

IMX477 + 50 mm / one Picamera2 camera configuration
→ one libcamera request with one sensor timestamp / frame identity
→ calibration-consistent metric geometry authority
   ├─ METRIC representation: calibration-space coordinates/K + optional ROI/pixels only when needed
   └─ AI representation: explicit deterministic transform T_cal_to_ai → 640x640
      → Hailo detections
      → NanoTracker
      → CA Kalman
      → CurrentTargetManager
      → inverse/associated transform T_ai_to_cal
      → metric bbox/centre/LOS/range evidence
      → HOROS LOS_RANGE ingress

This preserves a **single authoritative detection/tracking chain**. The metric path is a coordinate/measurement projection of the authoritative target state, not a tracker.

### Two implementation candidates for later benchmark

**Candidate A — one calibration-consistent main stream + application deterministic 640 transform.**
- Main stream is calibration-consistent geometry.
- Application generates 640x640 AI frame using a fully specified resize/crop/letterbox transform.
- Benefit: transform is explicit and easily invertible/auditable.
- Risk: CPU/memory-bandwidth cost of converting/resizing every frame for NanoTracker, even when Hailo is decimated.

**Candidate B — one Picamera2 configuration with main metric stream + secondary/lores AI stream from the same sensor request.**
- Picamera2 officially supports main/lores/raw streams in one configuration.
- libcamera models multiple streams from one camera/image source and a Request can carry buffers for multiple streams.
- Benefit: ISP can potentially generate lower-resolution AI stream without a Python full-frame resize/copy.
- Risk: exact crop/aspect/scaling relationship between main and lores must be directly proven. Do not assume 640x640 secondary output is a simple full-field anisotropic resize.

**Design preference:** Candidate B is computationally attractive only after direct geometry metadata/test proves a stable, deterministic mapping. Candidate A is the safer reference implementation for geometry correctness because the transform can be made explicit. No production choice is made by this review.

## C. REQUIRED_DATA_CONTRACTS

### 1. `HQFrameIdentity`
Required per camera request:
- `frame_id`: monotonic application ID.
- `sensor_timestamp_ns`: authoritative capture timestamp from libcamera/Picamera2 metadata.
- `request_sequence` if exposed, diagnostic only.
- `metric_stream_shape` and format/stride.
- `ai_stream_shape` and format/stride.
- `camera_geometry_id`: immutable identifier for active sensor mode/crop/calibration mapping.

### 2. `ImageTransform`
Must describe the exact map between calibration/metric coordinates and AI coordinates:
- source width/height.
- destination width/height.
- crop rectangle `(x0,y0,w,h)` if any.
- scale `sx, sy` or uniform `s`.
- padding `(px,py)` if letterboxed.
- orientation/rotation/flip.
- inverse transform or enough parameters to compute it deterministically.

For direct anisotropic resize:
`x_ai=sx*x_cal`, `y_ai=sy*y_cal`, with `sx=640/W_cal`, `sy=640/H_cal`.

For crop+resize:
`x_ai=sx*(x_cal-x0)`, `y_ai=sy*(y_cal-y0)`.

For letterbox:
`x_ai=s*x_cal+px`, `y_ai=s*y_cal+py` after any explicit crop.

No geometry may be inferred from output dimensions alone.

### 3. `TargetObservation`
AI-path observation must carry:
- frame_id and sensor timestamp of the image used by detector/tracker.
- target generation/identity from CurrentTarget authority.
- bbox in AI coordinates.
- bbox source stage: detector / tracker / CA.
- class and confidence with source age.
- mapped bbox/centre in calibration coordinates derived only through the recorded transform.
- observation age at consumption.

### 4. `MetricTargetEvidence`
Minimum payload for current class-size range/LOS does **not** require a full HQ image copy:
- calibration-space bbox corners or centre+width+height.
- calibrated K (`fx,fy,cx,cy`) identified by calibration ID, not modified.
- physical class-size evidence and provenance used by existing estimator.
- frame_id/timestamp.
- range + uncertainty/provenance when available.
- LOS/bearing computed in calibration coordinates.

Full-resolution pixels are required only for a metric operation that actually consumes texture/landmarks/segmentation, for debugging/validation, or for a target ROI extraction task. Do not retain full frames merely because a logical metric path exists.

## D. FRAME/TIMESTAMP_IDENTITY_MODEL

### VERIFIED external architecture principle
libcamera `Request` is the per-capture unit and can associate multiple stream buffers; Picamera2 can obtain image(s) and metadata from a captured request. `SensorTimestamp` is used by Picamera2 components as the precise video timestamp source.

### RECOMMENDATION
- Assign one `frame_id` at receipt of each completed camera request.
- All stream products from that request inherit the same `frame_id` and `sensor_timestamp_ns`.
- AI preprocessing records its source frame ID.
- Detector result records `detector_source_frame_id` and submit/complete timestamps.
- NanoTracker/CA updates record current frame ID and must never silently relabel a delayed detection as current.
- CurrentTarget generation ID must accompany observations so a late result from a previous target cannot mutate a newer target generation.
- Range/HOROS payload must contain measurement timestamp and measurement age; HOROS prediction time is not the same as source-measurement time.

### Async inference caveat
If Hailo later runs asynchronously or at reduced cadence, a result from frame F may return when tracking is at F+k. A production policy for delayed measurement association/rejection is **NOT_VERIFIED** and must be benchmarked. The minimum safe initial boundary is to avoid allowing stale detector results to overwrite newer authoritative tracker/CurrentTarget state. This review does not redesign NanoTracker or CA for out-of-sequence updates.

## E. MEMORY/COPY/PERFORMANCE_ANALYSIS

### Approximate uncompressed BGR888 payload sizes
- 2028x1520x3 = 9,247,680 bytes ≈ 8.82 MiB per full frame.
- At 25 FPS, one full application-level copy moves ≈231 MB/s of payload; at 30 FPS ≈277 MB/s, before stride/alignment/cache effects.
- 640x640x3 = 1,228,800 bytes ≈1.17 MiB per AI frame; at 25 FPS ≈30.7 MB/s.

These numbers are **INFERRED arithmetic**, not measured Pi5 bandwidth or runtime cost. Actual ISP/raw formats, strides, buffer counts, DMA, cache behaviour and Hailo transfer cost remain NOT_VERIFIED.

### Implications
- RAM capacity itself is unlikely to be the first constraint on a 16 GB Pi 5; repeated full-resolution copies and cache/memory bandwidth are the higher-risk costs.
- Multiple Picamera2 buffers at 2028x1520 can consume tens of MiB but remain modest relative to RAM; latency/backlog risk matters more than capacity.
- A secondary ISP-generated 640 stream may reduce CPU resize cost, but only if it does not introduce an unknown crop/FOV transform.
- `capture_array()` / NumPy conversion semantics and Hailo input transfer path must be profiled; do not claim zero-copy from documentation alone.

### Zero-copy / bounded-buffer recommendation
- Prefer camera request/buffer lifetime ownership with bounded buffers and prompt release.
- Avoid persistent duplicate full-resolution NumPy copies.
- Keep full-resolution data only as long as the metric consumer needs it.
- Use depth-1/latest-frame semantics for optional expensive asynchronous consumers; do not queue stale HQ frames.
- Zero-copy from camera buffer through Hailo is **NOT_VERIFIED** and is not required for the architectural correctness of the design.

### FPS gate
Any later implementation must demonstrate >25 FPS under the complete authoritative HQ tracking path. Geometry correctness alone is insufficient if 2028x1520 acquisition/transforming causes the system to fall to <=25 FPS. Prior multi-rate research additionally recommends preserving measured frame-time reserve, not merely passing 25 FPS average.

## F. RANGE/HOROS_INTEGRATION

### RECOMMENDATION
Keep detector/tracker/CA in their existing authoritative AI coordinate system initially. Add a **pure geometry projection boundary** after authoritative bbox state is available:

`authoritative AI bbox + frame transform + calibration K`
→ calibration-space bbox/centre
→ class-size range and LOS computation
→ existing range evidence
→ HOROS LOS_RANGE ingress.

This avoids creating a second tracker and avoids requiring the detector to operate in calibration resolution.

### Range cadence
The class-size formula is cheap. If authoritative tracker/CA bbox exists every camera frame and transform metadata is available, range can in principle update every valid authoritative tracking frame. Whether class-size range should use detector bbox, tracker bbox, CA bbox, or only specific freshness states is existing algorithm policy and must be traced/validated rather than changed by this architecture review.

### HOROS
- HOROS prediction remains independent/high-rate as already designed.
- LOS_RANGE measurement must carry original source timestamp, range uncertainty, and calibration/transform provenance.
- HOROS must not interpret a projected current track bbox as a fresh detector measurement if the class/size evidence is stale.
- No HOROS estimator redesign is required by the dual-geometry architecture.

## G. FAILURE_MODES

1. **Metric/AI frame mismatch** — detection from F mapped using geometry metadata from F+1.
2. **Stale detector overwrite** — delayed Hailo result changes newer track/CurrentTarget state.
3. **Transform drift/config change** — sensor mode/ScalerCrop changes but transform ID remains stale.
4. **Aspect-ratio ambiguity** — 2028x1520 → 640x640 treated as simple resize when actual ISP performs crop/padding.
5. **Competing target authority** — metric branch creates its own tracker/current-target state. Explicitly forbidden.
6. **Full-frame copy explosion** — every consumer deep-copies 8.82 MiB frame, causing bandwidth/FPS regression.
7. **Buffer backlog** — metric/Hailo consumer retains camera requests and stalls/recycles buffers late.
8. **Inference cadence mismatch** — tracker is current but detector class/confidence/range evidence age is hidden.
9. **ROI association error** — high-resolution target ROI is extracted from the wrong frame/track.
10. **Calibration misuse** — K for 2028x1520 applied to coordinates not actually mapped to that calibration field.
11. **Silent crop/FOV change** — libcamera stream configuration changes after camera stack/software update.
12. **Validation blind spot** — average FPS passes while minimum FPS, p95 latency, buffer age or range freshness fails.

## H. REQUIRED_CODE_TOUCHPOINTS

### INFERRED minimum future boundaries; exact files are NOT_VERIFIED until target runtime repository is re-opened
1. **CameraStream / Picamera2 configuration boundary** — expose calibrated stream and/or secondary AI stream from one configuration; capture metadata/frame identity.
2. **AI preprocess boundary** — centralize deterministic `metric/calibration → 640x640` transform and provenance.
3. **Detection/tracker observation envelope** — carry source frame ID/timestamp and transform ID without changing NanoTracker/CA algorithms.
4. **Range geometry adapter** — inverse-map authoritative bbox into calibration coordinates before class-size/LOS use.
5. **HOROS ingress envelope** — preserve measurement timestamp, uncertainty and provenance.
6. **Instrumentation** — frame age, queue depth, copy/resize time, detector submit/complete and minimum FPS.

Do **not** create a separate metric tracker, second CurrentTargetManager, second CA filter, or second Picamera2 capture thread as the default design.

## I. MINIMUM_IMPLEMENTATION_PLAN

This is a future plan only; no implementation is authorized.

1. Complete the direct Picamera2 geometry probe for current 640x640 and candidate calibration-consistent configuration.
2. Choose a **reference transform policy** for 2028x1520 → 640x640 that preserves the detector's expected preprocessing semantics; record crop/resize/padding explicitly.
3. Prove a single Picamera2 configuration can deliver the required calibration-consistent stream and AI representation without ambiguous geometry. Compare Candidate A vs Candidate B.
4. Introduce frame identity + transform provenance contract before changing range geometry.
5. Add pure inverse-coordinate projection from authoritative AI bbox to calibration space.
6. Route existing range/LOS/HOROS evidence through the projected geometry without changing tracker/CA/CurrentTarget authority.
7. Benchmark with Hailo N=1 first.
8. Only after geometry/quality/FPS PASS, test detector cadence N>1 according to the prior multi-rate campaign.

Smallest conceptual boundary: **camera geometry + transform provenance + bbox projection adapter**. Avoid broader pipeline redesign.

## J. VALIDATION_PLAN

### Geometry correctness
- Same physical target, known distance, same optical focus/calibration.
- Record sensor mode, ScalerCrop, stream configs and exact transform.
- Verify forward/inverse point and bbox mappings numerically.
- Compare calibration-space projected bbox against directly observed metric-stream object edges/known markers.
- Known-distance range tests across image centre and edges; multiple target sizes/orientations.

### Identity/time correctness
- Stamp every frame and detector/tracker/range/HOROS observation.
- Assert that a result can only use the transform associated with its source frame/config generation.
- Inject delayed detector results in replay and verify they cannot silently overwrite newer target generation.

### Performance
- N=1 baseline first.
- Measure camera FPS, minimum FPS, p95/p99 frame time, resize/ISP time, Hailo latency, CPU, RAM, buffer count/age, dropped frames, memory-copy proxy, stale-frame age.
- Reject if any operational segment reaches <=25 FPS.
- Compare Candidate A application resize vs Candidate B ISP secondary stream if both are geometrically valid.

### Quality regression
- NanoTracker continuity.
- CA prediction/innovation error.
- CurrentTarget resets/reacquisition.
- detector misses/confidence.
- range error/freshness.
- HOROS measurement age/spatial error.

## K. RISKS

### HIGH
- Assuming a 640x640 secondary stream has a known full-FOV mapping without proving ScalerCrop/aspect behaviour.
- Additional full-resolution copies causing memory-bandwidth/FPS loss.
- Async/decimated detector results applied to wrong temporal state.

### MEDIUM
- Detector accuracy change when preprocessing from 4:3 calibrated geometry to square AI tensor differs from today's implicit camera/ISP geometry.
- Higher-resolution ISP workload reducing headroom before Hailo cadence savings are realized.
- Transform metadata/config-generation bugs.

### LOW-MEDIUM
- RAM footprint itself, provided buffers are bounded and full frames are not retained unnecessarily.

## L. VERDICT

**VIABLE_WITH_CONDITIONS**.

### VERIFIED
- Picamera2 can configure multiple logical streams (`main`, `lores`, `raw`) from one camera configuration.
- libcamera represents multiple streams from one image source as one camera and associates stream buffers with capture Requests.
- TANGRA currently couples a 640x640 camera output request with a 640x640 detector input contract in the traced application path.
- Existing authoritative tracker/CA/CurrentTarget components do not need replacement to support separate metric and AI coordinate spaces.

### INFERRED
- A dual-logical-path architecture is cleaner and safer than treating detector tensor geometry as metric camera geometry.
- Current class-size range/LOS can operate from mapped calibration-space bbox/centre plus K and provenance; it does not intrinsically require retaining full HQ pixels every frame.
- ISP-generated secondary 640 stream may be more efficient than application resize, but performance and exact geometry must be measured.

### NOT_VERIFIED
- Current and candidate sensor mode/ScalerCrop/FOV mappings.
- Whether a 2028x1520 main + 640x640 lores combination preserves the exact required calibration field and detector preprocessing semantics.
- Zero-copy Hailo integration.
- Pi5 performance at >25 FPS with calibration-consistent HQ acquisition.
- Safe lower Hailo cadence in the dual-geometry configuration.

### RECOMMENDATION
Proceed only to a **read-only dual-stream/geometry probe + benchmark design**, not implementation. If the probe proves a stable calibration-consistent acquisition field and deterministic AI transform, the preferred architecture is one camera request, one authoritative tracking chain, explicit transform provenance, and metric projection of the authoritative target state. No physical calibration, NanoTracker, CA Kalman, CurrentTargetManager, detector input size or HOROS estimator change is justified by this review.

## SOURCES / PROVENANCE
- WORKSHOP prior camera-geometry forensic: `evidence/TASK-TANGRA-HQ-640-CAPTURE-GEOMETRY-FORENSIC-20260907/SCOUT.md`.
- WORKSHOP prior multi-rate research: `evidence/TASK-TANGRA-MULTIRATE-PIPELINE-PERFORMANCE-HEADROOM-RESEARCH-20260907/RESEARCH.md` and independent review.
- Raspberry Pi Picamera2 Manual (current 2026 edition): configuration supports main/lores/raw streams; image size/alignment can affect copies/efficiency; captured requests provide image data with matching metadata.
- libcamera public API: a Camera has one image source and may produce multiple streams; Request associates buffers/metadata for capture processing.
- Picamera2 source/examples use `SensorTimestamp` as the precise video timestamp source and demonstrate multiple streams in a single configuration.
