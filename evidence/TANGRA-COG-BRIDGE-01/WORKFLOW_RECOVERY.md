# TANGRA-COG-BRIDGE-01 — WORKFLOW RECOVERY FINDING

DATE: 2026-09-20
CLASSIFICATION: ROUTING/PROVISIONING REGRESSION; NOT COGNITIVE IMPLEMENTATION FAILURE

## Historical HOROS execution evidence

The successful HOROS repository campaign did not use GitHub Actions as its qualification executor.

WORKSHOP evidence/evidence/HOROS_3D_FINAL.md and TANGRA-DOCS Workshop/HOROS_3D/IMPLEMENTATION_MANIFEST.md record:
- target branch: workshop-horos-3d;
- execution against an exact local mirror;
- local mirror Git blob identities checked against repository blobs;
- command: python -m unittest discover -s Workshop/HOROS_3D/tests -q;
- result: 31/31 PASS, 0 FAIL, 0 ERROR;
- command: python -m compileall -q Workshop/HOROS_3D/implementation/horos3d;
- result: PASS;
- a real coordinator defect was found, repaired, and the final suite rerun;
- no Pi action and no Codex execution occurred.

Independent review/HOROS_3D_FINAL.md then inspected implementation/test methodology, protected scope and failure handling and issued PASS. Repository-side campaign was classified COMPLETE/READY_FOR_CODEX_REVIEW, while physical/runtime claims remained NOT VERIFIED.

The persisted evidence names the execution environment only as an exact local mirror. It does not persist the product/tool identity that provisioned that mirror, nor an agent instance identifier. Therefore those details are NOT VERIFIED and must not be invented.

## Current divergence

TANGRA-COG-BRIDGE-01 was incorrectly treated as though the GitHub inspection/Actions surface selected by the Control Room agent were the WORKSHOP Worker execution boundary.

That differs from HOROS: HOROS qualification executed in a local repository mirror with shell/Python, then matched the executed payload to repository blob identities.

The current blocker correctly proves only that the selected GitHub surface has no workflow run/dispatch route. It does NOT prove that WORKSHOP historically lacked or conceptually lacks repository-side execution.

Current classification:
- Cognitive implementation failure: NOT ESTABLISHED.
- GitHub Actions requirement: FALSE; not the historical HOROS model.
- Historical execution route: local mirror + shell/Python.
- Current agent shell/container capability: available.
- Current private TANGRA-2.0 checkout/provisioning into that execution workspace: NOT VERIFIED / not exposed by the current repository connector route.
- Exact historical mirror-provisioning mechanism: NOT VERIFIED from persisted evidence.

## Required recovery

Continue the SAME TANGRA-COG-BRIDGE-01 task. Do not create a new bridge/task/branch.

Required Worker route:
1. provision/checkout cognitive-bridge-integration into an execution-capable local workspace;
2. verify checkout HEAD/blob identities against GitHub;
3. execute the existing bridge qualification and package regression;
4. persist exact commands/environment/counts/output;
5. repair only executed defects on the existing branch and rerun;
6. hand execution evidence + diff/checkpoint to independent Reviewer;
7. Reviewer independently verifies/reruns where its execution route permits;
8. PASS/REWORK;
9. checkpoint only after Reviewer PASS.

Codex remains prohibited. Production Pi remains untouched.

## Current route availability

PARTIALLY AVAILABLE.

Evidence:
- shell/container execution capability exists in the current Control Room environment;
- GitHub repository read/write access exists;
- no checked-out TANGRA-2.0 workspace is present;
- the GitHub connector exposes repository content and existing Actions-run inspection/rerun, but no current workflow run or start/dispatch path;
- persisted HOROS evidence does not identify a callable historical provisioning tool that can be re-instantiated from repository state alone.

Therefore the missing capability is specifically private-repository workspace provisioning/checkout into the execution environment, not Python test execution itself and not a Cognitive Bridge defect.
