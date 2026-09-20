# TANGRA-COG-BRIDGE-01 — Qualification Blocker

DATE: 2026-09-20
STATUS: BLOCKED — PLATFORM PAYLOAD-TO-EXECUTION-MIRROR TRANSFER NOT EXPOSED
ROOT_CAUSE: WORKER ORCHESTRATION REGRESSION

## Current exact blocker
Historical WORKSHOP evidence proves that repository-side Worker validation did not require outbound GitHub access or authenticated Git checkout inside the Python execution container.

The proven execution model was:
`authenticated repository/submitted payload -> temporary exact-content local Python mirror -> tests -> independent repository/blob identity verification -> evidence -> Reviewer`.

Current capabilities can independently:
- read the authoritative private repository/ref/blob/tree through the authenticated repository connector;
- execute shell/Python in an isolated execution environment;
- obtain authoritative commit/tree/blob identities.

The currently exposed orchestration surface does not expose the historical platform operation that transfers/materializes the complete authenticated submitted repository payload into that isolated Python workspace while preserving exact paths/content.

That payload-to-mirror transfer boundary is the remaining blocker.

## Superseded diagnoses
SUPERSEDED AS ROOT CAUSE:
- no outbound GitHub network from the Python container;
- no authenticated Git clone/checkout in the Python container;
- no existing GitHub Actions workflow run/dispatch route;
- generic local checkout/workspace provisioning requirement.

Those observations remain historically true but are not root cause. HOROS successfully executed with no outbound GitHub route by using a temporary local mirror of submitted payloads.

See:
- control_room/WORKER_EXECUTION_INCIDENT_2026-09-20.md
- evidence/TANGRA-COG-BRIDGE-01/EXISTING_PYTHON_EXECUTION_ROUTE_FORENSIC.md

## Current target identity
Repository: nevincho/TANGRA-2.0
Branch: cognitive-bridge-integration
HEAD: e2d5cd10b780d87ef5b5ff25b50a2f10c2a9caef
Tree: c21fb9e5ac1becb763118692e220e3cbe15cc5ea
Bridge source blob: 5f4a6346fa70e369452067d9d96f776a84468a64
Bridge test blob: c67b9fe1ba85c372947b5e14c43cfdb5d3190695

## Qualification consequence
TEST EXECUTION: NOT RUN in this recovery attempt
PACKAGE REGRESSION: NOT RUN
INDEPENDENT REVIEW: NOT ELIGIBLE
REAL PI: NOT RUN / NOT AUTHORIZED / UNTOUCHED
CODEX: NOT USED

No Cognitive Bridge implementation failure is established.

## Unblock condition
Expose/select the existing platform capability that performs:
`authenticated submitted repository payload -> isolated temporary exact-content Python mirror`.

Once available, resume this SAME task directly through existing qualification, regression, raw evidence, post-execution identity verification, independent Reviewer and checkpoint. Do not restart implementation and do not add Git checkout as a prerequisite.
