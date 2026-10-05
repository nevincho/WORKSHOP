# TANGRA-RESEARCH-LAB-00 — Scout / Planner Qualification

STATUS: READY_FOR_CONTROL_ROOM
DATE: 2026-10-05
TARGET_CHANGE: NONE
CODEX_USED: NO
PI_OR_PRODUCTION_RUNTIME_ACCESSED: NO

## Routing verdict

The full-system research campaign is justified, but it must not be released as nine simultaneous investigations. Existing evidence is substantial and must be reused; the remaining gaps are cross-system evidence qualification, synchronized physical truth, time/freshness semantics, and current-source traceability rather than a lack of prior component work.

Scout stage is complete. The canonical task is moved from `READY` to `HOLD / READY_FOR_CONTROL_ROOM` because the human-directed campaign policy requires Control Room to accept this qualification and issue one bounded downstream Worker task. No research lane was executed in this Scout task.

The first justified downstream unit is `JOB-01 — Current Architecture and Evidence-Boundary Audit`, defined in `handoffs/TANGRA-RESEARCH-LAB-00.md`.

## Authority snapshot

Repository metadata and current refs were read through the authorized GitHub connection on 2026-10-05.

| Repository | Role established by current evidence | Ref inspected | Qualification boundary |
|---|---|---|---|
| `nevincho/WORKSHOP` | Coordination authority | `main@711edb4bf70e88234a0a17c42a1e032b33e6031e` before this Scout write | Contains policies, task history, evidence, reviews and handoffs; not implementation authority. |
| `nevincho/TANGRA-DOCS` | Canonical architecture/documentation and current-state evidence | `main@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba` | Current documents report production/runtime evidence, but this run did not independently access the Pi or production source tree. |
| `nevincho/TANGRA-CL` | Current Cognitive engineering/integration repository | `main@7a720af7fe5b4321b1ba47c8d2be58c815677fd7` | Contains Cognitive architecture, integration, schemas and runner material. Large imported external trees are references, not TANGRA authority. |
| `nevincho/TANGRA-2.0` | Separate architecture/validation repository with TANGRA 2.0 and Cognitive Pi validation records | `main@7fb29d1b88b4e40ba993f68d9dac4d37405a41cb` | Does not replace the frozen current production chain. Its role must be explicit whenever reused. |

Current Pi/production commit identity is `NOT VERIFIED` in this Scout execution. Repository records may be used as `REPOSITORY FACT` or as dated retained runtime evidence, but this Scout does not convert them into a fresh runtime observation.

## Coordination-state reconciliation

`status/WORKSHOP_STATE.yaml` and `control_room/CURRENT.md` predate the submitted task and still describe the older 2026-08-26 TANGRA hold. Newer authoritative coordination evidence is:

- `projects/TANGRA.md`: bounded TANGRA reactivation for repository-safe campaigns;
- `tasks/TANGRA-RESEARCH-LAB-00.md`: explicit 2026-10-05 authorization for read-only research qualification;
- target repositories above: current October 2026 documentation and Cognitive evidence.

The old state index therefore did not make the task ineligible. Runtime and production modification remain prohibited.

## Current baseline reconstructed for planning only

The following are repository-grounded starting constraints, not conclusions about H1-H9:

- `TANGRA-DOCS/CURRENT_SYSTEM.md` and `CURRENT_BASELINE.md` describe the protected current chain as dual cameras with HQ authoritative, Hailo detection, NanoTracker, current NumPy tracker labelled CA in current documents, CurrentTargetManager, range/projection, and HOROS downstream/shadow/non-authoritative.
- The same current documents record a frozen Mission/perception runtime, Cognitive as a separate service with `authority=NONE` and `operational_authority=[]`, and command/IFF/readiness/actuation intentionally off.
- `REPORTS/TANGRA_TRUE_CA_VALIDATION_REPORT_20261004.md` establishes that the tested genuine-CA candidate passed mathematical/API checks but failed candidate prediction suitability; production was unchanged. It also states that independent real-camera ground truth was unavailable.
- `REPORTS/HQ_POC_RANGE_AND_MULTI_OBJECT_PHYSICAL_EVIDENCE_20260915.md` retains one bounded 4.36 m physical range point producing 4.366 m plus two simultaneous confirmed FPV tracks. It explicitly records HOROS metric evidence as unusable at that checkpoint because transform/calibration authority was not verified.
- `REPORTS/TANGRA_CALIBRATION_AND_HOROS_VALIDATION_2026-09-05.md` records provisional camera intrinsics and paired-capture evidence, while final HQ-WIDE extrinsics, known-geometry metric accuracy, operational LOCAL_ENU and physical prediction accuracy remain open.
- `TESTS/TANGRA_STATIC_TARGET_RUNTIME_TRACKING_20261005.md` is a retained operator-supplied runtime snapshot with 3 h 36 m service continuity and 41.10 FPS mean, but uninterrupted same-target identity, current-session capture success and fresh synchronized physical truth are explicitly not verified.
- `COGNITIVE_V1_FINAL_ACCEPTANCE_20261004.md`, C13 and C14 records establish Cognitive V1 acceptance with limitations, incomplete live Bulgarian-quality qualification, and repository/simulation-only longitudinal qualification respectively.
- Latest TANGRA-DOCS range research promotes carrier-motion parallax only after airborne-carrier-to-airborne-target PoC. It remains not implemented and not validated.

These constraints are sufficient to plan research. They are insufficient to decide the nine hypotheses.

## Existing evidence reuse and gap map

| Lane | Reusable current evidence | Qualification | Remaining bounded need |
|---|---|---|---|
| 1. System Architecture Audit | `CURRENT_SYSTEM.md`, `CURRENT_BASELINE.md`, `PROJECT_STATE.md`; pre-freeze audit; current TANGRA project profile | Reusable as current repository baseline; live implementation tree not independently inspected in this run | Build one claim-to-source/authority/dependency matrix and identify contradictions, stale records and source gaps before specialist work. |
| 2. Perception / Tracking / Estimation | Physical detection/tracking reports; HQ geometry forensics; WIDE-EW-00..04 reviews; true-CA campaign | Strong component evidence; CA candidate failure and real-ground-truth absence must be preserved | Qualify observation identity, association, estimator input/output and genuine replay availability. Do not repeat the completed synthetic CA campaign without a new question. |
| 3. Range / Camera / Physical Geometry | Physical 4.36 m point; provisional intrinsics; HQ range/bbox and 640-geometry forensic reviews; dual-stream architecture decision; HOROS T1-T6 artifacts | Reusable but bounded; final transform/extrinsics and operational envelope remain incomplete | Establish measured parameter bounds and a first-order physical-state error budget. Use parameter sweeps where probability distributions are not evidenced. |
| 4. HOROS / Fusion / World Model | HOROS 3D final review (31 deterministic tests); HOROS T1-T7 reviewed packages; fusion/object-resolver deterministic evidence; canonical world-model document | Repository/simulation behavior is reusable; physical metric promotion and production source binding are not established | Audit actual authority/dataflow, provenance, observability and fail-open semantics against current evidence; no promotion or redesign. |
| 5. Timing / Concurrency / Performance | Long-runtime checkpoints; 2026-09-13 geometry FPS remediation; 2026-10-05 runtime snapshot; multirate research review; Cognitive coexistence evidence | Aggregate performance is reusable; source cadence, explicit frame age and synchronized stage timestamps are incomplete | Model error from age/latency/jitter/dropout and determine which missing timestamps prevent measurement. Optimization is not authorized by research alone. |
| 6. Communications / Flight Interfaces | Communication-stack report; LORA-02/03/05A reviewed packages; LORA-04 source-binding blocker; documented FC architecture; current A10/A11/A12 status | Protocol/simulation and some physical bench evidence are reusable; command/actuation remain off and integrated flight is deferred | Audit interface ownership, ACK timing/loss evidence, source binding, failure isolation and validation prerequisites without sending commands or actuating hardware. |
| 7. Cognitive Layer | TAI-COG-00..28, Cognitive V1 component tasks/reviews, Bridge Pi qualification, C12/C13/C14 records, TANGRA-CL current integration state | Extensive reusable evidence; C13 live quality and C14 live longitudinal gate remain incomplete; zero authority is current policy | Audit cross-service evidence freshness, resource coexistence, failure isolation and claim boundaries. Do not reopen completed COG implementation units. |
| 8. Validation / Scientific Method Red Team | Independent reviews exist per many component tasks; physical and synthetic limitations are often explicit | No single current cross-system scientific-method audit or evidence hierarchy closes the whole chain | Cross-examine whether tests measured their stated objectives, whether prerequisites existed, and whether retained claims exceed evidence. This is a late gate, not the first job. |
| 9. External State-of-the-Art Research | July/August 2026 counter-UAS landscape, sensor research and targeted geometry research | Reusable context but not a current, question-led comparison against qualified internal gaps | Perform targeted primary-source research only after internal questions and comparison dimensions are fixed. Avoid generic market/literature survey duplication. |

## Proposed bounded downstream programme

These are planning labels, not newly created canonical task IDs. Control Room must issue only one canonical task at a time.

| Order | Job | Exact question | Inputs and evidence | Dependencies / gate |
|---:|---|---|---|---|
| 1 | JOB-01 Current Architecture and Evidence-Boundary Audit | What architecture, authority boundaries, interfaces and evidence claims are current at the inspected refs, and where do sources conflict or stop? | Current files from the three target repositories plus relevant WORKSHOP reviews/checkpoints | None beyond this Scout. Read-only Worker, then independent Reviewer. |
| 2 | JOB-02 Physical-State Evidence and Error-Budget Qualification | Which measured parameters support detection-to-world-position claims, what uncertainty terms are missing, and what bounded tests would close them? | JOB-01 matrix; physical POC; calibration/geometry evidence; authentic measurement files if present | JOB-01 PASS. Contains quantitative A and D only within evidenced ranges. |
| 3 | JOB-03 Temporal Integrity and Performance Qualification | How do observation age, stage latency, jitter and dropout affect state freshness and prediction, and which quantities are actually measured? | JOB-01; runtime/performance reports; telemetry schemas/logs; source timestamps if available | JOB-01 PASS. Quantitative B; no optimization change. |
| 4 | JOB-04 Tracking/Prediction Evidence Qualification | Does current evidence support production tracker claims, and is any authentic replay suitable for fair CV/genuine-CA comparison? | JOB-01; true-CA report; tracking records; source/replay identity | JOB-01 plus JOB-03 timing definitions. Reuse prior synthetic campaign; run quantitative C only on authentic replay, otherwise classify the gap. |
| 5 | JOB-05 HOROS/Fusion/World-Model Authority Audit | Does downstream spatial state preserve provenance, observability, time and non-authority from accepted inputs to outputs? | JOB-01; JOB-02/03 findings; reviewed HOROS/Fusion artifacts | JOB-02 and JOB-03 reviewed. Read-only; physical promotion excluded. |
| 6 | JOB-06 Communications and Flight-Interface Readiness Audit | Are ownership, source binding, ACK/retry/failure semantics and deferred bench/flight gates coherent and evidence-backed? | JOB-01; communications evidence; LORA packages/blocker; FC docs/current status | JOB-01 reviewed. No command send, flash, actuation or flight. |
| 7 | JOB-07 Cognitive Cross-System Safety and Evidence Audit | Does the separate Cognitive service consume and report evidence without stale-state, resource, authority or lifecycle leakage? | JOB-01; TANGRA-CL; C12-C14; Pi bridge/coexistence records | JOB-01 reviewed. No live model execution unless separately authorized; completed COG units are not reimplemented. |
| 8 | JOB-08 Targeted External State-of-the-Art Comparison | What primary-source methods directly address the verified internal gaps, and under what assumptions/costs? | Reviewed questions from JOB-02..07; current primary literature/official sources | Internal gap definitions reviewed first. External facts kept separate from TANGRA facts. |
| 9 | JOB-09 Scientific-Method Red Team and Cross-Examination | Which findings survive challenge across prerequisites, ground truth, provenance, independence and test validity? | All reviewed investigation evidence and execution ledgers | JOB-02..08 complete. Reviewer must not author the primary findings. |
| 10 | JOB-10 Campaign Synthesis and Preliminary-Difference Analysis | What is supported, contradicted, insufficient, unnecessary or speculative, and how does that differ from the preliminary Control Room analysis? | JOB-09 verdicts plus the preliminary report as a supplied artifact | Final only. The preliminary report/A01-A16 definitions are not present in WORKSHOP and must be supplied before this job. |

Jobs 02-07 may be re-ordered after JOB-01 only if its dependency matrix proves independence. No job may infer that a missing runtime prerequisite has passed.

## Quantitative routing

| Requested experiment | Route | Evidence rule |
|---|---|---|
| A. Range-error Monte Carlo or parameter sweep | JOB-02 | Use Monte Carlo only if defensible distributions and correlations are evidenced. Otherwise use a deterministic parameter sweep across measured/declared bounds and label it `SYNTHETIC RESULT`. |
| B. Temporal-error modelling | JOB-03 | Separate measured latency/jitter/dropout from hypothetical sensitivity ranges. Preserve timestamp domain and clock-source provenance. |
| C. Identical-observation CV versus genuine-CA replay | JOB-04 | First inventory authentic replay, independent truth and identical coverage. Reuse the completed 2026-10-04 synthetic campaign; do not manufacture a real-replay claim. |
| D. First-order physical-state error budget | JOB-02, consumed by JOB-05 | Include bbox/detection geometry, intrinsics/crop, class-size prior, extrinsics, attitude/pose, timestamp/age and world-frame transform only where definitions exist. Missing terms stay `NOT VERIFIED`. |

## Hypothesis preservation

H1-H9 remain `HYPOTHESIS / NOT ASSESSED BY SCOUT`. No hypothesis is accepted, rejected or ranked by this planning result. In particular:

- H8 cannot be evaluated by A01/A03/A04/A08/A16 identifiers because their definitions and the preliminary report are absent from current WORKSHOP. JOB-02 can still qualify the physical-state programme by evidence domain, but the identifier-level comparison must wait for that artifact.
- H9 requires the completed Red Team and cannot be answered from component PASS counts.

## Provenance and execution ledger contract

Every downstream job must classify each material claim as exactly one of:

`REPOSITORY FACT`, `EXTERNAL FACT`, `EXPERIMENT RESULT`, `SYNTHETIC RESULT`, `ENGINEERING INFERENCE`, `HYPOTHESIS`, or `NOT VERIFIED`.

Each job must append a concise execution ledger containing: task/job identity; role; UTC timestamp; repository and exact ref; source paths; commands or retrieval operations; generated artifacts and hashes where material; tests and the objective they measure; exit/result; provenance class; limitations; protected-scope check; hygiene check; reviewer and verdict. It must record observable actions and evidence, not hidden reasoning.

## Current route limitations

- Direct Pi/production runtime and the exact current production source tree were not available through this repository-safe Scout route. Any claim requiring fresh runtime observation remains gated.
- The current source gap already blocked WIDE-EW-05 and LORA-04 source binding; the research campaign may classify that gap but cannot pretend to trace unavailable symbols.
- Live Cognitive C13 quality and C14 longitudinal production qualification require separately authorized runtime execution.
- Flight/actuation, command send, firmware flashing and airborne validation are outside this research Scout authorization.
- The preliminary Control Room report and A01-A16 definitions are absent from WORKSHOP. This does not block JOB-01, but it blocks the mandatory final difference analysis until supplied.

## Acceptance check

1. Repositories/refs and authority boundaries identified: PASS.
2. H1-H9 preserved as hypotheses: PASS.
3. Nine domains mapped without parallel release: PASS.
4. Quantitative A-D routed conditionally: PASS.
5. Dependencies and sequencing explicit: PASS.
6. Existing work reused; repeat CA/HOROS/Cognitive implementation avoided: PASS.
7. Target repositories/runtime remained read-only: PASS.
8. Codex not created or invoked: PASS.
9. No downstream Worker/Reviewer result manufactured: PASS.
10. Scout evidence persisted: PASS.
11. First bounded handoff prepared: PASS.
12. Missing final-comparison artifact and runtime/source gates recorded precisely: PASS.

## Repository hygiene

Only this consolidated Scout evidence and one current handoff are retained. No temporary target-repository copy, generated dataset, duplicate report, failed variant or disposable execution output was added. Git history remains the rollback mechanism for coordination edits.
