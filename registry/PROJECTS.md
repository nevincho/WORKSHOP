# WORKSHOP Project Registry

STATUS: MANDATORY COORDINATION DATA

This registry defines WORKSHOP coordination targets. Target repositories/runtimes remain authoritative for implementation state.

## Priority order
1. TANGRA — highest priority
2. VK — second priority
3. Horoscopes — third priority

## TANGRA
- Coordination mode: MONITOR / AUDIT / REPORT by default.
- Autonomous implementation: FORBIDDEN unless explicitly authorized in WORKSHOP.
- Canonical repository: `nevincho/TANGRA-DOCS`.
- Repository URL: `https://github.com/nevincho/TANGRA-DOCS`.
- Default branch: `main` unless a task explicitly identifies and verifies another branch/ref.
- Runtime/production path: NOT VERIFIED in this registry; discover from repository/runtime evidence before use.
- Protected production/validated components: preserve by default.

## VK
- Coordination mode: AUTONOMOUS RUNTIME / TOOLING / TESTING within policy.
- Canonical Core / personality / approved memory mutation: HUMAN GATE REQUIRED.
- Known canonical design repository evidence: `nevincho/TANGRA-DOCS`, branch `family-guardian-ai`, under `family_guardian_ai/`.
- Known implementation/UI repository evidence: `nevincho/LIVE`; exact implementation ref must be verified before modification.
- Human-confirmed active runtime host: Vlad's Windows PC.
- Human-confirmed runtime root: `D:\Store\AI`.
- Human-confirmed execution route: Codex may be used for precision integration into the local Windows runtime when Codex Gate authorizes it; Vlad is fallback human bridge only when Codex cannot complete the local integration.
- Before any modification, the executing agent/Codex MUST verify current local path, entrypoint, Git/runtime state, target files, checkpoint/rollback route and tests. Human confirmation of access does not prove current implementation state.
- Execution priority: AUTO -> CODEX -> HUMAN BRIDGE fallback.

## HOROSCOPES / MYSTICARIUM
- Coordination mode: AUTONOMOUS DEVELOPMENT according to canonical plan/TODO.
- Canonical repository planning/design evidence currently used by WORKSHOP: `nevincho/TANGRA-DOCS`, branch `agent/mysticarium`, path `projects/mysticarium/`; verify current ref before implementation.
- Human-confirmed active runtime/implementation host: Raspberry Pi 4.
- Human-confirmed execution route: Codex has SSH access to the Pi4 and is authorized to use that route for implementation/testing within WORKSHOP policy.
- Before any modification, Codex/agent MUST verify the actual Pi4 project root, repository state, runtime entrypoint/services, test command, checkpoint/rollback path and protected components through direct SSH/runtime evidence. Do not infer Pi4 implementation state from repository planning files alone.
- Execution priority: AUTO -> CODEX/SSH.

## Authority rule
WORKSHOP is authoritative for coordination state only. A target project repository/runtime is authoritative for architecture, implementation, validation, completed work and blockers.
