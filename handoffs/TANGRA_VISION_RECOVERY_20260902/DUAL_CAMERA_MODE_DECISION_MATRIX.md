# DUAL CAMERA MODE DECISION MATRIX

TASK_ID: `TASK-059`

## Decision principle

Do not choose dual-camera architecture by feature count. Choose the smallest mode that delivers demonstrated functional value while preserving HQ behavior and passing the owner performance gate.

`FUNCTIONAL PASS WITHOUT PERFORMANCE PASS = ARCHITECTURE FAIL`.

## Candidate modes

| Dimension | MODE A — FULL DUAL VISION | MODE B — ASYMMETRIC DUAL | MODE C — HQ FALLBACK |
|---|---|---|---|
| WIDE role | detection + authoritative/local tracking; may contribute to cross-camera target state | watch/acquisition/event sensing/ROI/sector hint and/or calibrated geometric observation; authoritative WIDE tracker not required | inactive / unavailable to Vision authority |
| HQ role | detection + tracking; authority relationship must be explicitly defined | authoritative detection, NanoTracker/CURRENT_TARGET, CA Kalman target state | sole authoritative detection/tracking/CA path |
| Required cross-camera association | mandatory for any merged target authority | required only for WIDE observation to influence HQ target/geometry; can remain advisory until confidence proven | none |
| Hailo cost | highest: second camera inference at useful cadence plus possible tracker cost | bounded by chosen WIDE acquisition/inference cadence; can decimate/adapt if justified | lowest among three |
| CPU/RAM/copy cost | highest | medium, tunable | baseline control |
| Functional upside | maximum FOV coverage and potential independent WIDE track continuity | early acquisition/wide awareness with protected telephoto tracking; supports future geometry without duplicating full tracker | maximum preservation, simplest failure isolation |
| Main risk | compute/latency contention, association ambiguity, duplicate authority, performance gate failure | WIDE advisory signal quality may be intermittent; association/calibration still required for geometry | no wide-area acquisition benefit; no dual geometry |
| Calibration dependency for detection | camera configuration yes; metric calibration not required for basic detection | same | HQ detection can operate without completed metric calibration if historical behavior preserved |
| Calibration dependency for metric 3D | full intrinsics/extrinsics/time association required | full intrinsics/extrinsics/time association required for geometric contribution | HQ monocular metric chain still requires physical calibration for accuracy claims |
| HQ fallback independence | must be designed explicitly and tested | naturally compatible but still must be tested | inherent |
| Promotion bar | highest | high but more achievable | mandatory retained mode, not a candidate that can be removed |

## Mandatory common prerequisites

Before comparing A/B/C:

1. Current authoritative implementation trace is reconciled.
2. Protected HQ snapshot/rollback exists.
3. HQ-only matched performance baseline is measured with labeled FPS metrics.
4. WIDE camera identity, source mode and preprocessing are known.
5. Current raw→accepted WIDE divergence is reproduced and understood enough that a mode comparison is meaningful.
6. No candidate relies on HOROS implementation to pass Vision acceptance.
7. CA mathematics remains unchanged unless a separate evidence-backed task later authorizes it.

## Objective experiment criteria

### Functional coverage

Measure with matched scenes/fixtures:

- first-detection/acquisition time by camera;
- raw/accepted detection count and precision evidence where ground truth exists;
- target continuity / loss / reacquisition;
- field-of-view coverage and sector acquisition benefit;
- cross-camera association correctness where used;
- target-state freshness and age;
- false-positive/incorrect-association burden;
- HQ performance/quality unchanged versus Mode C.

A WIDE path that increases detections but cannot support correct acceptance/association does not justify authority.

### Performance

For each mode report both processing-loop/pre-sleep and true end-to-end throughput, plus stage latency, CPU, RSS, temperature/throttling and Hailo scheduling.

Owner gate: normal tracking `<25 FPS = FAIL` once metric semantics are explicitly bound. No unlabeled FPS acceptance.

Mode A is rejected if it breaches the gate or causes unacceptable HQ freshness/latency even when aggregate FPS appears adequate.

Mode B may use a lower WIDE cadence than HQ only if the cadence is declared, its acquisition benefit remains meaningful and no stale WIDE observation is presented as current.

### Stability

- no monotonic object/queue/RSS growth beyond justified bounded cache behavior;
- no Hailo ownership/release failures;
- clean OFF→STANDBY lifecycle;
- no duplicate camera/worker/process ownership;
- thermal behavior within matched HQ-control envelope.

### Authority and safety

- HQ-only operation works when WIDE is disabled/unavailable.
- WIDE failure cannot block HQ startup/tracking.
- cross-camera observations have explicit source/time provenance.
- no WIDE advisory state can silently overwrite authoritative HQ target state without a validated policy.

## Decision scoring

Use a gate-first decision, not weighted averaging:

### Gate 1 — HQ preservation

If HQ physical/replay regression occurs: **REJECT candidate / revert**.

### Gate 2 — WIDE functional value

If WIDE adds no repeatable acquisition/coverage/geometric value: do not pay compute cost. Prefer Mode C.

### Gate 3 — Performance

If normal tracking FPS fails owner gate, or latency/freshness/resource stability fails: reject that candidate. A high feature score cannot compensate.

### Gate 4 — Association/calibration validity

If the candidate depends on cross-camera geometry/authority and association/calibration prerequisites are absent: keep that functionality advisory/offline; do not promote it.

### Final choice

- Choose **Mode A** only if it passes all gates and demonstrates a material benefit over Mode B that requires a WIDE authoritative tracker.
- Choose **Mode B** if wide acquisition/observation adds value while HQ remains the best authoritative tracking path and Mode A’s additional tracker authority is unnecessary or too expensive.
- Choose **Mode C** whenever dual benefits are unproven, performance fails, WIDE is unavailable, or as operational fallback in all cases.

## Recommended evaluation order

`Mode C baseline → WIDE capture-only → WIDE preprocess → WIDE inference shadow → Mode B → Mode A only if still justified`.

This order isolates cost and prevents full-dual complexity from hiding the actual first divergence.

## 3D boundary

A calibrated WIDE camera may remain valuable in Mode B as a geometric observation source. This does not imply stereo depth will be accurate at long range. With a 35.6 mm physical baseline, useful disparity at operational ranges must be measured/derived from calibrated intrinsics and validated against physical truth; baseline length alone is not an accuracy claim.
