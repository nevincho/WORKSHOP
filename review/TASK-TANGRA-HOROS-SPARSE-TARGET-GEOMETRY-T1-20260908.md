# TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908 — Independent Review

REVIEW_RESULT: PASS_WITH_CONDITIONS
COMMIT_REVIEWED: 6e3ee9b288d0c7129baba979062736d304886014

## Scope reviewed
Standalone passive ROI-only sparse geometry package in WORKSHOP handoff. No Task 2, no production integration, no architecture expansion.

## Findings
- Extractor reads only the supplied bbox ROI from the provided frame, aside from frame shape/bounds. No full-frame processing loop, detector, tracker, range logic, calibrated transform, HOROS authority write, guidance/dashboard/command path exists.
- Input frame and frozen metadata are not mutated by implementation; test includes frame hash + metadata equality.
- Fixed sparse point count is 5 when segmentation succeeds: CENTER, LEFT_SILHOUETTE, RIGHT_SILHOUETTE, NOSE, TAIL. Invalid extraction returns zero points.
- CENTER is contour centroid. LEFT/RIGHT are explicitly image-space x-extrema near centroid y; these semantics are deterministic and defensible as screen-space silhouette extrema, but are not target-relative wing-side landmarks.
- Nose/tail uses PCA major-axis endpoints and a narrower-end width-ratio heuristic. Symmetric/insufficiently anisotropic silhouettes degrade and mark axial semantics invalid rather than forcing validity.
- Architecture is lightweight and suitable for later same-frame SHADOW insertion without redesign, subject to local source compatibility verification before integration.
- No historical Geometry Observer state machine, temporal loop, tracker, metric observer, or duplicated runtime authority has been reintroduced.

## Concrete issue 1 — weak-contrast confidence is not fail-safe
Segmentation confidence is derived from connected-component geometry (centrality, component area, border contact) and detector confidence. It does not measure foreground/background photometric separation or Otsu separability. Therefore a very low-contrast but still threshold-separable silhouette can receive essentially the same segmentation confidence as a high-contrast silhouette. The existing 9-case suite checks blank ROI but not weak/near-uniform contrast. This does not satisfy the requested confidence-fails-safely criterion for weak silhouettes.

Smallest required correction: add a bounded photometric/separation quality gate or confidence factor (for example foreground/background intensity separation or an equivalent threshold-separability statistic) and add one deterministic weak-contrast/near-uniform silhouette test that must degrade or invalidate.

## Concrete issue 2 — invalid axial semantics retain coordinates
When polarity is selected geometrically but `semantic_conf < 0.25`, NOSE/TAIL are emitted with `valid=False` and reason `ambiguous_axial_polarity`, but their x/y fields can still contain the selected axial endpoint coordinates. This is internally marked invalid, but is weaker fail-closed behavior than clearing semantic coordinates and creates avoidable downstream misuse risk.

Smallest required correction: when `nt_valid` is false, emit NOSE/TAIL coordinates as `None` (or otherwise ensure the contract explicitly guarantees invalid semantic coordinates are unusable). Add an assertion covering this case.

## Tests
The repository test file contains 9 unittest cases matching the reported categories: near top-down; 23-degree in-plane rotation proxy; point ordering/repeatability; detection-confidence response; symmetric nose/tail ambiguity; bbox boundary clipping; repeated unchanged input; upstream immutability; blank ROI invalidation. Assertions are meaningful for those exact synthetic claims. The mild-oblique case is correctly described as an in-plane synthetic proxy, not perspective validation.

## Benchmark
Benchmark performs 20 warmups then 300 extractor calls at each of three ROI sizes (900 total) and reports extractor-internal `perf_counter_ns` elapsed time. Methodology is adequate to support the stated x86_64 synthetic micro-latency snapshot only. It does not support Pi5, end-to-end FPS, real-image, or production scheduling claims, and the evidence explicitly avoids those claims.

## Dependencies
Implementation imports only Python standard library, NumPy and OpenCV. No production object, runtime singleton, detector/tracker/HOROS object, network, file, model, or hardware dependency exists in the package.

## Top-down suitability
For the intended envelope — near top-down, mild oblique top-down, mostly complete and separable silhouette — Otsu + connected-component selection + contour centroid/PCA is technically plausible and appropriately lightweight. Physical silhouette quality, true 3D obliquity, clutter/low-contrast robustness and Pi5 performance remain NOT VERIFIED and are correctly classified as such.

## Decision
PASS_WITH_CONDITIONS. The package is architecturally bounded and technically coherent, but Task 1 should not be frozen COMPLETE until the two bounded fail-closed corrections above are made and re-tested. No redesign is required.

TASK1_COMPLETE: NO
BLOCKER: weak-silhouette confidence does not currently fail safely; invalid axial semantics can retain coordinates despite `valid=False`.
