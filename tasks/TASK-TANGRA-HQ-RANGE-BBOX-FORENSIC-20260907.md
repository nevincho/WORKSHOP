# TASK — TANGRA HQ MONOCULAR RANGE / BBOX GEOMETRY FORENSIC

TASK_ID: TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: READY
EXECUTION_CLASS: MONITOR_ONLY
CODEX_ALLOWED: NO

## OBJECTIVE
Perform an independent computer-vision geometry forensic on one bounded discrepancy: HQ monocular class-size range is under-ranging by ~46% while detector/bbox coordinates are reported in 640x640. Determine whether the supplied numbers are mathematically consistent with an unaccounted crop/ROI or equivalent optical/image transform before detector resize, and define the smallest decisive live-frame test.

This task is ANALYSIS ONLY. Do not modify TANGRA source/runtime, HOROS, calibration, class-size profiles, detector, tracker, CA Kalman, Fusion, CURRENT_TARGET, command/actuation, or production configuration.

## SOURCE_PLAN_OR_REQUEST
Control Room owner request dated 2026-09-07. Analyze only the supplied evidence below and return a bounded forensic recommendation for later human/Codex/runtime validation.

## CURRENT_STATE
NOT VERIFIED against authoritative runtime/source in this task.

The numerical values below are owner-supplied forensic inputs. Treat them as GIVEN DATA for mathematics, not as independently verified runtime state.

## PREREQUISITES
- No wider TANGRA discovery required or authorized for this task.
- No runtime/Pi access required.
- No implementation required.
- Mathematical analysis must preserve unknowns as unknown.

## DEPENDENCIES
NONE. This forensic is independent and read-only.

## AFFECTED_COMPONENTS
- HQ image geometry
- detector preprocessing geometry
- bbox coordinate transforms
- monocular class-size range geometry
- display-vs-ranging bbox provenance

## PROTECTED_COMPONENTS
- HOROS implementation and validated behavior
- production detector/Hailo path
- NanoTracker
- existing CA Kalman
- Fusion
- CURRENT_TARGET authority
- production command/actuation logic
- validated runtime/configuration
- existing class-size profiles
- physical calibration values

## HARD CONSTRAINTS
1. Do not redesign the system.
2. Do not propose arbitrary correction factors.
3. Do not change class-size profiles.
4. Do not assume calibration is wrong unless evidence requires it.
5. Do not perform wider TANGRA repository discovery.
6. Do not invoke Codex.
7. Do not modify production/runtime.
8. Explicitly classify every conclusion as one of:
   - VERIFIED FROM GIVEN DATA
   - MATHEMATICALLY CONSISTENT
   - HYPOTHESIS
   - NOT VERIFIED

## GIVEN DATA

HQ calibration space:
- 2028 x 1520

HQ intrinsics:
- fx = 15756.86
- fy = 15848.54
- cx = 1014.00
- cy = 760.00

Current inference/detector space reported:
- 640 x 640

Current live bbox:
- W = 639.497807 px
- H = 369.792327 px

Physical extent corresponding visually to the displayed green bbox:
- W = 0.165 m
- H = 0.0835 m

Measured lens-to-target distance:
- Z = 2.585 m

Current runtime scaling assumes direct:
- 2028 x 1520 -> 640 x 640

This gives approximately:
- fx640 = 4972.579
- fy640 = 6673.069

Current range result:
- Rw = 1.283000 m
- Rh = 1.506795 m
- combined = 1.390402 m
- physical error = 1.194598 m
- under-range = 46.21%

Previous forensic conclusion supplied by owner:
- detector bbox and scaled intrinsics are both expressed in 640 x 640 coordinates;
- no simple coordinate-space mismatch was found.

## NEW HYPOTHESIS TO TEST
There may be an unaccounted crop/ROI before resize:

2028 x 1520 native
-> crop/ROI approximately 1014 x 760
-> resize to 640 x 640
-> detector bbox approximately 640 x 370

If intrinsics are incorrectly scaled from the full native frame instead of from the actual ROI geometry, effective focal lengths used for detector-space ranging would be wrong.

Hypothetical 1014 x 760 ROI simulation:
- fx_eff ~= 15756.86 * 640 / 1014 ~= 9945 px
- fy_eff ~= 15848.54 * 640 / 760 ~= 13346 px

Using current bbox:
- horizontal range ~= 2.566 m
- vertical range ~= 3.014 m
- combined ~= 2.781 m

Ground truth:
- 2.585 m

Owner notes:
- horizontal simulated ROI result differs from ground truth by ~0.7%
- inverse calculation indicates ROI width around 1006-1014 px would explain the horizontal measurement

## ANALYSIS REQUIRED
1. Determine which exact image transforms can produce this numerical pattern.
2. Determine whether a ~half-width ROI is quantitatively plausible.
3. Identify alternative causes capable of producing the same numerical signature.
4. Distinguish evidential signatures of:
   - crop/ROI mismatch
   - wrong focal scaling
   - bbox transform mismatch
   - display-vs-range bbox divergence
   - detector bbox covering a larger semantic region than the supplied physical extent
5. Derive exact equations for effective intrinsics after:
   - crop
   - resize
   - anisotropic resize
   - centered ROI
   - non-centered ROI
6. State exactly which values must be captured from ONE live frame to prove or refute the ROI hypothesis.
7. Produce the smallest decisive forensic test.

## REQUIRED EQUATION COVERAGE
For native intrinsics K = (fx, fy, cx, cy), ROI origin (x0,y0), ROI size (Wr,Hr), and output size (Wo,Ho), derive and apply:

sx = Wo / Wr
sy = Ho / Hr
fx' = sx * fx
fy' = sy * fy
cx' = sx * (cx - x0)
cy' = sy * (cy - y0)

Also address letterbox/padding or any other transform if it can reproduce the signature, with explicit offsets and scales rather than vague description.

## ACCEPTANCE_CRITERIA
A valid Scout/Reviewer forensic must:
- independently recompute the supplied range/scaling numbers;
- identify whether the ROI hypothesis is mathematically consistent without calling it verified;
- rank plausible root causes using only supplied evidence;
- derive exact image/intrinsic transform equations;
- define the minimum one-frame telemetry capture needed to disambiguate causes;
- define a decisive test with expected outcomes for ROI TRUE vs ROI FALSE;
- preserve protected components and all hard constraints;
- not propose arbitrary fudge factors or class-size changes;
- not claim physical/runtime verification.

## VALIDATION_METHOD
Independent mathematical recomputation and consistency analysis only. Optional deterministic scratch calculations are allowed, but no source/runtime modification and no wider TANGRA discovery.

## PRE_CHANGE_CHECKPOINT
N/A — read-only forensic; no target implementation change authorized.

## ROLLBACK_METHOD
N/A — no implementation/runtime changes permitted.

## EVIDENCE_PATHS
- evidence/TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907/SCOUT.md
- review/TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907.md

## REQUIRED OUTPUT FORMAT
Output ONLY these sections in evidence/review:

A. NUMERICAL ASSESSMENT
B. MOST LIKELY ROOT-CAUSE RANKING
C. REQUIRED LIVE VARIABLES
D. DECISIVE TEST
E. EXPECTED RESULT IF ROI HYPOTHESIS IS TRUE
F. EXPECTED RESULT IF ROI HYPOTHESIS IS FALSE
G. DO-NOT-CHANGE ITEMS

Every substantive conclusion must carry one explicit classification:
VERIFIED FROM GIVEN DATA / MATHEMATICALLY CONSISTENT / HYPOTHESIS / NOT VERIFIED
