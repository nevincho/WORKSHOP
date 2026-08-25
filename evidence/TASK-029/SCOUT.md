# TASK-029 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25

## Dependency / duplication check
Canonical VK chain requires TASK-032 PASS before TASK-029. TASK-032 is now PASS. TASK-028 registry and TASK-007 HomeNode are also PASS. Existing HomeNode already carries connectivity/status/capabilities/provenance, but no separate tested health/evidence view was found. TASK-040 event envelope owns sensor events and is not a replacement for device health.

## Smallest justified scope
Add a non-Core immutable device health view derived from an existing `HomeNode`. Represent device identity/type, capabilities, connectivity, status, optional last-seen timestamp, and health evidence/provenance. Do not invent health measurements: absent last-seen remains `None`; current status/connectivity remain those already validated by HomeNode.

## Affected components
- new `family_guardian_ai/SOURCE_V09/app/device_health.py`
- new deterministic repository tests

## Protected / excluded
No registry operations changes; no schema redefinition; no capability probing; no network discovery; no device-specific integration; no Core/personality/memory changes; no live runtime claims.

## Validation
Use TASK-041 fixtures through `HomeNode`, cover camera/audio/generic node classes, status/connectivity preservation, optional last-seen, immutable evidence, and deterministic output.

## Rollback
Pre-Worker LIVE Legacy head: `d49095fac45cdee7cab0a32c850c48e21b606c61`.

## Codex Gate
Not required; bounded pure repository model with existing fixtures/test route.
