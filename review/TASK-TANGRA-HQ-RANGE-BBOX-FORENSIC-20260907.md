A. NUMERICAL ASSESSMENT

- [VERIFIED FROM GIVEN DATA] Reviewer independently recomputed the direct full-frame detector-space intrinsics: fx=4972.579093 px and fy=6673.069474 px.
- [VERIFIED FROM GIVEN DATA] Reviewer independently recomputed Rw=1.282999787 m and Rh=1.506795194 m. The reported combined 1.390402 m is the geometric mean sqrt(Rw*Rh)=1.390402069 m.
- [MATHEMATICALLY CONSISTENT] To make the observed bbox agree with Z=2.585 m using the supplied physical dimensions requires detector-space fx=10018.798976 px and fy=11448.061860 px.
- [MATHEMATICALLY CONSISTENT] These correspond to an equivalent pre-resize source region of about 1006.546835 x 886.007232 px when resized to 640x640.
- [MATHEMATICALLY CONSISTENT] A 1014x760 ROI gives Rw=2.565999574 m and Rh=3.013590388 m. Therefore it is an excellent X-only fit but not a joint X/Y fit.
- [NOT VERIFIED] The existence of any actual ROI/crop/zoom in the live pipeline remains unverified.

B. MOST LIKELY ROOT-CAUSE RANKING

1. [HYPOTHESIS] Unaccounted effective scaling before detector-space ranging: crop/ROI, digital zoom, sensor mode, ISP crop/scale, or equivalent affine transform.
2. [HYPOTHESIS] Detector bbox semantic extent does not correspond to the supplied physical extent. Under current direct intrinsics and Z=2.585 m, the bbox corresponds to approximately 0.33244 m x 0.14325 m.
3. [HYPOTHESIS] Bbox transform mismatch between preprocessing/detector/output/range coordinate spaces.
4. [HYPOTHESIS] Display bbox and range-consumed bbox are not identical/provenance-linked.
5. [HYPOTHESIS] Focal scaling is based on the wrong current image geometry for a reason other than crop.
6. [NOT VERIFIED] Calibration values themselves are wrong. Current evidence does not require this conclusion.

C. REQUIRED LIVE VARIABLES

- [VERIFIED FROM GIVEN DATA] One frame_id/timestamp shared across capture, preprocess, detector, range and display records.
- [VERIFIED FROM GIVEN DATA] Actual capture dimensions.
- [VERIFIED FROM GIVEN DATA] Calibration-space dimensions and fx,fy,cx,cy used.
- [VERIFIED FROM GIVEN DATA] Every crop/ROI rectangle, resize dimension/scale, padding and post-resize crop in order.
- [VERIFIED FROM GIVEN DATA] Actual detector tensor dimensions.
- [VERIFIED FROM GIVEN DATA] Raw detector bbox and coordinate convention.
- [VERIFIED FROM GIVEN DATA] Bbox after each transform, exact range-input bbox, exact displayed bbox.
- [VERIFIED FROM GIVEN DATA] Exact fx/fy used by ranging and the image space they are claimed to represent.
- [VERIFIED FROM GIVEN DATA] Read-only class-size values used and resulting Rw/Rh/combined.

D. DECISIVE TEST

- [MATHEMATICALLY CONSISTENT] Capture one frozen live frame and construct a transform ledger from calibration space to detector space. For ROI origin (x0,y0), ROI size (Wr,Hr), output (Wo,Ho): sx=Wo/Wr, sy=Ho/Hr; fx'=sx*fx; fy'=sy*fy; cx'=sx*(cx-x0); cy'=sy*(cy-y0).
- [VERIFIED FROM GIVEN DATA] Centered ROI uses x0=(Wn-Wr)/2 and y0=(Hn-Hr)/2; non-centered ROI uses actual x0,y0. ROI position changes principal point, not focal scale.
- [VERIFIED FROM GIVEN DATA] Letterbox uses isotropic s=min(Wo/Wr,Ho/Hr), with fx'=s*fx, fy'=s*fy, cx'=s*(cx-x0)+pad_left, cy'=s*(cy-y0)+pad_top.
- [VERIFIED FROM GIVEN DATA] Resize-to-fill followed by crop uses s=max(Wo/Wr,Ho/Hr), with the post-resize crop offsets subtracted from principal point.
- [MATHEMATICALLY CONSISTENT] Compare actual composed scale with direct full-frame scales 0.3155818540 / 0.4210526316 and range-consistent scales 0.6358372783 / 0.7223417337. Recompute K from the actual ledger, then recompute range using the exact bbox consumed by ranging.
- [MATHEMATICALLY CONSISTENT] This single-frame test distinguishes transform geometry from bbox provenance without changing calibration or class sizes.

E. EXPECTED RESULT IF ROI HYPOTHESIS IS TRUE

- [HYPOTHESIS] The captured pipeline will expose a crop/zoom/equivalent transform before 640x640 detector input.
- [HYPOTHESIS] X-equivalent source width should be close to 1007-1014 px if the supplied physical width is correct.
- [HYPOTHESIS] To explain both axes solely by image scaling, source height should be close to 886 px, not 760 px, unless another anisotropic stage exists.
- [HYPOTHESIS] Intrinsics propagated through the actual transform will move the computed range toward 2.585 m without profile changes.

F. EXPECTED RESULT IF ROI HYPOTHESIS IS FALSE

- [HYPOTHESIS] The transform ledger will show true direct 2028x1520 -> 640x640 mapping with no hidden scale-changing stage.
- [HYPOTHESIS] Detector-space intrinsics will remain approximately fx=4972.58 and fy=6673.07.
- [HYPOTHESIS] The discrepancy must then be localized to bbox transform/provenance, semantic bbox-to-physical-size mismatch, or another current-image-geometry/focal-scaling mismatch.

G. DO-NOT-CHANGE ITEMS

- [VERIFIED FROM GIVEN DATA] Do not change HOROS, detector/Hailo, NanoTracker, CA Kalman, Fusion, CURRENT_TARGET, command/actuation or production runtime/configuration.
- [VERIFIED FROM GIVEN DATA] Do not change calibration values from this mathematical result alone.
- [VERIFIED FROM GIVEN DATA] Do not change class-size profiles.
- [VERIFIED FROM GIVEN DATA] Do not introduce empirical correction factors.
- [VERIFIED FROM GIVEN DATA] Do not claim ROI as verified until the one-frame transform ledger demonstrates it.

Reviewer verdict: PASS for the bounded mathematical forensic. The ROI/equivalent-transform explanation is mathematically consistent and currently the leading hypothesis, but the exact proposed 1014x760 ROI is not jointly consistent with both axes. Physical/runtime root cause remains NOT VERIFIED.