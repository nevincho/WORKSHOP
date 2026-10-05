# TANGRA-RESEARCH-LAB-01 — Worker Evidence

TASK_ID: TANGRA-RESEARCH-LAB-01

ROLE: WORKER / READ-ONLY RESEARCH

STATUS: REVIEW_REQUIRED

DATE: 2026-10-05

TANGRA_CHANGED: NO

PI_OR_RUNTIME_ACCESSED: NO

CODEX_USED: NO

## Result

The qualified repository refs support a current architecture/evidence-boundary baseline, but they do not establish fresh runtime state. The current production description is a protected HQ-authoritative perception chain with HOROS downstream/non-authoritative, a separate zero-authority Cognitive service, telemetry paths that remain distinct from disabled command/actuation paths, and a dedicated Flight Controller boundary. Evidence maturity is uneven: repository/current-state records are extensive; physical geometry/range evidence is bounded; time/freshness observability is incomplete; communications have physical neutral-message evidence with loss/latency and recovery-isolation limitations; and integrated flight remains unqualified.

This artifact does not decide H1-H9, propose implementation, perform external research, run a quantitative experiment, or access production.

## Source authority and qualification boundary

| Source | Exact ref | Role used here | Boundary |
|---|---|---|---|
| `nevincho/WORKSHOP` | `main@4690ec2` at Worker start | Coordination, reviewed evidence, task lifecycle | Not TANGRA implementation authority. |
| `nevincho/TANGRA-DOCS` | `main@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba` | Canonical current architecture/documentation and retained runtime/validation records | Repository records are not a fresh Pi observation. |
| `nevincho/TANGRA-CL` | `main@7a720af7fe5b4321b1ba47c8d2be58c815677fd7` | Current Cognitive architecture/integration record | Chronological sections include superseded states; latest reconciliation governs current wording. |
| `nevincho/TANGRA-2.0` | `main@7fb29d1b88b4e40ba993f68d9dac4d37405a41cb` | Separate future/engineering and validation repository | Not current production authority; its architecture must not be merged into the current chain. |

Direct HTTPS clone was unavailable because this execution environment had no Git credential injection for private repositories. Exact-ref content was therefore read through the authenticated GitHub repository connector. The connector returned the exact requested refs and file blob identities. No local target checkout was created and no target write path was used.

Fresh production source commit/tree identity: **NOT VERIFIED**.

Fresh production runtime state on 2026-10-05 during this Worker run: **NOT VERIFIED**.

## 1. Current subsystem and interface map

Every row is a current repository claim at the cited ref unless explicitly marked retained evidence or proposed.

| From / owner | Interface / edge | To / owner | Authority and state | Exact source |
|---|---|---|---|---|
| HQ IMX477 / Mission service | image frames | Hailo detector / Mission | HQ is authoritative detection source | TANGRA-DOCS `CURRENT_SYSTEM.md`; `CURRENT_BASELINE.md` |
| WIDE IMX708 / Mission | secondary latest-value observation | HOROS spatial processing | Secondary only; bounded latest-value worker; stale `>0.5 s` rejected in dated development evidence | TANGRA-DOCS `CURRENT_SYSTEM.md`; `REPORTS/HOROS_DUAL_CAMERA_LOCAL_MAPPING_2026-09-06.md` |
| Hailo detector | detections / class+bbox | NanoTracker | Detector supplies measurements; no independent physical class truth implied | TANGRA-DOCS `CURRENT_SYSTEM.md`; `REPORTS/DRONEGUARD_PYTHON_MODULE_MAP_2026-09-06.md` |
| NanoTracker | transient track observations/IDs | NumPy tracker labelled CA | Nano owns association; Kalman does not replace Nano IDs in the candidate study | TANGRA-DOCS `CURRENT_SYSTEM.md`; `REPORTS/TANGRA_TRUE_CA_VALIDATION_REPORT_20261004.md` |
| Current production NumPy tracker | image-space state / dropout prediction | CurrentTargetManager | Current repository calls it CA, but the 2026-10-04 forensic report describes the captured production state as CV `[p,v]` and no normal predict-before-update | TANGRA-DOCS `CURRENT_BASELINE.md`; `REPORTS/TANGRA_TRUE_CA_VALIDATION_REPORT_20261004.md` |
| CurrentTargetManager | persistent mission target identity | range/projection and HOROS | CurrentTarget semantics are protected; Nano IDs remain diagnostic/temporary | TANGRA-DOCS `CURRENT_SYSTEM.md`; `REPORTS/HOROS_DUAL_CAMERA_LOCAL_MAPPING_2026-09-06.md` |
| target profile + bbox + calibration | `MONOCULAR_CLASS_SIZE` range and uncertainty | LOS/range enrichment | Functional current range path; one bounded 4.36 m physical point, not a full-range qualification | TANGRA-DOCS `REPORTS/HQ_POC_RANGE_AND_MULTI_OBJECT_PHYSICAL_EVIDENCE_20260915.md`; `REPORTS/HOROS_DUAL_CAMERA_LOCAL_MAPPING_2026-09-06.md` |
| camera projection | bearing/LOS | HOROS | Metric interpretation depends on profile/calibration/transform provenance | TANGRA-DOCS `REPORTS/TANGRA_CALIBRATION_AND_HOROS_VALIDATION_2026-09-05.md` |
| tracking + range/projection | target spatial inputs | HOROS runtime | HOROS is downstream, fail-open, shadow/non-authoritative relative to tracking; physical metric promotion open | TANGRA-DOCS `CURRENT_SYSTEM.md`; `CURRENT_BASELINE.md` |
| HOROS | spatial state/history/prediction/uncertainty | telemetry/API/Dashboard 3D | Dated implementation/regression evidence exists; live target-dependent Dashboard fields lacked stimulus in that gate | TANGRA-DOCS `REPORTS/HOROS_DUAL_CAMERA_LOCAL_MAPPING_2026-09-06.md` |
| Mission service | `TANGRA_MISSION_TELEMETRY_V1` JSON+ACK over Unix socket | Cognitive service | Latest-wins ordinary telemetry; lossless mission-end transition; `mission_active` is lifecycle truth | TANGRA-DOCS `CURRENT_SYSTEM.md`; TANGRA-CL `integration/CURRENT_INTEGRATION_STATE.md` |
| Cognitive service | COG-16/18/19/20/22/26 + persistence | report/status/audit | Separate service; observer/record-only during mission; deep work in standby; authority `NONE`, operational authority `[]` | TANGRA-CL `README.md`; `architecture/COGNITIVE_LAYER_ARCHITECTURE.md`; `integration/SHADOW_INTEGRATION_CONTRACT.md` |
| Mission telemetry API `127.0.0.1:8080` | telemetry read | LoRa shadow sender | Live telemetry sender is separate; configured USB device absent at 2026-09-22 snapshot | TANGRA-DOCS `CURRENT_SYSTEM.md`; `CURRENT_BASELINE.md` |
| PC/phone/ground communication | high-level communication | TANGRA Master ESP32 | Master owns routing/ACK/heartbeat, not stabilization | TANGRA-DOCS `ARCHITECTURE/TANGRA_FLIGHT_CONTROL_ARCHITECTURE.md` (**PROPOSED document**) |
| TANGRA Master ESP32 | UART high-level commands | dedicated Flight Controller ESP32 | FC owns stabilization/estimators/PID/mixer/ESC/safety; Pi must not send motor PWM | Same proposed architecture file; newer `CURRENT_SYSTEM.md` says A10 implementation DONE but A11/A12 deferred |
| Flight Controller | motor mixer/ESC output | carrier | Integrated bench/flight validation is not established by the inspected current evidence | TANGRA-DOCS `CURRENT_BASELINE.md`; `TANGRA_PROJECT_STATE_CURRENT.md` |
| TANGRA-2.0 ARKAN/ZAYA/ORON/MENH/HIMORI | future architecture contracts | separate TANGRA 2.0 stack | Proposed/separate engineering architecture, not part of current production baseline | TANGRA-2.0 `TANGRA_2_0/TANGRA_2_0_ARCHITECTURAL_FOUNDATION.md`; component files under `10_ARKAN`…`50_HIMORI` |

### Current topology summary

`HQ → Hailo → NanoTracker → current NumPy tracker → CurrentTargetManager → range/projection → HOROS downstream → telemetry/API/Dashboard`

Parallel bounded paths:

- `WIDE → latest-value/freshness boundary → HOROS`;
- `Mission → versioned IPC → independent Cognitive service → report/status/audit`;
- `Mission telemetry API → LoRa telemetry sender`;
- proposed/high-level carrier control boundary: `Pi/Master → UART high-level request → dedicated FC → ESC`, with FC final safety authority.

## 2. Claim-to-evidence matrix

| ID | Material claim | Classification | Evidence date / maturity | Exact evidence | Limitation |
|---|---|---|---|---|---|
| C01 | Canonical current chain is HQ-authoritative, with WIDE secondary and HOROS downstream/non-authoritative. | REPOSITORY FACT | cutoff 2026-10-04; current docs | TANGRA-DOCS `CURRENT_SYSTEM.md`, `CURRENT_BASELINE.md` | Fresh production tree/runtime not inspected here. |
| C02 | Production service/process split assigns Mission and Cognitive independent systemd ownership. | REPOSITORY FACT based on retained runtime evidence | 2026-09-28 | TANGRA-DOCS `CURRENT_SYSTEM.md`; TANGRA-CL `integration/CURRENT_INTEGRATION_STATE.md` | Not freshly observed. |
| C03 | Cognitive authority is NONE and operational authority empty; Shadow forbids command/flight/target/mission/config/IFF/LoRa authority. | REPOSITORY FACT | current contract plus dated runtime records | TANGRA-CL `architecture/COGNITIVE_LAYER_ARCHITECTURE.md`, `integration/SHADOW_INTEGRATION_CONTRACT.md`, `README.md` | Runtime enforcement today not freshly rechecked. |
| C04 | One physical near-field range point measured 4.36 m and runtime produced 4.366 m. | EXPERIMENT RESULT | 2026-09-15; bounded physical POC | TANGRA-DOCS `REPORTS/HQ_POC_RANGE_AND_MULTI_OBJECT_PHYSICAL_EVIDENCE_20260915.md` | Does not validate range curve, infinity focus, target-size prior, or operational distances. |
| C05 | Two simultaneous confirmed tracks were observed for the bounded F450 insertion. | EXPERIMENT RESULT | 2026-09-15; bounded physical POC | Same report | Does not establish airborne multi-target performance or classification accuracy. |
| C06 | HQ/WIDE intrinsics are provisional; paired capture works; final R/T, known-geometry accuracy and LOCAL_ENU remain open. | EXPERIMENT RESULT + NOT VERIFIED gaps | 2026-09-05 | `REPORTS/TANGRA_CALIBRATION_AND_HOROS_VALIDATION_2026-09-05.md` | Optical state/focus and processing-domain transfer constrain use. |
| C07 | Dated HOROS development evidence reports downstream spatial integration and WIDE latest-only/freshness protection with >25 FPS. | EXPERIMENT RESULT | 2026-09-06 | `REPORTS/HOROS_DUAL_CAMERA_LOCAL_MAPPING_2026-09-06.md` | Dual-camera physical geometry remained non-authoritative; target-dependent live UI stimulus absent. |
| C08 | WORKSHOP HOROS T2-T7 packages have individual final independent PASS reviews for standalone synthetic/host transform, range-fusion, stability, envelope and passive-guidance contracts. T1 sparse-target geometry remains `REVIEW / PASS_WITH_CONDITIONS / TASK1_COMPLETE: NO`; a bounded Worker correction and re-review request exist, but final independent re-review is absent and therefore `NOT VERIFIED`. | SYNTHETIC RESULT / mixed review maturity | 2026-09-08 | WORKSHOP final reviews for `TASK-TANGRA-HOROS-*T2..T7*`; `tasks/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908.md`; `review/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908.md`; `evidence/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908/CORRECTION_20260908.md`; `review/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908-REREVIEW_REQUEST.md` | Production transform, physical metric status, Pi E2E and guidance runtime remain NOT VERIFIED. T1 correction must not be treated as independently accepted until a final re-review verdict exists. |
| C09 | The 2026-10-04 genuine-CA candidate passed math/API checks but failed candidate prediction suitability; production unchanged. | SYNTHETIC RESULT / EXPERIMENT RESULT | 2026-10-04 | `REPORTS/TANGRA_TRUE_CA_VALIDATION_REPORT_20261004.md` | No usable real detector replay or independent real-camera truth; synthetic paths exceeded some physical view bounds. |
| C10 | Current production tracker naming is semantically inconsistent with the forensic state model. | REPOSITORY FACT (conflict) | 2026-10-04 | `CURRENT_SYSTEM.md`/`CURRENT_BASELINE.md` call it NumPy CA; true-CA report identifies captured production state `[p,v]` as `CURRENT_CV` | Requires JOB-04 terminology/model qualification; no rename/change proposed here. |
| C11 | Static-target session ran 3 h 36 m 30 s, zero restarts; five late FPS samples averaged 41.10. | EXPERIMENT RESULT (operator-supplied retained runtime evidence) | 2026-10-05 | `TESTS/TANGRA_STATIC_TARGET_RUNTIME_TRACKING_20261005.md` | Not full-session distribution; no fresh Worker runtime access. |
| C12 | Same-ID first-to-last span 6314.31 s is not uninterrupted same-target lifetime. | REPOSITORY FACT about evidence boundary | 2026-10-05 | Same runtime snapshot | Frame-by-frame identity continuity absent. |
| C13 | Current-session capture persistence, physical detector identity, airborne performance and uninterrupted tracking remain unverified. | NOT VERIFIED | 2026-10-05 boundary | Same runtime snapshot | Requires independent session-specific evidence. |
| C14 | Cognitive 2-hour workload passed 1018/1018, including 763 model operations, with no observed restart/fatal error. | EXPERIMENT RESULT | 2026-09-27 | TANGRA-CL `integration/COGNITIVE_ENDURANCE_VALIDATION_20260927.md` | Tested Shadow workload only; manual/non-continuous thermals; not longer-term proof. |
| C15 | Cognitive coexistence did not establish active-tracking A/B coexistence. | EXPERIMENT RESULT / NOT VERIFIED | 2026-09-27 | TANGRA-CL `integration/COGNITIVE_MISSION_COEXISTENCE_20260927.md` | `active_trackers=0`, no target stimulus, cadence/frame age unavailable. |
| C16 | Cognitive V1 core was independently accepted with limitations; OBS work is repository-only/deferred by Mission freeze. | REPOSITORY FACT (reviewed coordination evidence) | 2026-10-04 | WORKSHOP `review/TANGRA-COG-V1-C12.md` | Old COG-26 fixture drift produced 33 failures; classified harness drift, not fresh production defect. |
| C17 | Bulgarian Cognitive quality is not qualified. | NOT VERIFIED / failed methodology execution | 2026-10-04 | WORKSHOP `review/TANGRA-COG-V1-C13.md` | 24-case live model run and human ratings not executed; no model defect established. |
| C18 | C14 longitudinal result is repository/simulation-only and found one repaired persistence load-order defect plus contract limitations. | SYNTHETIC RESULT / REPOSITORY FACT | 2026-10-04 | WORKSHOP `review/TANGRA-COG-V1-C14.md` | No live production execution; no durable disposition state/expiry policy/ref integrity. |
| C19 | Later bridge cumulative 317-test regression was not executed; 317/317 must not be claimed for that gate. | REPOSITORY FACT (reviewed coordination evidence) | 2026-09-20 | WORKSHOP `review/TANGRA-COG-BRIDGE-01.md`; TANGRA-CL `integration/CURRENT_INTEGRATION_STATE.md` | Historical earlier pre-Unit11 317/317 is a different gate. |
| C20 | Physical neutral communication tests showed non-zero loss and ~1.1 s observed ACK latency; six-node loss-isolation test failed during Node 4 disconnect. | EXPERIMENT RESULT | 2026-07-13 | TANGRA-DOCS `REPORTS/COMMUNICATION_STACK_VALIDATION_EVIDENCE.md` | Test could not isolate ESP-NOW RF loss from host/serial observation congestion; no actuation. |
| C21 | Command send/IFF/readiness/real command/actuation remain OFF in current baseline. | REPOSITORY FACT | cutoff 2026-10-04 | `CURRENT_SYSTEM.md`, `CURRENT_BASELINE.md` | Fresh hardware state not observed. |
| C22 | Dedicated Flight Controller implementation A10 is recorded DONE, while bench A11 and integrated flight A12 are deferred. | REPOSITORY FACT from current baseline | 2026-10-03 reconciliation | `CURRENT_SYSTEM.md`, `CURRENT_BASELINE.md` | Underlying firmware/source/ref is not identified in inspected current entry documents. |
| C23 | Full integrated flight stabilization/ESC/flight is not verified in the older current project-state snapshot. | NOT VERIFIED | cutoff 2026-09-24 | `TANGRA_PROJECT_STATE_CURRENT.md` | Consistent with A11/A12 deferred, but A10 implementation is newer. |
| C24 | Current telemetry surfaces do not expose all required HQ/WIDE cadence and explicit frame-age quantities. | REPOSITORY FACT about known observability gap | 2026-09-27 | TANGRA-CL coexistence report; TANGRA-DOCS current baseline | Exact source timestamps/time domains remain to be inventoried by JOB-03. |
| C25 | TANGRA-2.0 is a separate architecture/validation line and must not be treated as current production. | REPOSITORY FACT / authority classification | exact ref 2026-10-05 inspection | TANGRA-2.0 foundation/component documents; Scout authority snapshot | Active replay reports qualify their own stack only. |

## 3. Protected authority matrix

| Domain | Current owner / authority | May consume/propose | Explicitly non-authoritative / forbidden | Evidence |
|---|---|---|---|---|
| AI detection | HQ + Hailo in Mission service | WIDE may provide secondary spatial/environment evidence | WIDE cannot confirm/replace authoritative target chain | TANGRA-DOCS current files |
| Track association | NanoTracker | current estimator consumes observations | HOROS/Cognitive do not replace Nano association | Current files; module map |
| Image-state estimation | Current production NumPy tracker | genuine-CA candidate is research only | Candidate failed suitability; no production promotion | true-CA report |
| Mission target identity | CurrentTargetManager | HOROS consumes stronger identity before Nano fallback | HOROS must not invent/replace mission identity | HOROS dual-camera report |
| Range | Existing range estimator/profile/calibration path | HOROS consumes published LOS/range with provenance | HOROS standalone contracts do not become production metric authority | physical POC; WORKSHOP T3/T4 reviews |
| Spatial/world state | HOROS downstream | telemetry/Dashboard/guidance may consume qualified outputs | Non-authoritative relative to tracking; fail-open; physical metric promotion gated | current files; HOROS reports |
| Mission lifecycle | Mission service `mission_active` | Cognitive consumes IPC | `swarm_state` is context, not lifecycle truth | current system; CL current integration |
| Cognitive interpretation | independent Cognitive service | structured proposals/reports/status/audit | No command, flight, target, mission, config, IFF/readiness or LoRa authority | CL architecture/Shadow contract |
| Communications routing | TANGRA Master ESP32 (architectural owner) | high-level packets/ACK/heartbeat | Must not stabilize aircraft | proposed flight architecture |
| Stabilization/ESC/safety | dedicated Flight Controller ESP32 | accepts high-level requests through UART | Pi and Master must not send direct motor PWM or own stabilization | proposed flight architecture; current A10/A11/A12 reconciliation |
| Promotion | Human/defined promotion gates | reviewed evidence informs decision | PASS does not authorize production or actuation | WORKSHOP policies |

## 4. Contradiction, staleness and source-gap register

| ID | Type | Sources | Finding | Disposition for later job |
|---|---|---|---|---|
| G01 | MODEL/NAMING DRIFT | current docs vs true-CA report | `NumPy CA Kalman` label conflicts with captured `[p,v]` current CV dynamics and missing normal prediction step. | JOB-04 must define model semantics from exact source before comparing estimators. Do not infer defect from label alone. |
| G02 | STALE DOCUMENT | `ARCHITECTURE/TANGRA_FLIGHT_CONTROL_ARCHITECTURE.md` vs current docs | Flight file says PROPOSED/no implementation; newer current baseline says A10 implementation DONE, A11/A12 deferred. | JOB-06 must locate exact A10 firmware/ref and treat the architecture file as boundary/design, not current implementation status. |
| G03 | CHRONOLOGICAL SUPERSESSION | TANGRA-CL `CURRENT_INTEGRATION_STATE.md` | Same file contains stub-only blocker, per-inference model-exit topology, persistent server topology and later independent-service topology. | Use latest dated reconciliation/current pointer; preserve older passages only as historical evidence. |
| G04 | SOURCE GAP | current A10 claim | Exact FC firmware repository, commit, build/test evidence not named in inspected current entry files. | JOB-06 prerequisite inventory. A10 existence is repository-recorded; exact implementation remains NOT VERIFIED here. |
| G05 | SOURCE GAP | production architecture claims | Exact current production repository/tree/commit is absent from Worker access; docs contain dated snapshots and selected file hashes only. | All specialist jobs must distinguish repository claim from source-level verification. |
| G06 | GEOMETRY GAP | calibration/HOROS reports | Final HQ↔WIDE R/T, known-geometry metric accuracy, operational LOCAL_ENU/carrier pose and long-range accuracy remain open. | JOB-02 owns measured terms/error budget; JOB-05 consumes only reviewed outcomes. |
| G07 | PROCESSING-DOMAIN GAP | physical POC range report | Earlier attempted global scale correction used incompatible bbox domains and was rolled back. | JOB-02 must inventory actual live 640×640 bbox/crop/resize transform and avoid cross-domain calibration claims. |
| G08 | TIME/OBSERVABILITY GAP | Cognitive coexistence/current telemetry | HQ/WIDE cadence and explicit frame age were not exposed; source timestamp/timebase consistency is incomplete. | JOB-03 first inventories timestamp producers/domains and freshness consumers. |
| G09 | VALIDATION GAP | static-target snapshot | First-to-last same-ID span is not uninterrupted identity; current-session capture did not produce verified persistence evidence. | JOB-04 must define continuity truth; do not reuse span as tracker-lifetime truth. |
| G10 | COMMUNICATION FAILURE EVIDENCE | comm validation report | Node-4 disconnect window coincided with severe loss across other nodes; cause unknown. | JOB-06 must preserve this as failure-isolation evidence and inspect whether later tests supersede it. |
| G11 | COMMUNICATION SOURCE GAP | comm report/current baseline | Historical standalone verification record missing; current LoRa serial device absent at 2026-09-22 snapshot; source binding issues exist in prior campaign. | JOB-06 must map exact active firmware/source/transport and separate ESP-NOW bench evidence from LoRa telemetry. |
| G12 | COGNITIVE QUALIFICATION GAP | C13 review | Bulgarian routing PASS does not establish Bulgarian response quality; live 24-case execution absent. | JOB-07 may cite the gap but must not rerun/expand C13 without separate authorization. |
| G13 | COGNITIVE CONTRACT LIMITATION | C14 review | No durable COG-30 disposition state, no expiry/decay, no Experience-ref integrity; COG-26 is stateless assembler. | JOB-07 assesses cross-system safety impact, not implementation. |
| G14 | REGRESSION ACCOUNTING | bridge/current integration | Historical 317/317 and later unexecuted 317 suite are different gates. | Never aggregate them into a current cumulative PASS. |
| G15 | FUTURE/CURRENT CONFLATION RISK | TANGRA-2.0 vs TANGRA-DOCS | TANGRA-2.0 components and replay results describe a separate future/engineering stack. | Exclude from current-system claims except as explicitly labelled proposed/experimental comparison input. |
| G16 | LEGACY/OVERLAP CANDIDATES | module map | `pi_runtime_backend.py`, `pc_dashboard_bridge.py`, `kalman.py`, compatibility `dashboard.py` and other unreferenced modules may overlap/legacy, but dynamic/operator use was not ruled out. | Record as source-level inventory question; no deletion/simplification recommendation until current source/ref is available. |
| G17 | WORKSHOP EVIDENCE-MATURITY GAP | HOROS T1 task/review/correction/re-review request | T1 remains `REVIEW / PASS_WITH_CONDITIONS / TASK1_COMPLETE: NO`. Its bounded Worker correction is present, but no final independent re-review verdict exists. It must not be promoted by association with final-PASS T2-T7 evidence. | JOB-02/JOB-05 may inspect T1 as conditional/unaccepted evidence only; final maturity remains `NOT VERIFIED` until independent re-review. |

## 5. Evidence maturity by research unit

| Unit | Strong reusable evidence | Weak/conflicting/missing evidence | Boundary for next work |
|---|---|---|---|
| JOB-02 physical state | one direct range point; provisional intrinsics; paired-capture timing; explicit failed/rolled-back scale attempt | operational bbox transform, final extrinsics, pose/LOCAL_ENU, target-size distributions, multiple distances/angles/targets | Deterministic bounded sensitivity first; Monte Carlo only if distributions/correlation evidence exists. |
| JOB-03 temporal/performance | WIDE latest-only semantics and stale rejection; selected FPS/latency/endurance records | end-to-end timestamp domains, observation age per stage, jitter/dropout association, full-session distributions | Inventory clocks/IDs/queues before modelling. |
| JOB-04 tracking/prediction | true-CA synthetic campaign; static-session records and explicit limits | authentic replay with independent truth; production model semantics/naming; identity continuity ground truth | Depends on JOB-03 timing definitions; do not rerun synthetic CA work. |
| JOB-05 HOROS/Fusion | current downstream authority; dated operational/regression evidence; final-reviewed standalone T2-T7 contracts; conditional T1 artifact at incomplete review gate | T1 final independent re-review; production transform/metric promotion; provenance continuity in current exact source; physical prediction truth | Depends on reviewed JOB-02 and JOB-03. T1 must remain conditional/NOT VERIFIED unless its separate re-review closes. |
| JOB-06 comm/flight | neutral physical six-node tests; ACK integrity; architectural authority split; current A10/A11/A12 status | exact A10 source/ref; recovery isolation root cause; present LoRa device/source binding; integrated bench/flight | Can start after JOB-01 review; no commands/actuation. |
| JOB-07 Cognitive | extensive reviewed C12/C14/bridge evidence, service split, authority contracts, endurance | C13 live BG quality, active-tracking coexistence A/B, fresh runtime, cross-service stale data semantics | Can start after JOB-01 review; reuse completed units and preserve zero authority. |

## 6. Dependency recommendation for JOB-02..07

1. **JOB-02 and JOB-03 may proceed independently after JOB-01 Reviewer PASS.** JOB-02 must declare time/pose terms as missing rather than waiting for JOB-03; JOB-03 must not assume metric truth.
2. **JOB-04 remains dependent on JOB-03.** Fair estimator comparison requires exact timestamp/horizon/dropout semantics and source identity. JOB-02 is informative but not a hard prerequisite for image-space comparison.
3. **JOB-05 remains dependent on both JOB-02 and JOB-03.** It must consume qualified physical-state and freshness/provenance results instead of recreating them.
4. **JOB-06 may proceed after JOB-01 Reviewer PASS, independent of JOB-02/03.** Its first gate is exact source/ref and interface ownership inventory, especially A10 and the ESP-NOW/LoRa distinction.
5. **JOB-07 may proceed after JOB-01 Reviewer PASS, independent of JOB-02/03.** It must reuse C12/C14/Bridge reviews, preserve C13 as incomplete live qualification, and inspect only cross-service freshness/resource/authority boundaries.
6. No JOB-02..07 canonical task is created by this Worker. Control Room remains one-task-at-a-time.

## 7. Existing reviewed evidence reused

- WORKSHOP final independent reviews were reused for HOROS T2-T7. HOROS T1 was reused only as conditional evidence: canonical state is `REVIEW / PASS_WITH_CONDITIONS / TASK1_COMPLETE: NO`; its Worker correction exists, but final independent re-review is absent / `NOT VERIFIED`. No geometry/range/fusion experiment was repeated.
- WORKSHOP C12, C13, C14 and Cognitive Bridge reviews were reused; no Cognitive implementation or live model execution was repeated.
- The multi-rate research review was reused only as a current evidence-boundary warning: cadence changes remain unqualified and latest-frame semantics matter; no optimization recommendation was produced.
- Dated TANGRA-DOCS runtime/physical reports were treated as retained evidence for their dates, not current Worker observation.

## 8. Acceptance check

| Criterion | Worker result |
|---|---|
| Material current claims cite exact repository/ref/path or NOT VERIFIED | PASS at Worker stage |
| Repository facts separated from retained/fresh runtime | PASS; fresh runtime explicitly NOT VERIFIED |
| Current vs proposed/future separated | PASS; TANGRA-2.0 and proposed FC document isolated |
| Authority boundaries explicit | PASS |
| Conflicts/staleness/source gaps registered | PASS |
| Existing reviewed work reused | PASS |
| Dependencies narrowed without executing later jobs | PASS |
| Target read-only/hygiene | PASS at Worker stage |
| Independent Reviewer | REQUESTED / NOT YET COMPLETE |

## 9. Execution ledger

| UTC | Action | Result / provenance |
|---|---|---|
| 2026-10-05 | Read WORKSHOP `README.md`, `AGENTS.md`, applicable policies, Worker role, registry, TANGRA profile, state/control-room, schemas, JOB-00 task/evidence/handoff, JOB-01 task | Pre-execution gate satisfied; REPOSITORY FACT |
| 2026-10-05 | Verified WORKSHOP `main@4690ec2`; confirmed JOB-01 absent evidence/review and status READY | Task not duplicated; REPOSITORY FACT |
| 2026-10-05 | Attempted read-only HTTPS clone of `TANGRA-DOCS` | Failed before checkout: no Git username/credential injection. No target file created. Environment/access fact. |
| 2026-10-05 | Used authenticated GitHub connector to read exact refs and recursive trees for TANGRA-DOCS, TANGRA-CL, TANGRA-2.0 | Exact requested commit SHAs returned; REPOSITORY FACT |
| 2026-10-05 | Read current entry files, physical/calibration/tracker/runtime/communications/HOROS/flight reports, Cognitive architecture/current integration/coexistence/endurance/contracts | Claim/source matrix generated; no external research |
| 2026-10-05 | Read relevant WORKSHOP evidence/reviews for HOROS T1-T7, multi-rate, Cognitive Bridge, C12-C14 | T2-T7 final reviews reused; T1 retained at incomplete review gate; REPOSITORY FACT / SYNTHETIC RESULT as labelled |
| 2026-10-05 | Applied bounded rework from independent JOB-01 review commit `282280c` | Corrected only T1 evidence maturity and dependent wording; no specialist rerun or target change |
| 2026-10-05 | Wrote only `tasks/TANGRA-RESEARCH-LAB-01.md`, this evidence, and Reviewer request | WORKSHOP-only mutation |

Commands/retrieval operations included `rg --files`, `sed`, `git status`, `git log`, one failed read-only `git clone`, GitHub exact-ref tree reads, exact-ref file reads and local WORKSHOP review reads. No Python execution, simulation, service command, device access, flash, network command to TANGRA runtime, or target write occurred.

## 10. Protected-scope and hygiene check

- TANGRA repositories/runtime modified: **NO**.
- Production/Pi accessed: **NO**.
- Commands/flight/flash/actuation: **NO**.
- External literature research: **NO**.
- Quantitative experiment: **NO**.
- H1-H9 answered: **NO**.
- Disposable target checkout retained: **NO**; clone failed before creation.
- WORKSHOP artifacts retained: one canonical Worker evidence file and one Reviewer request; no duplicate draft/report.

## Stop

`REVIEW_REQUIRED`. Independent Reviewer must inspect this actual artifact, sample every subsystem row against exact-ref sources, verify provenance separation/conflict handling and confirm repository hygiene before Control Room advances.
