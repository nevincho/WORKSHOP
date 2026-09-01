# TANGRA — HOROS / LOCAL 3D / MISSION REPLAY

STATUS: READY_FOR_CODEX_REVIEW

## Covered task IDs / campaign tasks
- `tasks/HOROS_3D_CAMPAIGN.md`
- repository-side implementation phases A–F as bounded by the dedicated campaign specification.

## Exact objective
Reconcile the reviewed isolated HOROS / Local 3D / persistent sparse map / Mission Recorder / 3D Tactical Replay / diagnostics package against the authoritative active TANGRA source and runtime, reuse existing validated components where available, eliminate duplication, adapt interfaces, integrate only in shadow/off-by-default mode, and perform deterministic plus bounded runtime validation.

## Architecture summary
Three separated systems are preserved:
1. HOROS live peripheral spatial evidence — advisory/passive only.
2. Persistent sparse local 3D map — optional/fail-open context and constraints.
3. Mission Recorder / Tactical Replay / diagnostics — asynchronous observer with operational authority NONE.

Protected baseline authority remains with existing detector/Hailo, NanoTracker, image-space CA Kalman, CURRENT_TARGET and command/actuation paths.

## Reviewed target artifacts
Repository: `nevincho/TANGRA-DOCS`
Branch: `workshop-horos-3d`
Validated campaign head: `ff778dfa3ac052fdb9c48d4eb7a55da371bee622`

Primary package:
- `Workshop/HOROS_3D/implementation/horos3d/__init__.py`
- `Workshop/HOROS_3D/implementation/horos3d/contracts.py`
- `Workshop/HOROS_3D/implementation/horos3d/algorithms.py`
- `Workshop/HOROS_3D/implementation/horos3d/coordinator.py`
- `Workshop/HOROS_3D/implementation/horos3d/mapping.py`
- `Workshop/HOROS_3D/implementation/horos3d/recorder.py`
- `Workshop/HOROS_3D/implementation/horos3d/replay.py`
- `Workshop/HOROS_3D/tests/test_contracts.py`
- `Workshop/HOROS_3D/tests/test_coordinator.py`
- `Workshop/HOROS_3D/tests/test_core_modules.py`
- `Workshop/HOROS_3D/IMPLEMENTATION_MANIFEST.md`
- `Workshop/HOROS_3D/MISSING_CURATED_INPUT.md`

Exact implementation/test blob identities are listed in `IMPLEMENTATION_MANIFEST.md`.

## Verified repository-side state
- Common HOROS contracts/state primitives implemented.
- Timestamp/frame mismatch and stale/unavailable semantics implemented.
- Synthetic pinhole geometry adapter and explicit association contract implemented.
- Fixed-baseline stereo evidence and Hybrid Range Fusion implemented.
- Carrier/world transforms and passive Local3D estimator implemented.
- Persistent bounded sparse map and map-derived constraints implemented.
- Localization-candidate contract implemented.
- HOROS coordinator is off-by-default/fail-open and rejects foreign-target evidence.
- Bounded non-blocking Mission Recorder producer interface and deterministic drop accounting implemented.
- Versioned JSONL replay parsing with corrupt/schema issue isolation implemented.
- Tactical Replay timeline/path/event data model implemented.
- Residual/error-origin/downstream-propagation/retraining-candidate preparation implemented.

## Tests executed/results
`python -m unittest discover -s Workshop/HOROS_3D/tests -q`
Result: 31 PASS / 0 FAIL / 0 ERROR.

`python -m compileall -q Workshop/HOROS_3D/implementation/horos3d`
Result: PASS.

Independent Reviewer verdict: PASS for repository-side scope.

## Remaining NOT VERIFIED
- real HQ/WIDE intrinsics/distortion/extrinsics and camera-to-body transforms;
- physical metric accuracy;
- actual subsystem timestamp/timebase precision;
- active carrier pose schema/uncertainty/update rate;
- compatibility with authoritative detector/tracker/CA-Kalman/projection/range/Fusion/CURRENT_TARGET interfaces;
- runtime recorder event rate/storage budget/persistence location;
- real Dashboard client integration/rendering;
- bounded shadow runtime behavior;
- `HOROS OFF` real baseline equivalence.

## Known assumptions
- All campaign geometry values used by tests are explicitly SYNTHETIC.
- Python standard-library implementation was chosen to minimize dependencies and ease authoritative-source reconciliation.
- Mission record payload is deliberately generic at the campaign boundary because authoritative live schemas were not supplied.
- Dashboard artifact is a data/state model, not a production UI implementation.

## Known defects
No known deterministic-test failures remain. Real integration incompatibilities are NOT VERIFIED rather than assumed absent.

## Intended integration points
Read-only/adaptor boundaries for existing perception/tracker/CA-Kalman/CURRENT_TARGET/projection/range/carrier-state outputs; passive HOROS evidence input to existing Fusion; asynchronous observer taps for Mission Recorder; Dashboard-side mission dataset loading/replay rendering.

Exact authoritative module/file names and signatures MUST be discovered by Codex in the real active TANGRA source. Do not infer them from this package.

## Protected components
DO NOT redesign, replace, rename, move or mutate production detector/Hailo, NanoTracker, existing CA Kalman, CURRENT_TARGET authority, command/actuation logic or validated production runtime/configuration unless separate explicit evidence and human approval require it.

## Acceptance criteria for Codex stage
1. Inspect authoritative active TANGRA source/runtime first.
2. Reuse validated existing functions instead of duplicating them.
3. Reconcile/adapt campaign interfaces to actual source contracts.
4. Keep HOROS isolated/shadow/off-by-default.
5. Run the repository deterministic suite and authoritative regression suite.
6. Run bounded shadow/runtime validation without production promotion.
7. Verify recorder/replay failures cannot affect autonomous critical paths.
8. Verify foreign-target/frame/time mismatch fail safely.
9. Verify `HOROS OFF` preserves baseline behavior.
10. Report all remaining physical/runtime NOT VERIFIED items.
11. Do not promote to production without separate explicit human approval.

## Shadow validation plan
- fingerprint protected baseline before integration;
- integrate only adapters/shadow hooks;
- run baseline with HOROS disabled and compare behavior/performance;
- enable HOROS shadow outputs without granting authority;
- exercise timing/frame/association/range/map degradation cases;
- exercise recorder queue/storage pressure and failure isolation;
- replay recorded mission data client-side/offline;
- confirm diagnostics have no feedback path to live control;
- collect evidence for later physical calibration/metric validation gate.

## Rollback/checkpoint
Pre-campaign target checkpoint: `2d7e0d62aad683811d72688696e69fc2e2911d43`.
Validated repository-side campaign head: `ff778dfa3ac052fdb9c48d4eb7a55da371bee622`.
No runtime side effects exist in this WORKSHOP campaign.

## Explicit non-goals
- no production deployment or promotion;
- no command/actuation change;
- no detector/tracker/Kalman replacement;
- no fabricated physical calibration;
- no claim of physical 3D accuracy from synthetic tests;
- no uncontrolled global point cloud;
- no automatic retraining, parameter mutation or model promotion;
- no automatic replay-to-live correction path.

## Codex execution state
NOT INVOKED. Execution remains human-gated.
