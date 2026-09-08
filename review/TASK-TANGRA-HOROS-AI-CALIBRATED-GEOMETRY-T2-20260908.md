# TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908 — Independent Review Cycle 1

REVIEW_RESULT: PASS_WITH_CONDITIONS
COMMIT_REVIEWED: 1e112de0e197b7dff3a97872282f0ddfe320babe

## Verified
- Explicit finite invertible affine CAL->AI matrix with inverse AI->CAL mapping.
- Crop/resize/padding represented by transform parameters rather than hidden assumptions.
- TASK 1 equivalent bbox/center/sparse-point contract; invalid/null sparse points remain null/invalid.
- Non-invertible and malformed transforms fail closed.
- K_AI=A*K_CAL consistency test is mathematically correct for affine A.
- No concrete production A is fabricated; production transform remains NOT_VERIFIED.
- No TASK 1 or protected runtime modification; no image reconstruction, range, tracking, HOROS or Guidance integration.
- 12 deterministic tests and bounded host microbenchmark are appropriately scoped.

## Concrete bounded defect
The declared pixel convention says integer coordinates denote pixel centers, but the practical full-frame resize/crop/letterbox fixtures construct resize transforms with zero half-pixel translation. Under the declared center convention, a standard center-aligned resize should use x_out=(x_in+0.5)*sx-0.5 (and y analog), with crop-origin and padding terms composed explicitly. Leaving this implicit makes the resize examples internally inconsistent with the documented convention and could create a systematic sub-pixel offset when a concrete runtime transform is later instantiated.

## Required correction
Add a deterministic center-aligned crop/resize transform constructor implementing the documented half-pixel terms; update resize, crop+resize, padding/letterbox and boundary tests/documentation to use and assert that convention. Keep the generic affine contract unchanged. Rerun the complete test suite and affected coordinate microbenchmark. No architecture expansion.

TASK2_COMPLETE: NO
BLOCKER: bounded pixel-center convention inconsistency only.
