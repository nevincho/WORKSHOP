# TANGRA-RESEARCH-LAB-02 — Worker Evidence

TASK_ID: TANGRA-RESEARCH-LAB-02

ROLE: WORKER

DATE: 2026-10-05

STATUS: REVIEW_REQUIRED

TARGET_CHANGES: NONE

PI_OR_RUNTIME_ACCESSED: NO

CODEX_USED: NO

## 1. Result boundary

The qualified evidence supports one near-field range observation, provisional intrinsic calibration, algebraic range/LOS sensitivity, and static paired-capture timing observations. It does **not** support a calibrated uncertainty distribution, an operational range curve, final HQ↔WIDE extrinsics, carrier pose, LOCAL_ENU/world position, moving-target paired-camera geometry, or current production-source/runtime identity.

The strongest quantitative conclusion is therefore bounded: the 4.36 m truth and 4.366 m estimate differ by 0.006 m (0.1376%) at one near-field point, while the estimator itself reported 1.774 m uncertainty (40.6322% of the estimate). That small residual is evidence for the point, not for a full curve or for world position.

## 2. Exact sources and provenance

Qualified target ref: `nevincho/TANGRA-DOCS@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba`.

| ID | Exact source | Date | Use |
|---|---|---:|---|
| S01 | `REPORTS/HQ_POC_RANGE_AND_MULTI_OBJECT_PHYSICAL_EVIDENCE_20260915.md` | 2026-09-15 | 4.36/4.366 point, 1.774 m reported uncertainty, 4.00 m focus, five FPV profiles, invalid cross-domain scale attempt and rollback |
| S02 | `REPORTS/TANGRA_CALIBRATION_AND_HOROS_VALIDATION_2026-09-05.md` | 2026-09-05 | provisional HQ/WIDE intrinsics, reprojection evidence, 35.6 mm baseline, paired timestamp deltas, extrinsics/world gaps |
| S03 | `REPORTS/HOROS_DUAL_CAMERA_LOCAL_MAPPING_2026-09-06.md` | 2026-09-06 | class-size formula path; assumed identity rotation/baseline-X development geometry; explicit non-authoritative boundary |
| S04 | `CURRENT_SYSTEM.md`, `CURRENT_BASELINE.md` | through 2026-10-04 | current bounded state and open physical metric promotion; dated runtime statements only, not fresh Worker observation |
| S05 | WORKSHOP `evidence/TASK-TANGRA-HQ-RANGE-BBOX-FORENSIC-20260907/SCOUT.md` + matching independent review | 2026-09-07 | exact image-transform equations; mathematical domain mismatch hypotheses; single-frame decisive test |
| S06 | WORKSHOP second-object forensic evidence + review | 2026-09-07 | confirms geometry/focal/bbox-scale confounding and rejects an exact single reverse-solved crop as universal explanation |
| S07 | WORKSHOP dual-stream metric-path research/live addendum + independent review | 2026-09-08 | exact forward transform remains NOT VERIFIED; class/silhouette/frame identity are separate domains |
| S08 | WORKSHOP metric-geometry architecture decision + independent review | 2026-09-08 | calibrated geometry is sufficient only after forward transform is known; no implementation conclusion used here |

Git CLI could not authenticate to the private target repositories. Exact-ref reads were performed through the authenticated GitHub connector. Blob SHA for S01: `e7cd460a2f0e1fc118b99002d75a4122635b428b`; S02: `19883482c21b83ff232ae4d421be6953fec2a461`.

Fresh production source/runtime: **NOT VERIFIED**. No Pi/runtime access was attempted.

## 3. Parameter and transform authority table

| Stage/input | Value/status | Class | Authority/evidence | Consequence |
|---|---|---|---|---|
| HQ calibration plane | 2028×1520 | calibrated candidate | S02, PROVISIONAL PASS | Valid only for locked optical state represented by calibration |
| HQ K | fx 15756.86, fy 15848.54, cx 1014, cy 760 px | calibrated candidate | S02 | Focal/principal point covariance not supplied |
| HQ distortion | zero vector in candidate | assumed/candidate | S02 | Zero distortion is not independently qualified across operational field |
| HQ reprojection RMS | ~1.239 px | measured calibration residual | S02 | Residual is not focal-length uncertainty and is not used as one |
| focus | 4.00 m for near-field set | measured/configured | S01 | Not infinity-focus qualification |
| AI/runtime plane | 640×640 reported | observed dated state | S01/S04/S07 | Exact sensor→ScalerCrop→ISP→AI mapping is NOT VERIFIED |
| calibration→AI transform `A` | missing | NOT VERIFIED | S05/S07/S08 | Cannot propagate K or bbox to a proven common domain |
| detector bbox | live 640×640 domain | measured runtime variable, values absent for 4.36 m point | S01 | Point cannot be independently recomputed from bbox |
| tracker/CA/range bbox lineage | incomplete for the 4.36 m sample | NOT VERIFIED | S05-S07 | Semantic/transform uncertainty unbounded |
| class identity feeding range | FPV at the point; exact stabilization provenance incomplete | derived/NOT VERIFIED detail | S01/S07 | Wrong/unstable class changes size prior independently of geometry |
| FPV size profiles | 0.20×0.25, 0.30×0.30, 0.40×0.40, 0.50×0.50, 0.60×0.60 m; equal-weight mean | synthetic/model-derived prior | S01 explicitly says not physically calibrated | Dominant evidenced model spread; not target-population truth |
| axis ranges | `Rw=fx W/pw`, `Rh=fy H/ph` | derived | S03/S05 | Requires K and bbox in same coordinate domain |
| final range | equal-weight multi-profile output; axis geometric-mean behavior evidenced in forensic | derived | S01/S05 | 4.366 m is estimator output, not independent truth |
| physical truth at point | 4.36 m camera-to-target | measured | S01 | Independent of estimator in method, but instrument/procedure uncertainty absent |
| reported range uncertainty | 1.774 m | derived estimator output | S01 | Not independently calibrated coverage/covariance |
| LOS ray | centre + K | derived | S07/S08 | Only defensible in calibration plane after `A^-1`; live `A` absent |
| HQ↔WIDE baseline magnitude | ~0.0356 m | physically measured | S02 | Magnitude alone is not translation vector/extrinsics |
| HQ↔WIDE R/T | unsolved | missing / NOT VERIFIED | S02 | No physically calibrated stereo/world fusion |
| paired sensor deltas | 4.807, 44.751, 50.691 ms | measured on static calibration pairs | S02 | Static usefulness does not validate moving-target alignment |
| observation source time / age | required, values absent | missing / NOT VERIFIED | S07/S08 | Motion displacement and stale-state error unbounded |
| carrier attitude/pose | absent | missing / NOT VERIFIED | S02 | Camera-frame ray cannot be promoted to world/LOCAL_ENU |
| LOCAL_ENU transform | incomplete | missing / NOT VERIFIED | S02 | World position unsupported |
| development dual-camera transform | identity rotation + baseline X | explicit test assumption | S03 | Must not be treated as measured geometry |

## 4. Processing domains and equations

The valid monocular equations require a single coordinate domain:

`Rw = fx * W / pw`, `Rh = fy * H / ph`, `R = sqrt(Rw*Rh)`.

For small independent deterministic perturbations, the algebraic first-order relation is:

`dR/R = 0.5(df_x/f_x + df_y/f_y + dW/W + dH/H - dpw/pw - dph/ph)`.

This is sensitivity, not a covariance result. The required distributions and correlations are not evidenced, so Monte Carlo was not performed.

The invalid 2026-09-15 scale candidate combined manual 2028×1520 segmented bboxes with the live 640×640 estimator domain. It was falsified live (~2 m output at a 4.50 m target) and rolled back byte-for-byte. Those replay values are excluded from qualification.

## 5. Ground-truth and methodology audit

| Claim/test | Actual independent quantity | Method verdict |
|---|---|---|
| 4.36 m → 4.366 m | physical camera-to-target measurement independent of estimator | **SUPPORTED AT ONE POINT**; measuring instrument/procedure uncertainty absent |
| estimator `range_uncertainty_m=1.774` | produced by same estimator path | **NOT independent ground truth**; coverage/calibration NOT VERIFIED |
| HOROS `input_range_m=4.366` | copied upstream estimate | **Ingress evidence only**; self-comparison cannot validate HOROS metric accuracy |
| 2028×1520 replay scale | manual segmentation in different bbox domain | **REJECTED METHODOLOGY** and physically falsified; rollback confirmed |
| provisional intrinsics PnP at 2.43/2.58 m | physical board/distance evidence | **PARTIAL intrinsic evidence** under locked near-field focus; not operational/infinity focus |
| paired captures on static board | sensor timestamp deltas | **PAIRING OPERATIONAL FOR STATIC TARGET**; moving-target geometric accuracy NOT VERIFIED |
| 35.6 mm baseline | physical separation magnitude | **INSUFFICIENT for R/T or stereo accuracy** |
| assumed identity rotation/baseline-X | development configuration | **SYNTHETIC ASSUMPTION**, not physical truth |
| Dashboard/HOROS XYZ from range | downstream derived state | Cannot exceed upstream range/LOS/pose qualification; world validation unsupported |

No circular validation was accepted. In particular, estimator uncertainty and downstream reuse of the same range were not counted as independent confirmation.

## 6. Deterministic sensitivity results

Reproducible artifacts:

- `physical_state_sensitivity.py` SHA-256 `11facaeefa8f19f932a05958b0ee5d41b208cfb686308277c99427380c71e4ee`
- `physical_state_sensitivity.json` SHA-256 `bd4920496dcd236b6ceb20cfacbf4cfe4500a505204436ac5799e187da4a0546`

Command: `python3 evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.py`.

### 6.1 Single point

- residual: 0.006 m;
- residual/truth: 0.137614679%;
- reported uncertainty/estimate: 40.632157581%;
- residual/reported uncertainty: 0.003382187.

The last number does not establish uncertainty calibration; one point cannot measure coverage.

### 6.2 One-factor relative sweep

The ±1/2/5/10% grid is explicitly synthetic and distribution-free. A focal or physical-size change maps linearly to range. A bbox-scale change maps inversely; at 4.366 m, +5% bbox produces −0.2079 m, while −5% produces +0.2298 m. This asymmetry is exact algebra, not noise modelling.

### 6.3 Documented FPV profile-only spread

At fixed bbox and calibration, the five documented profiles have geometric size scales 0.223607, 0.3, 0.4, 0.5 and 0.6 m. Relative to their equal-weight mean, their isolated range ratios are 0.552496, 0.741251, 0.988334, 1.235418 and 1.482501. If the mean output is normalized to 4.366 m, individual profile contributions span 2.4122–6.4726 m, or −44.75% to +48.25% around the equal-weight mean.

This does not describe a drone population distribution. It quantifies sensitivity to the estimator's own documented synthetic/model-derived hypotheses and shows why the 6 mm point residual must not be generalized.

### 6.4 LOS pixel sensitivity

In the provisional 2028×1520 calibration plane, a synthetic 1 px centre offset is 0.06346 mrad horizontally and 0.06310 mrad vertically, corresponding to ~0.277/0.275 mm cross-range at 4.366 m. Ten pixels correspond to ~2.771/2.755 mm. These values do not apply directly to AI-plane pixels until `A` is verified.

### 6.5 Pair timing coefficient

For the recorded deltas, displacement is 4.807, 44.751 and 50.691 mm per 1 m/s of relative motion. This is a normalized coefficient, not an assumed TANGRA target speed. Without source timestamps, motion and measurement age, moving-target spatial error remains unbounded.

## 7. First-order physical-state error budget

| Term | Range | LOS/camera | World/LOCAL_ENU | Current numerical status |
|---|---|---|---|---|
| physical size prior/semantic extent | first-order +1:1 scale | none directly | propagates through range | documented profile-only −44.75%/+48.25%; true distribution NOT VERIFIED |
| bbox width/height | inverse scale | centre/extent influences ray | propagates | synthetic sweep only; live uncertainty absent |
| fx/fy | first-order +1:1 scale jointly per equation | angular scale | propagates | values evidenced; parameter covariance absent |
| cx/cy / bbox centre | no first-order size effect | ray angle | propagates | values evidenced; live centre uncertainty absent |
| calibration reprojection | not a focal covariance | point residual | propagates | 1.239 px residual only; not converted to parameter sigma |
| calibration→AI transform | systematic scale/offset/domain | systematic ray bias | propagates | **UNBOUNDED / NOT VERIFIED** |
| focus/optical state | changes effective calibration | changes ray/calibration | propagates | near-field 4.00 m only; operational state NOT VERIFIED |
| target pose/foreshortening | biases visible extent | changes semantic centre | propagates | **UNBOUNDED / NOT VERIFIED** |
| class provenance | selects size hypotheses | indirect | propagates | incomplete trace; **NOT VERIFIED** |
| physical truth measurement | affects residual | n/a | n/a | value given; instrument/procedure uncertainty absent |
| HQ↔WIDE R/T | no monocular effect | cross-camera mapping | essential | **UNBOUNDED / NOT VERIFIED** |
| carrier attitude/position | no camera-frame range effect | rotates ray | essential | **UNBOUNDED / NOT VERIFIED** |
| timestamp/age/jitter | motion-dependent | motion-dependent | motion-dependent | only static pair deltas; live age **NOT VERIFIED** |
| estimator correlations | affects combined uncertainty | n/a | propagates | **NOT VERIFIED**; no quadrature/Monte Carlo justified |

Because multiple systematic terms are unbounded, no defensible scalar total world-position error or covariance can be reported. Adding only known small terms would create false precision.

## 8. Claim qualification

| Claim | Classification | Confidence | Falsifier / closure evidence |
|---|---|---|---|
| Current estimator matched 4.36 m at the recorded near-field point | PARTIALLY VALIDATED / single point | high for recorded report, not fresh runtime | authenticated raw frame/telemetry and measurement record contradicting pairing |
| Full range curve is accurate | UNSUPPORTED / NOT VERIFIED | high | multi-distance, multi-target, multi-angle independent truth with preregistered tolerance |
| 1.774 m uncertainty is calibrated | NOT VERIFIED | high | sufficient independent residual series showing required coverage/consistency |
| Provisional HQ intrinsics support bounded near-field board work | PARTIALLY VALIDATED | medium-high | independent recalibration/holdout failure under same optical state |
| Live AI bbox is correctly mapped to calibration K | NOT VERIFIED | high | one-frame exact transform ledger and round-trip geometry |
| One fixed hidden crop explains all historic error | REJECTED as universal explanation | medium-high | existing two-object reverse solutions conflict; a captured common transform plus corrected physical extents could falsify this rejection |
| 35.6 mm baseline establishes stereo accuracy | UNSUPPORTED | high | solved/validated R/T plus known-geometry residuals |
| Camera-frame LOS is physically valid in live path | NOT VERIFIED | high | exact transform, K provenance, centre/bbox lineage, rigid-marker angular validation |
| World/LOCAL_ENU position is validated | UNSUPPORTED | high | synchronized camera geometry, extrinsics, carrier pose/time and independent surveyed world truth |
| HOROS ingestion of 4.366 validates HOROS metric position | REJECTED methodology | high | independent world-state residual, not reuse of upstream range |

## 9. Ranked minimum physical experiments

### P0-1 — One-frame geometry/provenance ledger

Freeze one live frame and record frame ID/source timestamp, sensor mode, ScalerCrop/ROI, every resize/pad/crop/orientation, detector tensor, raw detector bbox, post-tracker/CA bbox, exact range bbox, display bbox, K/profile/class provenance and composed `A/A^-1`.

Pass: declared transform round-trip ≤0.5 px for tested interior points and every bbox is linked without unexplained scale/offset. Fail: any unexplained transform, stale frame/config generation, or range bbox not traceable to source frame. This closes the highest-impact domain ambiguity without changing production behavior.

### P0-2 — Independent rigid-target range curve

Use rigid targets with directly measured physical extents corresponding to the estimator's semantic bbox, at minimum three distances spanning the intended next validation envelope, centre plus two off-axis positions, repeated frames, fixed documented focus. Predeclare allowable absolute/relative residual and uncertainty-coverage criteria before capture.

Pass: preregistered residual and repeatability limits at every condition; uncertainty interval coverage meets preregistered criterion. Fail: any condition exceeds it. The current 4.36 m point remains one datum, not the criterion.

### P0-3 — Class/size/pose isolation

Hold camera geometry and distance fixed; capture a rigid target under controlled orientation while separately logging instantaneous detector class, range-consumed class/profile set and visible semantic extent.

Pass: range provenance identifies the intended class/profile and orientation-dependent extent stays within preregistered error. Fail: class/profile switches or foreshortening drive residual beyond criterion. This separates geometry from prior/silhouette error.

### P1-1 — HQ↔WIDE extrinsics and holdout

Solve R/T from multiple paired shared poses after sufficient common features exist, then test on withheld known 3D geometry. Pass/fail must be defined in angular and metric residuals appropriate to the intended envelope; baseline magnitude alone is not acceptance.

### P1-2 — Synchronized pose/world validation

With timestamped carrier attitude/position and validated camera-to-body transform, observe surveyed static points and a controlled moving target. Pass: preregistered camera-frame and LOCAL_ENU residuals by age bin; fail on frame mismatch, stale age, or residual excess. This is the first experiment capable of validating world position.

### P1-3 — Measurement-age motion test

Log sensor timestamp, inference completion, range time, HOROS ingest time and render time against controlled target motion. Pass: age is explicit end-to-end and displacement-compensated residual meets threshold. Fail: missing timestamp edge or age-dependent bias beyond criterion.

## 10. Preservation recommendation

KEEP/PROTECT:

- existing estimator and provisional calibration unchanged pending independent curve evidence;
- protected HQ→detector→NanoTracker→CA→CurrentTarget authority;
- HOROS non-authoritative/fail-open metric gate;
- explicit rejection of incompatible bbox-domain calibration and arbitrary global correction constants;
- separation of camera geometry, class prior, silhouette, frame identity, timing and world-pose validation.

No redesign or parameter change is justified by this task.

## 11. Execution ledger

| UTC date | Action | Result |
|---|---|---|
| 2026-10-05 | Pulled WORKSHOP `origin/main`; reconciled identical untracked canonical task safely | Fast-forward to `edec207`; no task state lost |
| 2026-10-05 | Read mandatory policies, Worker role, registry/project/state/control room, schemas, JOB-00/01 task/evidence/review/checkpoint and JOB-02 | Bootstrap/prerequisite gate PASS |
| 2026-10-05 | Attempted read-only target `git ls-remote` | Git credential injection unavailable; no target checkout/write |
| 2026-10-05 | Read exact qualified TANGRA-DOCS ref through authenticated GitHub connector | S01-S04 verified; fresh runtime not accessed |
| 2026-10-05 | Reused independently reviewed WORKSHOP geometry/range forensics | No duplicate component investigation; incomplete claims retained as NOT VERIFIED |
| 2026-10-05 | Ran deterministic sensitivity script | JSON generated; no Monte Carlo or invented distributions |
| 2026-10-05 | Re-ran script twice and compared hashes | deterministic/reproducible PASS |
| 2026-10-05 | Wrote only JOB-02 evidence/calculation/review-request and task status | WORKSHOP-only mutation; target unchanged |

## 12. Acceptance self-check

| Criterion | Worker result |
|---|---|
| Numerical provenance | PASS at Worker stage; synthetic grids explicit |
| Domains/frames explicit | PASS |
| Independent truth discipline | PASS; one point bounded, estimator outputs not truth |
| Range not promoted to world | PASS |
| Reproducible, distribution-free calculation | PASS |
| Missing transform/extrinsic/pose/time visible | PASS |
| Minimum experiments + falsification | PASS |
| Protected/read-only scope | PASS |
| Independent review | REQUESTED / NOT YET COMPLETE |

## Stop

`REVIEW_REQUIRED`. Independent Reviewer must re-run the script, independently recompute sampled values, inspect source provenance and challenge whether any result exceeds the available evidence.
