A. NUMERICAL ASSESSMENT

- [VERIFIED FROM GIVEN DATA] Direct full-frame scaling 2028x1520 -> 640x640 gives sx=640/2028=0.3155818540, sy=640/1520=0.4210526316, fx'=4972.5790927 px, fy'=6673.0694737 px.
- [VERIFIED FROM GIVEN DATA] With W=0.165 m, H=0.0835 m, bbox_w=639.497807 px, bbox_h=369.792327 px, monocular size ranging gives Rw=fx'W/bbox_w=1.282999787 m and Rh=fy'H/bbox_h=1.506795194 m.
- [VERIFIED FROM GIVEN DATA] The supplied combined range 1.390402 m is the geometric mean sqrt(Rw*Rh)=1.390402069 m, not the arithmetic mean (1.394897491 m).
- [VERIFIED FROM GIVEN DATA] At measured Z=2.585 m, direct full-frame intrinsics predict bbox_w=317.398665 px and bbox_h=215.551761 px for the supplied physical extents. The observed bbox is larger by factors 2.014809x (X) and 1.715562x (Y).
- [MATHEMATICALLY CONSISTENT] If the discrepancy is entirely caused by an unaccounted crop/ROI followed by resize to 640x640, the effective detector-space focal lengths required by the measured range are fx_req=Z*bbox_w/W=10018.798976 px and fy_req=Z*bbox_h/H=11448.061860 px.
- [MATHEMATICALLY CONSISTENT] Those focal lengths correspond to an equivalent pre-resize ROI size Wr=fx*640/fx_req=1006.546835 px and Hr=fy*640/fy_req=886.007232 px. Therefore a roughly half-width ROI is quantitatively plausible in X.
- [MATHEMATICALLY CONSISTENT] A 1014x760 ROI gives fx_eff=9945.158185 px and fy_eff=13346.138947 px. It yields Rw=2.565999574 m and Rh=3.013590388 m; geometric combined range is 2.780899 m. Horizontal error versus 2.585 m is about -0.735%, so the X hypothesis is strong numerically.
- [VERIFIED FROM GIVEN DATA] The proposed 760 px ROI height does not explain the Y measurement at the same physical dimensions and distance: the Y-consistent equivalent height is about 886.0 px, not 760 px. Thus the exact 1014x760 ROI hypothesis is not jointly supported by X and Y.
- [HYPOTHESIS] A crop/digital-zoom/sensor-mode/ISP transform with approximately 1007x886 effective source geometry could reproduce both axes without changing calibration values themselves.
- [NOT VERIFIED] No supplied evidence establishes that such an ROI actually exists in the live pipeline.

Exact transform equations:
- [VERIFIED FROM GIVEN DATA] Native intrinsics K=(fx,fy,cx,cy), ROI origin (x0,y0), ROI size (Wr,Hr), output (Wo,Ho): sx=Wo/Wr, sy=Ho/Hr; fx'=sx*fx; fy'=sy*fy; cx'=sx*(cx-x0); cy'=sy*(cy-y0).
- [VERIFIED FROM GIVEN DATA] Pure crop without resize: fx'=fx; fy'=fy; cx'=cx-x0; cy'=cy-y0.
- [VERIFIED FROM GIVEN DATA] Anisotropic resize after crop uses independent sx and sy exactly as above.
- [VERIFIED FROM GIVEN DATA] Centered ROI: x0=(Wn-Wr)/2, y0=(Hn-Hr)/2. Non-centered ROI uses the actual x0,y0; ROI position changes principal point but not focal-length scale.
- [VERIFIED FROM GIVEN DATA] For isotropic letterbox after ROI, s=min(Wo/Wr,Ho/Hr), pad_x=(Wo-s*Wr)/2, pad_y=(Ho-s*Hr)/2; fx'=s*fx, fy'=s*fy, cx'=s*(cx-x0)+pad_x, cy'=s*(cy-y0)+pad_y. Asymmetric padding replaces pad_x/pad_y with actual left/top offsets.
- [VERIFIED FROM GIVEN DATA] For resize-to-fill/cover followed by crop, s=max(Wo/Wr,Ho/Hr), then fx'=s*fx, fy'=s*fy, cx'=s*(cx-x0)-crop_left, cy'=s*(cy-y0)-crop_top.
- [MATHEMATICALLY CONSISTENT] Any affine image transform whose X/Y scale terms are about 2.0148x/1.7156x larger than the currently assumed full-frame scales produces the same size-ranging numerical signature. Crop is one such transform, not the only one.

B. MOST LIKELY ROOT-CAUSE RANKING

1. [HYPOTHESIS] Unaccounted effective image scaling before detector-space ranging: ROI/crop, digital zoom, sensor-mode crop, ISP crop/scale, or equivalent resize chain. Confidence: medium-high mathematically, NOT VERIFIED operationally. Reason: required scale factors are directly recoverable from the measured distance and bbox; half-width geometry matches X to <1%.
2. [HYPOTHESIS] Bbox semantic extent does not correspond to the supplied 0.165x0.0835 m physical extent. Under the currently assumed intrinsics, the observed bbox at 2.585 m corresponds to about 0.33244 m x 0.14325 m, i.e. 2.0148x wider and 1.7156x taller than the supplied extent. This can reproduce the same signature without any ROI.
3. [HYPOTHESIS] Bbox transform mismatch between detector/preprocess/output spaces (e.g. bbox de-letterboxing/de-scaling applied incorrectly or applied twice). It can produce independent X/Y scale errors matching the observed factors.
4. [HYPOTHESIS] Display-vs-range bbox divergence: the green display box and the box consumed by the range calculation may not be the same coordinates/provenance. This cannot be excluded from supplied data.
5. [HYPOTHESIS] Wrong focal scaling for reasons other than ROI, such as using calibration-space dimensions that are not the actual current camera mode. Numerically equivalent to item 1 but distinct operational cause.
6. [NOT VERIFIED] Calibration itself is wrong. The supplied evidence does not require this conclusion and it should not be assumed.

C. REQUIRED LIVE VARIABLES

Capture all of the following for ONE frame with a single frame_id/timestamp:
- [VERIFIED FROM GIVEN DATA] Native/capture frame width and height actually delivered by the HQ camera path.
- [VERIFIED FROM GIVEN DATA] Calibration profile ID and calibration-space width/height plus fx,fy,cx,cy used on that frame.
- [VERIFIED FROM GIVEN DATA] Every preprocessing stage in order, with input/output dimensions.
- [VERIFIED FROM GIVEN DATA] Any ROI/crop rectangle: x0,y0,Wr,Hr.
- [VERIFIED FROM GIVEN DATA] Any resize scale sx,sy or isotropic s.
- [VERIFIED FROM GIVEN DATA] Any letterbox/padding: left,top,right,bottom.
- [VERIFIED FROM GIVEN DATA] Any resize-to-fill/post-resize crop offsets.
- [VERIFIED FROM GIVEN DATA] Detector tensor dimensions actually presented to Hailo/model.
- [VERIFIED FROM GIVEN DATA] Raw detector bbox before any reverse transform, including coordinate convention (xyxy/xywh, normalized/pixels).
- [VERIFIED FROM GIVEN DATA] Bbox after every transform back toward display/range space.
- [VERIFIED FROM GIVEN DATA] Exact bbox used by monocular range calculation.
- [VERIFIED FROM GIVEN DATA] Exact bbox drawn as the green display box.
- [VERIFIED FROM GIVEN DATA] fx,fy actually used by the range calculation for that frame and the dimensions they are claimed to correspond to.
- [VERIFIED FROM GIVEN DATA] Physical class-size values actually used by the range call, read-only.
- [VERIFIED FROM GIVEN DATA] Final Rw,Rh,combined range and combination rule.
- [VERIFIED FROM GIVEN DATA] Measured lens-to-target Z for the same frame/test setup.

D. DECISIVE TEST

[MATHEMATICALLY CONSISTENT] Smallest decisive test: instrument one frozen live frame read-only and record the transform ledger from calibrated HQ image to detector tensor, together with the exact raw detector bbox and exact range-input bbox. Compose the declared transforms into one affine mapping:

x_out = ax*x_native + bx
y_out = ay*y_native + by

For crop+resize, ax=Wo/Wr and ay=Ho/Hr. Compare the composed ax,ay with:
- assumed full-frame ax_full=640/2028=0.3155818540, ay_full=640/1520=0.4210526316;
- range-consistent required scales ax_req=fx_req/fx=0.6358247 and ay_req=fy_req/fy=0.7223435.

Then recompute detector-space intrinsics strictly from the captured transform ledger, not from assumed dimensions, and recompute Rw/Rh from the exact bbox consumed by ranging.

Decision rule:
1. If captured transform ledger contains crop/zoom/equivalent scaling and derived fx',fy' move the range to the measured Z while raw/range/display bboxes are provenance-consistent, ROI/equivalent-transform hypothesis is supported.
2. If transform ledger is truly direct 2028x1520 -> 640x640, then ROI hypothesis is refuted for that frame; inspect bbox provenance/semantic extent next without changing profiles.
3. If raw detector bbox and range bbox differ by an unexplained scale/offset, classify bbox-transform mismatch.
4. If range bbox and displayed green bbox differ, classify display-vs-range divergence.
5. If all transforms/bboxes are consistent but physical extent does not match the semantic object region enclosed by bbox, semantic-extent mismatch remains the leading cause.

E. EXPECTED RESULT IF ROI HYPOTHESIS IS TRUE

- [HYPOTHESIS] The live transform ledger will expose an ROI/crop/digital-zoom/sensor-mode/ISP-equivalent source region before the 640x640 detector tensor.
- [HYPOTHESIS] Its effective source width should be near 1006-1014 px if X is the clean axis and the supplied physical width is correct.
- [HYPOTHESIS] To explain both axes solely by transform geometry with the supplied physical dimensions, effective source height should be near 886 px, not 760 px, unless an additional anisotropic transform exists.
- [HYPOTHESIS] Recomputing K through the actual transform will approximately double fx relative to the current full-frame scaling and increase fy by about 1.716x relative to current scaling; range will move toward 2.585 m without changing class-size values.
- [HYPOTHESIS] Raw detector bbox, range bbox and displayed bbox will be mutually traceable through known transforms.

F. EXPECTED RESULT IF ROI HYPOTHESIS IS FALSE

- [HYPOTHESIS] The transform ledger will show no pre-detector crop/zoom/equivalent scale; composed mapping will match direct full-frame scaling within numeric tolerance.
- [HYPOTHESIS] Correctly propagated detector-space intrinsics will remain about fx=4972.58, fy=6673.07.
- [HYPOTHESIS] The 2.585 m truth will then require another explanation: bbox transform/provenance divergence, semantic bbox-to-physical-size mismatch, or a non-ROI focal/calibration-mode mismatch.
- [HYPOTHESIS] If range bbox differs from raw/display bbox, the mismatch will be directly measurable from that single frame.
- [HYPOTHESIS] If all bboxes and transforms agree, the observed bbox implies approximately 0.33244 m x 0.14325 m physical semantic extent under the current intrinsics at 2.585 m; this is the quantitative signature to compare against what the detector box actually encloses.

G. DO-NOT-CHANGE ITEMS

- [VERIFIED FROM GIVEN DATA] Do not change HOROS implementation or validated HOROS behavior.
- [VERIFIED FROM GIVEN DATA] Do not change production detector/Hailo, NanoTracker, CA Kalman, Fusion, CURRENT_TARGET, command/actuation, or runtime configuration during this forensic.
- [VERIFIED FROM GIVEN DATA] Do not change calibration values based on this analysis alone.
- [VERIFIED FROM GIVEN DATA] Do not change class-size profiles to compensate for the range error.
- [VERIFIED FROM GIVEN DATA] Do not introduce empirical/fudge correction factors.
- [VERIFIED FROM GIVEN DATA] Do not infer ROI existence from numerical agreement alone; capture the one-frame transform ledger first.
- [VERIFIED FROM GIVEN DATA] Do not claim physical/runtime verification from this mathematical forensic.