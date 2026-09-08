# TASK 3 Evidence Report

TASK_ID: TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908
STATUS: CORRECTED / READY_FOR_FINAL_REVIEW

## Evidence boundary
Repository evidence confirms the production-wired `MONOCULAR_CLASS_SIZE` path but physical class-size accuracy remains open, FPV multi-size support is not physically calibrated, TASK 2 production transform A remains NOT_VERIFIED, and sparse point pairs require explicit physical correspondence. No inspected evidence proves numerical production target dimensions are exact TASK 1 LEFT/RIGHT or NOSE/TAIL extrema. TASK 3 therefore embeds no production dimensions/correspondences; all metric fixtures are `SYNTHETIC`.

## Implementation
Standalone SHADOW `sparse_geometry_range_source.py` provides explicit calibration, calibrated-geometry, physical-span/profile, candidate evidence, robust fusion, uncertainty and passive existing-range comparison contracts. It uses anisotropic normalized span `q=sqrt((du/fx)^2+(dv/fy)^2)` and `Z=S*r/q` only for explicitly verified physical correspondences and explicit orientation projection factor r. Nonzero distortion fails closed unless coordinates are declared undistorted.

Candidate evidence records both calibrated pixel span and normalized calibrated span, physical span/uncertainty, candidate range/uncertainty/confidence/validity/rejection, independence group, profile-span provenance, source geometry reference, calibration id, transform id/version and orientation factor.

## Review correction cycle 1
Initial commit `1cd2e641f4387aa190071839d763bb2b9732dc1f` received PASS_WITH_CONDITIONS for two bounded evidence-contract defects:
1. candidate evidence exposed normalized span but not explicit calibrated pixel length;
2. candidate provenance did not directly carry source geometry/calibration/transform identity.
Corrections add `calibrated_length_px` and candidate-level `source_geometry_ref`, `calibration_id`, `transform_id`, `transform_version` provenance only. No mathematical/architecture expansion.

## Tests
Corrected complete suite: 18/18 PASS. Coverage: exact SYNTHETIC top-down 8/20/50 m; consistent spans; one corrupted outlier; insufficient independent evidence; invalid/null NOSE/TAIL; physical-dimension uncertainty; disagreement fail closed; malformed calibration/transform; near-zero span; mild SYNTHETIC foreshortening; uncertainty behavior; repeatability; unverified correspondence; production metric gate; distortion handling; calibration production gate; passive existing-range comparison; explicit calibrated pixel span and full candidate provenance.

## Corrected benchmark
SYNTHETIC host-only, n=50,000: mean 0.06209089742 ms; median 0.053601 ms; p95 0.090216 ms; max 22.973591 ms. Maximum is a single host scheduling/outlier observation and is not an end-to-end claim. Pi5/end-to-end NOT_VERIFIED.

## Existing range comparison
Passive interface accepts externally supplied existing range evidence such as MONOCULAR_CLASS_SIZE and reports absolute/relative delta only when both observations are valid. Live/production A/B comparison NOT_PERFORMED / NOT_VERIFIED. No superiority claim.

## Dependencies
Python 3; NumPy; Python standard library.

## Architecture isolation
No TASK 1/TASK 2 source, HQ acquisition, detector, NanoTracker, CA Kalman, CurrentTargetManager, existing range estimator, HOROS authoritative estimator, Guidance, Dashboard, command or flight-control path is modified or imported for production integration.
