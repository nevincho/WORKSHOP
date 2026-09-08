# TASK 2 Mathematical / Architecture Note

## Scope
Coordinate transformation only. No image reconstruction, resize, retained 2028x1520 image, range, XYZ, LOS range, pose, temporal propagation, tracking, HOROS state write, guidance, or production promotion.

## Transform convention
The explicit homogeneous affine matrix A maps calibrated-plane continuous image coordinates into AI-plane coordinates: p_AI_h=A*p_CAL_h. The adapter obtains calibrated coordinates only by p_CAL_h=A^-1*p_AI_h. Any finite invertible 2D affine matrix with last row [0,0,1] is accepted.

Axis-aligned crop/resize/pad transforms are represented as A=[[sx,0,tx],[0,sy,ty],[0,0,1]]. Crop origin, resize and padding are explicit transform terms and are never silently assumed.

## Pixel convention
Coordinates are continuous image coordinates. Integer coordinate (0,0) denotes the center of the top-left pixel. Last pixel centers are (W-1,H-1). Bounding boxes use the same continuous coordinate system and are mapped by all four corners.

For center-aligned crop/resize/letterbox, the constructor uses:
x_AI=(x_CAL-crop_x+0.5)*sx-0.5+pad_x
y_AI=(y_CAL-crop_y+0.5)*sy-0.5+pad_y.
Thus half-pixel behavior is explicit in A rather than implicit.

## Calibration contract
The supplied provisional HQ plane is 2028x1520 with fx=15756.86, fy=15848.54, cx=1014.0, cy=760.0 and D=[0,0,0,0,0]. These are evidence/configuration data, not hard-coded into adapter geometry logic.

## Intrinsics consistency
For an affine A representing the same image-plane preprocessing, K_AI=A*K_CAL. The deterministic test projects the same normalized ray through K_CAL and K_AI and verifies equality with A applied to the calibrated coordinate. Mathematical consistency only; not production calibration validation.

## Production transform evidence gate
Available WORKSHOP/TANGRA-DOCS evidence did not prove the complete live sensor/raw -> ScalerCrop/ROI -> HQ output -> AI crop/resize/pad chain and coordinate convention. No concrete production A is selected. PRODUCTION_TRANSFORM_STATUS=NOT_VERIFIED.

## TASK 1 compatibility
Input mirrors TASK 1 bbox, center, sparse points, validity/null coordinates, frame identity/timestamp and provenance. Invalid or null points remain invalid with x=None/y=None. No coordinate is manufactured.
