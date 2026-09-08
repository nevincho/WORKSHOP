# TASK 2 Mathematical / Architecture Note

## Scope
Coordinate transformation only. No image reconstruction, resize, retained 2028x1520 image, range, XYZ, LOS range, pose, temporal propagation, tracking, HOROS state write, guidance, or production promotion.

## Transform convention
The explicit homogeneous affine matrix A maps calibrated-plane continuous image coordinates into AI-plane coordinates:

p_AI_h = A * p_CAL_h

The adapter obtains calibrated coordinates only by inversion:

p_CAL_h = A^-1 * p_AI_h

The implementation permits any finite invertible 2D affine matrix with last row [0,0,1]. Axis-aligned crop/resize/pad transforms are generated as:

A = [[sx,0,tx],[0,sy,ty],[0,0,1]]

Crop then resize is represented by translation induced by the crop origin followed by scaling. Letterbox/padding is represented by scale plus output-plane offset. No crop/pad stage is silently assumed or omitted.

## Pixel convention
Coordinates are continuous image coordinates. Integer coordinate (0,0) denotes the center of the top-left pixel. Last pixel centers are (W-1,H-1). Bounding boxes are treated as geometric xyxy coordinates in the same continuous coordinate system and mapped by all four corners. No implicit +0.5/-0.5 convention is applied.

## Calibration contract
The supplied provisional HQ plane is 2028x1520 with K_CAL using fx=15756.86, fy=15848.54, cx=1014.0, cy=760.0 and zero distortion. These values are evidence/configuration data, not hard-coded into adapter geometry logic.

## Intrinsics consistency
For an affine A representing the same image-plane preprocessing:

K_AI = A * K_CAL.

The deterministic test projects the same normalized ray through K_CAL and K_AI and verifies that the resulting AI coordinate equals A applied to the calibrated coordinate. This is mathematical consistency only, not a production calibration validation.

## Production transform evidence gate
Search of available WORKSHOP and TANGRA-DOCS evidence did not establish an authoritative live chain proving sensor/raw geometry, ScalerCrop/ROI, HQ output geometry, AI crop/pad/letterbox behavior, and coordinate convention end-to-end. Therefore no concrete production A is selected. PRODUCTION_TRANSFORM_STATUS = NOT_VERIFIED.

## TASK 1 compatibility
Input contract mirrors TASK 1 geometry fields: bbox, center, sparse points, validity/null coordinates, frame identity/timestamp and provenance. Any invalid point or point with a null coordinate remains invalid with x=None/y=None after adaptation. No coordinate is manufactured.
