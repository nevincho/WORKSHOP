# TANGRA-FC-AUTONOMY-INTEGRATION-REWORK-02

MODE: CONTROL_ROOM
PROJECT: TANGRA
CAMPAIGN: TANGRA-FC-SOFTWARE-AUTONOMY
STATUS: COMPLETE
DATE: 2026-11-09

## Objective

Remove remaining Codex blockers in the WORKSHOP package without changing the approved TANGRA architecture.

## Required corrections

1. STEP_3
   - do not use simulation fixtures as evidence of real FC integration;
   - expose adapter contracts for the authoritative TANGRA controller, virtual Quad-X mixer and estimator;
   - if local FC headers are unavailable, mark ADAPTER_REQUIRED / NOT_INTEGRATION_TESTED.

2. STEP_4
   - stateful vertical-state producer from timestamped altitude samples;
   - validate dt, stale/duplicate/non-finite data and reset;
   - deterministic climb/descent/stale/invalid tests.

3. STEP_5
   - stateful local-state producer;
   - establish origin, transform geodetic observations to local frame, derive velocity from timestamps;
   - stale/discontinuity/invalid-origin/reset tests.

4. STEP_8
   - separate payload codec from MAVLink transport/dialect adapter;
   - explicit message ID, payload length and CRC-extra boundary;
   - malformed length, unknown ID, invalid enum, truncation and round-trip tests;
   - real TANGRA dialect unavailable => TRANSPORT_ADAPTER_REQUIRED.

5. Test validity
   - STANDALONE_SIM_PASS;
   - ADAPTER_CONTRACT_PASS;
   - REAL_FC_INTEGRATION_NOT_TESTED;
   - clean build and full test provenance.

6. Provenance
   - WORKSHOP Git commit SHA must be a 40-character Git commit;
   - ZIP SHA-256 must be reported separately as a 64-character digest.

NO_LOCAL_FC_EDITS: true
FLASHING: false
HARDWARE_OPERATIONS: false
PHYSICAL_OUTPUTS: OFF
ARCHITECTURE_REDESIGN: false

REVIEWER_VERDICT: PASS_WITH_EXPLICIT_LOCAL_ADAPTER_BOUNDARY
CHECKPOINT: checkpoints/TANGRA-FC-AUTONOMY-INTEGRATION-REWORK-02.md
READY_FOR_CODEX_REVIEW: YES
REAL_FC_INTEGRATION: NOT_TESTED
