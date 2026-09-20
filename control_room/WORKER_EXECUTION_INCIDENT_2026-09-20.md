# WORKSHOP Worker execution incident — 2026-09-20

STATUS: OPEN — ROOT CAUSE IDENTIFIED; HISTORICAL ROUTE SEMANTICS RECOVERED; PLATFORM PAYLOAD-TRANSFER INVOCATION NOT EXPOSED
AFFECTED_TASK: TANGRA-COG-BRIDGE-01
CLASSIFICATION: WORKER ORCHESTRATION REGRESSION

## When it worked
Repository-persistent evidence establishes the following successful repository-side Worker Python executions:
- HOROS Phase A: 13/13 PASS.
- HOROS lanes: temporary local mirror of submitted campaign payloads; 27/27 PASS.
- HOROS final: 31/31 PASS plus compileall PASS; executed mirror checked against repository Git blob identities.
- TAI-COG-01: py_compile PASS plus 12/12 unittest PASS.
- TAI-COG-20: py_compile PASS plus 23/23 unittest PASS.
- TAI-COG-27: py_compile PASS; compact 14/14 PASS; extended acceptance 41/41 PASS.

The decisive historical HOROS record is WORKSHOP commit 4cc46a29f85569f4074d9241ffffa8a2aac54784. It states that the execution container had no outbound GitHub route and therefore used a local mirror of submitted campaign file payloads, with exact-content verification against repository blob SHAs performed separately before Reviewer PASS.

## What failed
During TANGRA-COG-BRIDGE-01 qualification, orchestration substituted:
`Python Worker -> authenticated Git clone/checkout -> tests`
for the historically proven:
`authenticated repository payload -> temporary exact-content Python mirror -> tests -> independent blob identity verification`.

This produced BLOCKED — EXECUTION ACCESS before the existing qualification tests were run.

## Initial misdiagnosis — SUPERSEDED
The first diagnosis treated lack of outbound GitHub network from the isolated Python environment, lack of a local Git checkout, and lack of a dispatchable GitHub Actions run as the execution blocker. A post-reload retry reproduced those conditions.

That diagnosis is superseded as root cause. Historical HOROS evidence proves no-outbound-GitHub was normal during successful Worker execution. Git clone/checkout inside the execution container was not a historical prerequisite.

The old evidence is retained for chronology; it must not be read as the current root-cause determination.

## Root cause
WORKER ORCHESTRATION REGRESSION.

The historically proven `submitted repository payload -> temporary exact-content Python mirror` stage stopped being selected/performed. An unsupported authenticated Git-checkout prerequisite was substituted.

No task-schema difference was found that explains the regression. Historical TAI-COG tasks and the affected bridge task all route as WORKER and identify repository/ref/checkpoint/paths/validation without a special checkout field.

No current policy prohibition against the historical payload-mirror method was found.

## Impact
- Cognitive Bridge implementation was NOT demonstrated defective by this incident.
- Qualification and regression execution were prevented.
- Python/shell execution capability remained available.
- Authenticated repository connector access remained available.
- Codex was not required or used.
- Pi/production was untouched.
- TANGRA-COG-BRIDGE-01 remained the same task.

## Recovery attempt on 2026-09-20
The historical semantics were tested against the currently exposed capabilities.

Authoritative target:
- repository: nevincho/TANGRA-2.0
- branch: cognitive-bridge-integration
- HEAD: e2d5cd10b780d87ef5b5ff25b50a2f10c2a9caef
- tree: c21fb9e5ac1becb763118692e220e3cbe15cc5ea
- package payload: 153 repository blobs, 741424 bytes
- package tests: 21 repository blobs, 94395 bytes
- bridge source blob: 5f4a6346fa70e369452067d9d96f776a84468a64
- bridge test blob: c67b9fe1ba85c372947b5e14c43cfdb5d3190695
- qualification document blob: 284dfefcb96cb194dadf2cbbd2f577a6fe2f4d35

Available semantics:
- authenticated repository file/blob/tree reads: AVAILABLE;
- isolated shell/Python execution: AVAILABLE;
- authoritative commit/tree/blob identity acquisition: AVAILABLE.

Still missing from the exposed orchestration surface:
- the historical platform operation that transfers/materializes the complete authenticated submitted repository payload into the isolated Python workspace while preserving paths/content.

The repository contains no persistent runner, venv, container definition, mirror script, or Worker launcher implementing that transfer. The historical evidence describes the semantics but not the platform invocation.

Because this run was explicitly forbidden from inventing a replacement execution architecture, manually designing a new connector-to-filesystem exporter was not substituted.

RESULT: execution recovery remains BLOCKED at one exact platform boundary: authenticated repository payload -> isolated temporary exact-content Python mirror.

## Repair status
PARTIAL / ROUTING SEMANTICS RECOVERED, PLATFORM TRANSFER CAPABILITY NOT EXPOSED.

The false Git-checkout prerequisite is removed. Future recovery must resume from the missing payload-transfer operation, not from Git/network troubleshooting.

If/when that operation is exposed, the same task must continue:
exact payload mirror -> identity record -> existing bridge qualification -> package regression -> raw execution evidence -> post-execution identity verification -> independent Reviewer -> PASS/REWORK -> checkpoint.

## Prevention
See policies/EXECUTION_ROUTING_POLICY.md. Repository-side Worker Python validation in an isolated environment must check the repository-payload -> temporary exact-content execution-mirror route before declaring execution access blocked. Outbound GitHub access and authenticated Git checkout inside the Python environment are not implicit prerequisites.

## Cross references
- evidence/TANGRA-COG-BRIDGE-01/EXISTING_PYTHON_EXECUTION_ROUTE_FORENSIC.md
- evidence/TANGRA-COG-BRIDGE-01/WORKFLOW_RECOVERY.md
- evidence/TANGRA-COG-BRIDGE-01/WORKSPACE_PROVISIONING_RECOVERY.md
- evidence/TANGRA-COG-BRIDGE-01/POST_RELOAD_EXECUTION_ROUTE_RECHECK.md
- blockers/TANGRA-COG-BRIDGE-01-QUALIFICATION.md
