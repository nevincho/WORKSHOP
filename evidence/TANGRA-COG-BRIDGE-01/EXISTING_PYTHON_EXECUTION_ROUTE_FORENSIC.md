# TANGRA-COG-BRIDGE-01 — EXISTING WORKSHOP PYTHON EXECUTION ROUTE FORENSIC

DATE: 2026-09-20
TASK: TANGRA-COG-BRIDGE-01
RESULT: ROOT CAUSE IDENTIFIED — HISTORICAL PAYLOAD-MIRROR EXECUTION ROUTE WAS NOT ROUTED/RECONSTRUCTED
SCOPE: repository-side Worker execution only; no Codex; no Pi; no Cognitive redesign

## Root cause

The previous qualification attempts selected the wrong execution model.

Historical WORKSHOP did not require an authenticated Git checkout inside the Python execution container. The decisive persisted HOROS execution record, commit 4cc46a29f85569f4074d9241ffffa8a2aac54784, explicitly states:

> Execution environment used a local mirror of the submitted campaign file payloads because the execution container has no outbound GitHub network route. Exact-content verification against repository blob SHAs is performed separately before Reviewer PASS.

Therefore `git ls-remote` failure from the isolated execution container is expected historical behavior, not the root blocker.

The current TANGRA-COG-BRIDGE-01 handling incorrectly coupled:
1. authenticated GitHub repository access, and
2. local Python execution,
by requiring Git clone/checkout/materialization in the execution container.

Historical WORKSHOP separated them:
- repository connector/write path produced/read the submitted repository payload;
- a task-local external/local mirror of those submitted files was used by Python;
- tests ran in that mirror;
- exact repository blob identity was verified separately before Reviewer PASS;
- temporary external test workspace was not retained as a repository artifact.

## Historical path traced

### HOROS_3D

Commit f4efe25d86548f6f014ae5a60ec31021ab781722 records Worker execution of:
`python -m unittest Workshop.HOROS_3D.tests.test_contracts -v` -> 13/13 PASS.

Commit 4cc46a29f85569f4074d9241ffffa8a2aac54784 records:
- local mirror of submitted campaign file payloads;
- execution container has no outbound GitHub network route;
- exact-content verification against repository blob SHAs separately before review;
- `python -m unittest discover -s Workshop/HOROS_3D/tests -v` -> 27/27 PASS.

Final consolidated evidence records:
- `python -m unittest discover -s Workshop/HOROS_3D/tests -q` -> 31/31 PASS;
- `python -m compileall -q Workshop/HOROS_3D/implementation/horos3d` -> PASS;
- executed local mirror checked against repository Git blob identities.

The Phase-A evidence explicitly says: `Temporary external test workspace is not a repository artifact.`

### TAI Cognitive

TAI-COG-01 records local deterministic py_compile + unittest 12/12 PASS and exact COG-00 blob identity comparison.
TAI-COG-20 records py_compile + unittest 23/23 PASS. It also records an unrelated `artifact_tool` spreadsheet warmup traceback from the environment before the tests, which is direct evidence that execution occurred in a broader Python tool/runtime environment rather than a repository-native CI runner.
TAI-COG-27 records py_compile, compact 14/14, extended 41/41, and static checks PASS.

These campaigns use the same architectural separation: repository state/identity is evidenced separately from local deterministic Python execution.

## What the repository does and does not persist

Current WORKSHOP tree contains no persistent Python runner script, virtualenv definition, container definition, checkout script, workspace directory, or executable Worker launcher. The execution environment itself is therefore platform/tool-provided and ephemeral, not a versioned WORKSHOP repository environment.

The repository persists:
- Worker role and routing policy;
- task execution class;
- commands/results/evidence;
- branch/head/blob identity;
- temporary-mirror methodology in HOROS evidence.

It does not persist the platform-specific API/tool invocation that created the temporary mirror.

## Historical vs current configuration

Historical TAI-COG-01:
- EXECUTION_CLASS: WORKER
- repository + branch + base checkpoint
- affected package path
- deterministic validation method
- no explicit checkout/workspace metadata
- local Python execution succeeded.

Current TANGRA-COG-BRIDGE-01:
- EXECUTION_CLASS: WORKER
- repository branch known
- pre-change checkpoint known
- affected implementation/test paths known
- repository tests + regression required
- no explicit checkout/workspace metadata.

Therefore missing task metadata is NOT the differentiator. Historical tasks did not require a checkout/materialization field either.

## Regression mechanism

The regression is routing/orchestration, not task schema or Python capability:

The current Worker path treated the repository connector/Control-Room surface as though it had to provide a Git checkout to the execution container. That bypassed the previously proven WORKSHOP pattern of constructing a temporary exact-content mirror from submitted/read repository payloads, executing Python there, then separately proving blob identity.

No current policy change was found that prohibits the historical mirror method. Worker policy still permits deterministic repository test execution. AUTONOMY_POLICY explicitly permits repository-side deterministic/simulation tests. EXECUTION_ROUTING_POLICY requires the cheapest capable route and does not require Git clone.

The stale 2026-08-24 WORKER_STATUS and 2026-08-26 global state describe older execution-access conditions, but AUTONOMY_POLICY says stale summary state must not override newer canonical task/handoff evidence. They should not have been used to infer that the historical Python execution pattern disappeared.

## Current recoverability

The method is policy-valid and conceptually recoverable: exact submitted/read repository payload -> temporary local mirror -> Python tests -> independent repository blob identity verification.

However, the current Control Room/connector tool surface does not expose the historical platform operation that transfers the complete repository payload into the Python execution environment. Reconstructing a new transfer mechanism here would be a replacement execution architecture, explicitly outside this investigation.

Accordingly:
- Python execution environment: EXISTS as a platform execution capability historically and current shell/Python capability is available;
- repository-local Git/network inside it: was never required by HOROS;
- exact historical payload-to-mirror transfer invocation: NOT PERSISTED / NOT EXPOSED in current WORKSHOP repository configuration;
- task metadata defect: NOT FOUND;
- policy prohibition: NOT FOUND;
- root cause: Worker orchestration stopped selecting/performing the historical submitted-payload temporary-mirror stage and instead imposed an unnecessary Git-checkout prerequisite.

## Required routing correction

For TANGRA-COG-BRIDGE-01, Worker routing must use the established historical mode:

`repository submitted/read payload -> temporary exact-content Python mirror -> execute -> repository blob identity verification -> evidence -> Reviewer`

Do not require outbound GitHub access or Git checkout inside the Python container.

No bridge source was changed in this forensic step.
No qualification result is claimed because the historical payload-transfer operation itself is not callable from the currently exposed Worker/Control-Room tool surface.
No Codex or Pi action occurred.
