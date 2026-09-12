# TAI-COG-23 — Digital Twin Experiment Foundation

Status: ENGINEERING COMPLETE / REVIEW PENDING AT TASK CREATION

Objective: build a bounded non-authoritative Digital Twin experiment layer for REPLAY and SYNTHETIC Phase-A experiments, with SHADOW structurally defined but non-executable.

Authoritative engineering repo: `nevincho/TANGRA-2.0`
Base reviewed checkpoint: `5bdc25db69dbe0dc948a8ebe5a6b938247457c16`
Branch: `tai-cog-23`

Protected: COG-00..22, production/runtime, HQ/Hailo/Nano/CA/CurrentTarget/HOROS, FC/carrier, communications authority.

Hard invariants:
- TWIN != REALITY
- EXPERIMENT != AUTHORITY
- SIMULATION != VALIDATION
- RESULT != PROMOTION
- authority = NONE
- operational_authority = []
- no live SHADOW, runtime mutation, commands, automatic promotion, ExperienceStore lifecycle mutation, LLM/model integration, Pi integration, or COG-24 work.
