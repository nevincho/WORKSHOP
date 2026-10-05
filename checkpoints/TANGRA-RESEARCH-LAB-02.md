# TANGRA-RESEARCH-LAB-02 — Read-Only Research Checkpoint

CHECKPOINT_ID: TANGRA-RESEARCH-LAB-02

PROJECT: TANGRA

TASK_ID: TANGRA-RESEARCH-LAB-02

TIMESTAMP: 2026-10-05

TARGET_REPOSITORY_OR_RUNTIME: WORKSHOP coordination/evidence only; TANGRA sources inspected read-only

BRANCH_OR_RUNTIME_CONTEXT: WORKSHOP `main`; no production/Pi/runtime context accessed

SNAPSHOT_REFERENCE: Worker commit `b2f9d0f`; independent review and checkpoint commit containing this file

VALIDATION_EVIDENCE:
- `evidence/TANGRA-RESEARCH-LAB-02/WORKER.md`
- `evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.py`
- `evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.json`
- `review/TANGRA-RESEARCH-LAB-02.md`

TESTS_RUN:
- deterministic script re-execution with stable JSON hash;
- independent arithmetic assertions for residual, profile ratios, focal/bbox sweep and timestamp coefficients;
- provenance, bbox-domain, coordinate-frame and ground-truth-independence sampling;
- uncertainty/claim-scope challenge;
- repository hygiene and read-only boundary inspection.

PROTECTED_COMPONENT_STATUS: PASS — no TANGRA target repository, production/Pi/runtime, firmware, model, configuration, service, Dashboard or authority path was modified

ROLLBACK_METHOD: Revert only the WORKSHOP JOB-02 task/evidence/review/checkpoint/state commits; no target rollback applies

KNOWN_LIMITATIONS:
- fresh production source/runtime remains `NOT VERIFIED`;
- this checkpoint validates a research evidence/error-budget artifact, not operational TANGRA performance;
- live bbox transform/lineage, target extent distributions, final extrinsics, pose/world transform and measurement age remain `NOT VERIFIED` or unbounded;
- the 4.36 m/4.366 m result remains one bounded near-field point with unspecified truth-measurement uncertainty;
- JOB-03 and later campaign conclusions remain `NOT EXECUTED` at this checkpoint.

REVIEW_VERDICT: PASS

TANGRA_MODIFIED: NO
