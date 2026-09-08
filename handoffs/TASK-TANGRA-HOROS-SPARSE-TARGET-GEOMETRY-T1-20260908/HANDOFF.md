# Reviewer Handoff — TASK 1 Sparse Target Geometry

Status: REVIEW READY / SHADOW CANDIDATE ONLY

## Architecture boundary
Input is one existing HQ frame plus authoritative bbox/class/confidence metadata. The extractor takes a NumPy ROI view, allocates only ROI-sized grayscale/mask temporaries, performs deterministic threshold/component/contour/PCA geometry, and returns a frozen typed observation. No second detector, frame capture, full-frame processing loop, tracker, range calculation, calibrated transform, HOROS authoritative write, guidance, dashboard or command path exists in this package.

## Point model
Fixed first-pass topology: CENTER, LEFT_SILHOUETTE, RIGHT_SILHOUETTE, NOSE, TAIL. LEFT/RIGHT are explicitly image-space silhouette extrema. Nose/tail use a constrained top-down engineering assumption: the narrower axial end is the nose. If end-width evidence does not exceed the configured ratio, nose/tail are returned invalid with `ambiguous_axial_polarity`; semantics are not fabricated. Hard point count = 5.

## Processing mechanism
ROI grayscale -> Otsu binary/inverse candidates -> connected-component scoring by centrality/area/border contact -> internal contour -> centroid/PCA axis -> image-space lateral extrema -> axial endpoint-width polarity test -> confidence/validity. Full contour is temporary and is not persisted in the observation.

## Integration boundary for later Codex
Codex must first inspect the current local implementation authority and verify the exact same-frame HQ+bbox contract and safe passive insertion point. Candidate source must remain shadow-only. Do not integrate if doing so mutates detector/NanoTracker/CA/CurrentTarget/range/HOROS authority. No AI-to-CAL transform or range work belongs to this task.

## Known limitations
- All validation fixtures are SYNTHETIC; no physical target validation claim.
- Nose/tail polarity is only justified for silhouettes where the narrower-end assumption is evidenced; symmetric targets degrade rather than guess.
- Otsu/component segmentation assumes usable foreground/background separation inside the detector ROI; cluttered/low-contrast real imagery is NOT VERIFIED.
- Exact compatibility with current local `main.py` and target metadata types is NOT VERIFIED until local source inspection.
- Host microbenchmark is not Pi5/end-to-end performance evidence.
