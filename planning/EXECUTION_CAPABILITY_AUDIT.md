# EXECUTION CAPABILITY AUDIT

STATUS: TODO / POST-TEST-002 INFRASTRUCTURE MILESTONE
PURPOSE: Establish the real tool and execution capabilities available to WORKSHOP agents before autonomous implementation work begins.

## Rule
Do not infer runtime access from GitHub access. Every route below remains NOT VERIFIED until demonstrated by evidence.

## Required capability matrix
For each project and role, verify: read, write, execute, validate, checkpoint/rollback, and protected/destructive-operation boundaries.

### Common capabilities
- GitHub read/search and history/diff inspection.
- GitHub write to WORKSHOP for tasks, evidence, reports, blockers, handoffs, reviews, and checkpoints.
- Target-repository read.
- Controlled target-repository write only for authorized implementation roles.
- Build/test/lint execution where applicable.
- Runtime/log/process/service inspection.
- Backup/checkpoint creation and rollback verification.
- Independent validation tools: HTTP/API probes, test runner, build verification, logs, process/service state, file/hash comparison, Git diff, configuration comparison, performance/resource sampling, UI/screenshot evidence when relevant.

## Role expectations
### Scout / Planner
Read/search repositories and runtime evidence; inspect history/diffs; collect evidence; no implementation by default.

### Worker
Perform authorized mechanical and implementation work; tests/builds; controlled shell/filesystem operations; create checkpoints; no protected/destructive changes without authorization.

### Codex Gate
Conserve Codex capacity. Codex is not for discovery, inventory, mechanical file work, log summarization, or routine validation. Escalate only with a minimal verified implementation package.

### Reviewer
Independently verify the claimed objective using runtime/test/diff evidence where possible. Worker reports alone are not validation.

## Project execution routes to establish
### TANGRA
Expected route: WORKSHOP -> canonical repository `nevincho/TANGRA-DOCS` + controlled Pi5 execution/inspection route.
Needed capabilities: SSH or equivalent controlled execution, filesystem read, systemd/process/log inspection, runtime health, camera/Hailo status where relevant, tests, telemetry, backup/rollback, Git evidence.
Safety: autonomous workers must not restart production services, deploy to validated production runtime, or alter protected validated components unless explicitly authorized by task/policy.
Current execution capability: NOT VERIFIED.

### VK
Expected route: WORKSHOP -> canonical design in `nevincho/TANGRA-DOCS` + UI repository `nevincho/LIVE` -> Codex/controlled execution bridge -> Windows runtime.
Needed capabilities: Windows filesystem, PowerShell, Python environment, process management, localhost HTTP/API tests, browser/UI validation, logs, Git, controlled synchronization, checkpoint/rollback.
Important: GitHub visibility does not prove access to the active Windows runtime.
Current execution capability: NOT VERIFIED.

### HOROSCOPES
Expected route: WORKSHOP -> controlled Codex/SSH route -> Pi4 project/runtime.
Needed capabilities: SSH, filesystem, Git, Python/environment inspection, tests, service/process/log inspection, HTTP endpoint tests where applicable, backup/rollback.
Use Codex for precision implementation/debugging, not routine grep/inventory/file movement/log reading.
Exact Pi4 project/repository/runtime path: NOT VERIFIED.
Current execution capability: NOT VERIFIED.

## Restricted capabilities
Do not grant or exercise unrestricted destructive shell operations, mass deletion, production deployment, destructive DB migrations, secrets export, force push/history rewrite, automatic major dependency upgrades, arbitrary system configuration, or unrestricted Codex invocation. Apply existing WORKSHOP policies and human gates.

## Acceptance criteria for this milestone
1. Each project has a repository-backed capability record.
2. Each claimed execution route has direct evidence or is explicitly NOT VERIFIED.
3. Reviewer has at least one independent validation path for each environment that is claimed operational.
4. Backup/rollback path is established before implementation changes are authorized.
5. Protected/destructive operations are explicitly bounded.
6. No project is declared autonomous merely because its GitHub repository is accessible.

## Sequencing
Run after TEST-002 establishes autonomous repository task discovery. This audit is non-destructive and should precede real autonomous implementation work.
