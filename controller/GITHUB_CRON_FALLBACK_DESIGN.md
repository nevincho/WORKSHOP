# GitHub Cron Fallback Controller — Staging Design

STATUS: STAGED / NOT ACTIVE

## Purpose
Provide a repository-native scheduler and observable run ledger for WORKSHOP if ChatGPT Scheduled Tasks proves unreliable.

## Activation rule
This design MUST remain off the default branch until explicitly activated after the ChatGPT scheduler validation window.

## Architecture
GitHub Actions schedule -> checkout WORKSHOP -> record scheduler heartbeat -> inspect coordination state/queue -> optionally invoke Codex execution layer when explicitly enabled -> persist logs/evidence.

## Important boundary
GitHub Actions can provide reliable, inspectable scheduling and repository operations. It does not wake existing ChatGPT project chat sessions. For AI execution, the supported GitHub-native option is OpenAI's `openai/codex-action`, which currently requires a provider API key stored as a GitHub Actions secret. This is distinct from ChatGPT Plus/Codex plan quota unless product support explicitly changes.

## Safety defaults
- Workflow is staged on a non-default branch, therefore scheduled runs are not active.
- Codex invocation is additionally gated by repository variable `WORKSHOP_CODEX_ENABLED == true`.
- No target runtime deployment is performed by this scheduler scaffold.
- TANGRA remains on hold according to WORKSHOP state.
- All runs must create observable heartbeat/log output.

## Proposed schedule
Hourly at minute 17 (`17 * * * *`) to avoid top-of-hour GitHub Actions congestion.

## Activation procedure
1. Validate ChatGPT Fresh Controller through the agreed observation window.
2. If fallback is needed, review the staged workflow.
3. Merge/copy the workflow onto the default branch `main`.
4. Leave `WORKSHOP_CODEX_ENABLED` false until an execution credential/budget decision is made.
5. Verify one manual `workflow_dispatch` run first.
6. Only then enable Codex execution if required.
