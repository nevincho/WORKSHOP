# TAI-COG-17 — Bounded Replay Diagnostic Harness

Status: COMPLETE / REVIEWER PASS
Date: 2026-09-12

Objective: implement a bounded post-mission/offline replay harness that projects existing COG-01 RecordedEvent / COG-02 EvidencePacket sources into the reviewed COG-16 deterministic diagnostic executor using exact COG-15 tool IDs and COG-12 replay vocabulary.

Base: nevincho/TANGRA-2.0 @ 8c786120bdb8dd29fa98056dbcbd01ddf277846c
Branch: tai-cog-17
Reviewed checkpoint: 000da0117c320f17aac53de39ccfc20a5376f669

Protected: COG-00..16, production/runtime, HQ/Hailo/Nano/CA/CurrentTarget/HOROS authority, FC/carrier, communications authority, recorded evidence artifacts.

Hard invariants: post-mission/offline only; MISSION_CONSTRAINED rejected; no cognition/LLM, Digital Twin execution, remediation, tuning, config/mission/target mutation, shell/network/filesystem scanning, command dispatch, Pi integration, approval or operational authority.

Validation: py_compile PASS; bounded unittest harness 34/34 PASS.
Reviewer: PASS.
Blockers: NONE.
COG-18: NOT STARTED.
