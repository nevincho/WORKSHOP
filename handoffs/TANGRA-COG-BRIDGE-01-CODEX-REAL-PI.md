# TANGRA-COG-BRIDGE-01 — CODEX HANDOFF — REAL PI INTEGRATION AND VALIDATION

STATUS: PREPARED_FOR_HUMAN_RUN
EXECUTION_ROUTE: HUMAN RUNS THIS HANDOFF THROUGH CODEX SEPARATELY
WORKSHOP DOES NOT DISPATCH CODEX

Mode: Token conservation. No long reasoning. No extra architecture discussion. Do the task and report only facts.

## Objective

Integrate and validate the already-qualified Cognitive Bridge candidate on the actual current TANGRA Raspberry Pi runtime without replacing or redesigning the existing production pipeline.

Reviewed source candidate:
- repository: nevincho/TANGRA-2.0
- branch: cognitive-bridge-integration
- commit: bd11d92f396b68de00a0f3636ae49ed8310ce420
- bridge: TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_bridge.py
- bridge blob: 5f4a6346fa70e369452067d9d96f776a84468a64
- qualification: 17/17 PASS
- cumulative 317-test regression: NOT EXECUTED because of WORKSHOP execution-environment acquisition/persistence limits; do not report it as PASS.

Current canonical production evidence says:
- runtime root: /home/khan/ai-drone/tangra
- entry: /home/khan/ai-drone/tangra/main.py
- service: tangra-droneguard-1-0.service
- protected perception/spatial chain: HQ -> Hailo detector -> NanoTracker -> CA Kalman -> current-target/range evidence -> HOROS -> telemetry -> Dashboard
- WIDE is secondary.
- Cognitive authority: NONE.

Treat those as expected state only. VERIFY THE ACTUAL CURRENT PI STATE BEFORE MODIFYING ANYTHING. If actual state materially contradicts the expected state, STOP and report the contradiction; do not force the integration.

## Mandatory control boundary

Cognitive control must remain disabled throughout:
CONTROL_ENABLED=false
AUTHORITY=NONE
operational_authority=[]

Do not activate autonomous Cognitive control.
Do not grant Cognitive flight, mission, target, command, configuration, IFF, readiness, LoRa-command or actuation authority.

## Protected runtime

Preserve the existing production runtime and behavior:
- HQ detection;
- Hailo detector;
- NanoTracker;
- CA Kalman;
- current-target/range;
- HOROS;
- telemetry/API;
- Dashboard-facing telemetry compatibility;
- WIDE capture/detection.

Keep WIDE environment/3D mapping disabled. Verify its actual current disable mechanism before relying on it.

Do not replace the current production pipeline.
Do not redesign protected components.
Do not use the obsolete direct-backend Shadow path as the Cognitive integration.

## Required integration

Use the reviewed cognitive_bridge.py as the thin ingress/composition boundary.

Connect current live TANGRA state/events into the existing Cognitive chain through structured State/Evidence contracts.

Preserve, where available from the producer and supported by the authoritative contracts:
- source component/capability identity;
- provenance;
- epistemic/claim class;
- realism class;
- freshness;
- evidence reference;
- correlation identity;
- validity/confidence.

Use the full existing Cognitive ingress and COG-20 path. Do not bypass the Cognitive chain by wiring live state directly to a model/backend.

Integrate the required live Cognitive persistence lifecycle using the existing reviewed Cognitive persistence/experience components. Persistence must survive a controlled runtime restart without granting authority.

If the current Pi package layout or Cognitive interfaces differ from the repository assumptions, make only the smallest integration change justified by verified current code. Do not redesign the Cognitive architecture. Report every necessary deviation.

## Procedure

1. PRECHECK
Verify actual Pi hostname/platform, current runtime root, entry point, service definition, active process, Python environment, relevant Cognitive package availability, current git/file state where applicable, storage paths, lifecycle source, WIDE mapping state, and current authority/control configuration. Confirm reviewed candidate identity before integration.

2. ROLLBACK POINT
Before any modification, create a recoverable backup/checkpoint of every production file/configuration that may change. Record exact paths and restoration commands.

3. BASELINE
Before change, capture bounded current health/performance evidence sufficient for comparison:
- service/process health;
- /api/health and /api/telemetry if present;
- HQ/Hailo detection path;
- tracking/NanoTracker/CA Kalman;
- range/HOROS;
- telemetry;
- WIDE capture/detection and mapping-disabled state;
- representative FPS/cadence/resource observations available from current runtime.
Do not invent unavailable metrics.

4. INTEGRATION
Integrate the reviewed bridge into the current runtime with minimal changes. Feed live operational evidence into structured Cognitive ingress. Preserve operational fail-open behavior: Cognitive failure must not break the existing TANGRA runtime.

5. COGNITIVE CHAIN / COG-20
Demonstrate with actual runtime evidence that observations pass through the bridge into the existing Cognitive ingress/full COG-20 path, not an obsolete direct-backend Shadow path. Preserve provenance/epistemic/source metadata across the boundary.

6. PERSISTENCE
Configure/use the existing Cognitive persistence lifecycle required by the reviewed architecture. Demonstrate a controlled write/state transition, controlled restart, and restoration/continued availability after restart. Do not treat bridge checkpointing alone as proof of the full Cognitive persistence lifecycle unless the authoritative current architecture explicitly defines it that way.

7. CONTROL STATE
Verify before, during and after integration:
CONTROL_ENABLED=false
AUTHORITY=NONE
operational_authority=[]
Verify no Cognitive-originated operational command/control path becomes active.

8. TESTS
Run the bridge qualification and applicable Cognitive tests that are actually available and executable on the Pi. Record exact commands, counts, failures/errors and exit codes. If the full cumulative regression is available on the Pi, run it; otherwise state exactly what was and was not executed. Never infer 317/317 PASS.

9. LIVE RUNTIME
Start/restart the actual TANGRA service in a controlled manner and validate:
- service remains healthy;
- HQ/Hailo detection remains operational;
- NanoTracker/CA Kalman tracking remains operational;
- range/HOROS remains operational;
- telemetry/API remains operational;
- WIDE capture/detection remains operational;
- WIDE environment mapping remains disabled;
- Cognitive observations demonstrably enter through the bridge/full Cognitive ingress;
- Cognitive failure/isolation behavior does not disrupt the protected runtime.

10. REGRESSION
Compare post-change runtime evidence with the pre-change baseline. Identify any measurable degradation, error, changed protected behavior, unexpected resource impact, or telemetry breakage. Do not call regression PASS without evidence.

11. ROLLBACK
If integration fails, Cognitive authority is not NONE, persistence fails in a way that compromises runtime integrity, or protected production behavior is degraded, restore the pre-change checkpoint and verify restoration. Report the failed state and rollback evidence. Do not leave a degraded production runtime active.

## Non-goals

- no autonomous Cognitive control;
- no flight/actuation enablement;
- no protected perception-chain redesign;
- no replacement production pipeline;
- no obsolete direct-backend Shadow integration;
- no unrelated cleanup/refactor;
- no claim that the WORKSHOP 317-test regression passed.

## Required report format

Report only verified facts under exactly these headings:

PRECHECK
BASELINE
FILES_CHANGED
BRIDGE_INTEGRATION
COGNITIVE_CHAIN
COG20
PERSISTENCE
CONTROL_STATE
TESTS
LIVE_RUNTIME
REGRESSION
ROLLBACK
RESULT

For every failure distinguish implementation defect, integration defect, test-harness defect, environment limitation, or protected-runtime regression. Include exact commands/paths/commit or file identities where available.

STOP after the report. Do not independently promote further changes.
