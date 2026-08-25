# TASK-032 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25

## Necessity and phase
TASK-021 established that VK has partial capability/status probes but no single normalized host-wide capability discovery contract. TASK-042 subsequently supplied canonical mock profiles covering CPU/GPU/RAM/storage/network/display/audio/cameras/microphones/Bluetooth/Wi-Fi/LAN/models/tools. TASK-028 is now PASS, satisfying the canonical VK chain prerequisite.

## Smallest justified repository scope
Implement a non-Core repository-only capability discovery normalization layer. It must accept supplied probe observations, normalize all TASK-042 dimensions to `present|absent|unknown`, preserve `unknown` distinctly from `absent`, reject unsupported states, and expose deterministic output. Missing observations become `unknown` rather than fabricated absence.

This task does NOT authorize live OS/hardware probing in the controller environment. A probe-provider boundary may be defined for later runtime integration, but fixture values must never be represented as live hardware evidence.

## Affected components
- new `family_guardian_ai/SOURCE_V09/app/capability_discovery.py`
- new deterministic tests under `family_guardian_ai/SOURCE_V09/tests/`

## Protected / non-goals
- VK Core/personality/memory/provenance unchanged
- do not replace `config/capabilities.json` policy registry
- no registry health model (TASK-029)
- no LAN discovery (TASK-010)
- no device-specific adapters
- no live Windows deployment or hardware claims
- no heavy dependencies

## Validation
Use exact TASK-042 fixtures. Verify all required dimensions, exact normalization of all three fixture profiles, missing=>unknown, unknown!=absent, invalid state rejection, stable deterministic key order/output.

## Rollback
LIVE Legacy pre-Worker head: `d59b1871db64e782ee85c5f8706882c19eaa7bb3`.

## Codex Gate
Not required. This is bounded pure repository logic with existing fixtures and deterministic test route.
