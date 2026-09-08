# TASK 3 Evidence Report

TASK_ID: TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908

## Repository evidence inspected
- `TANGRA-DOCS/CURRENT_BASELINE.md`: HQ calibration provisional; production-wired MONOCULAR_CLASS_SIZE uses bbox + target profiles + provisional intrinsics; physical accuracy not yet validated; FPV two-axis multi-size support not physically calibrated.
- `TANGRA-DOCS/CURRENT_ACTIVE_MODULES.md`: MONOCULAR_CLASS_SIZE production-wired / physical accuracy open; HOROS downstream fail-open.
- `TANGRA-DOCS/ARCHITECTURE/HOROS_TARGET_SILHOUETTE_GEOMETRY_RESEARCH_20260908.md`: sparse structural range is an engineering hypothesis; point pairs require known/assumed physical separations; keypoints do not remove monocular scale/orientation ambiguity.
- TASK 1 frozen commit `c7b378841979f82b037c47be3571fa72a7b70e51` for point semantics/null behavior.
- TASK 2 frozen commit `4bd4b5d38357db501de07511aeabaa4c0ae058e1` for calibrated-plane contract and production transform NOT_VERIFIED gate.

## Evidence conclusion
No inspected evidence proves concrete production CAL->AI transform A or proves numerical production target dimensions are exact TASK 1 LEFT/RIGHT or NOSE/TAIL silhouette correspondences. No production dimensions/correspondences are embedded. All metric fixtures are explicitly SYNTHETIC.

## Implementation
Standalone `sparse_geometry_range_source.py` defines calibration/distortion verification gates, TASK 2-compatible calibrated input, target profile/span contracts, candidate evidence, anisotropic normalized span mathematics, uncertainty propagation, group-aware robust fusion, fail-closed disagreement/insufficient evidence, production metric gate and passive existing-range comparison. No protected runtime component is imported or modified.

## Tests
17/17 PASS. Coverage: synthetic top-down 8/20/50 m; consistent spans; corrupted outlier; insufficient spans; invalid/null NOSE/TAIL; dimension uncertainty; disagreement fail closed; malformed calibration/transform; near-zero span; mild synthetic foreshortening; uncertainty growth; repeatability; unverified correspondence; production metric gate; distortion handling; calibration verification gate; shadow comparison.

## Benchmark
SYNTHETIC host-only n=50,000: mean 0.05930015368 ms; median 0.051208 ms; p95 0.086491 ms; max 2.180426 ms. Pi5/end-to-end NOT_VERIFIED.

## Existing range comparison
Comparison interface implemented and deterministic test PASS. Live/prod A/B comparison NOT_PERFORMED / NOT_VERIFIED because authoritative runtime inputs/profile correspondences and production transform were not proven through this evidence path. No superiority claim.

## Dependencies
Python 3; NumPy; Python standard library.

## Exact TASK 3 files
- handoffs/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/sparse_geometry_range_source.py
- handoffs/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/test_sparse_geometry_range_source.py
- handoffs/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/benchmark_sparse_geometry_range_source.py
- evidence/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/MATH_ARCHITECTURE.md
- evidence/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/REPORT.md
- evidence/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/benchmark.json
- review/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908-REQUEST.md
- tasks/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908.md
