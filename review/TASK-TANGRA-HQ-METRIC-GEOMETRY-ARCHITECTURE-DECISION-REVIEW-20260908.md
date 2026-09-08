# REVIEW — TANGRA HQ METRIC GEOMETRY ARCHITECTURE DECISION

TASK_ID: TASK-TANGRA-HQ-METRIC-GEOMETRY-ARCHITECTURE-DECISION-REVIEW-20260908
VERDICT: PASS
STATUS: COMPLETE

## Independent review conclusion

The comparative decision correctly uses the already COMPLETE/Reviewer-PASS Task A and Task B results without reopening settled findings. No contradiction exists between A and B: they share one protected HQ→Hailo→NanoTracker→CA→CurrentTarget→range→HOROS authority and differ primarily in how much calibration-consistent image information is retained/exposed.

The chosen recommendation **HYBRID_MINIMAL_FIRST** is supported by the existing reviews and does not mean implementing two parallel architectures. It means:
- first implementation boundary should be Task B's geometry-only AI→calibration projection after the live transform is proven;
- the camera-geometry/provenance contract should remain compatible with Task A so calibrated pixels/ROI can be exposed later if a real consumer requires them.

## Comparative checks

1. **Metric correctness:** PASS. Task B is not less correct for current geometry-only consumers when `A` is correct; Task B review explicitly proved `K_ai=A K_cal` and `K_ai^-1 p_ai = K_cal^-1 p_cal`. Task A remains more information-preserving but does not improve current metric correctness merely by retaining pixels.

2. **Information preservation:** PASS. The decision correctly states that B cannot reconstruct crop/FOV/clipped information. Task A is the fallback when that missing information is required.

3. **Performance:** PASS. The decision correctly favours B for initial Pi 5 risk because it avoids unnecessary full-resolution image copies/buffers. It does not claim a numeric FPS gain and preserves the >25 FPS gate.

4. **Implementation surface:** PASS. B's minimum boundary is smaller: geometry provenance + transform + bbox adapter + existing range/LOS/HOROS. A adds camera-stream/buffer representation complexity if pixels are retained.

5. **Synchronization:** PASS. Both require frame_id, SensorTimestamp, config/geometry generation, CurrentTarget generation and measurement age. B removes stream-pairing risk when no separate metric image product exists, but stale-result provenance remains equally mandatory.

6. **Physical evidence use:** PASS. E88 class instability and movable propellers are not used as evidence against either architecture; F450, printed E88, Shahed miniature and snapshot-404 evidence are kept in their proper validation domains.

7. **Validation methodology:** PASS. The six independent domains from Task A are preserved and not collapsed into a global range result.

8. **Shared gate:** PASS. Both A and B remain blocked from implementation decision execution until the actual `sensor mode -> ScalerCrop -> ISP/output -> AI 640x640` transform is directly VERIFIED.

## Architecture convergence verdict

Candidate conclusion:
> B may be the minimal first implementation, while A remains the extensible architecture if future metric consumers require real calibrated pixels/ROI rather than geometry only.

Classification: **SUPPORTED_BY_EXISTING_REVIEW**.

This is directly aligned with Task B's prior final review and Task A's prior conclusion that current class-size range/LOS can operate on mapped calibrated geometry without retaining full HQ pixels.

## Decision

IMPLEMENTATION_RECOMMENDATION: **HYBRID_MINIMAL_FIRST**
FINAL_VERDICT: **HYBRID_PREFERRED**

Interpretation:
- B-first for current metric geometry needs;
- A-compatible provenance/data-contract design;
- A metric-image/ROI extension only when the defined fallback gate is evidenced.

## Definition of Done / hygiene

- Requested A-M comparison present: PASS.
- Exactly one implementation recommendation selected: PASS.
- Exactly one final verdict selected: PASS.
- No implementation or production changes: PASS.
- No Codex prompt written: PASS.
- No new general research introduced: PASS.
- Protected tracker/CA/CurrentTarget/HOROS authority preserved: PASS.
- Shared forward-transform gate preserved as NOT_VERIFIED: PASS.

FINAL: **PASS / COMPLETE FOR ARCHITECTURE DECISION REVIEW ONLY.**
