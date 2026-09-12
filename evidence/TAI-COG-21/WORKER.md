# TAI-COG-21 — WORKER EVIDENCE

RESULT: PASS

Engineering repo: `nevincho/TANGRA-2.0`
Branch: `tai-cog-21`
Base: `ea9777ee9f5b57bde75e641ad7885d5069228c26`
Head at final validation: `7d8e4d2804ef9f59dd33f206fb490c2ae9f9ab37`
Compare: ahead 7, behind 0. Unique changed paths: 5, all under `TANGRA_2_0/00_FOUNDATION/TAI_COG_21/`.

Implemented:
- README.md
- fixtures/signal_policy.json
- tangra_cognitive_signal/__init__.py
- tangra_cognitive_signal/signal.py
- tests/test_signal.py

Validation:
- py_compile PASS
- unittest 34/34 PASS, 0 failures/errors
- 11 signal types present
- severity vocabulary exactly INFO/NOTICE/WARNING
- deterministic IDs/order/serialization PASS
- bounded diagnostic/correlation/hypothesis/signal inputs PASS
- evidence/source refs preserved
- HYPOTHESIS/INFERENCE/UNKNOWN/SOURCE_GAP preservation PASS
- severity cannot promote epistemic class
- no COG-21 VERIFIED_CAUSE generation
- action NONE; authority NONE; operational_authority empty
- semantic duplicate suppression PASS
- conflict/unknown preservation PASS
- NO_SIGNAL PASS
- MISSION_CONSTRAINED PASS using pre-existing inputs only
- no backend/heavy diagnostic/replay/Twin invocation surface
- COG-09 observer/observation identity preserved passively
- no network/radio/UI/command transport surface
- raw degraded DiagnosticResult alone produces NO_SIGNAL, avoiding 1:1 subsystem duplication
- per-item malformed/missing source refs isolated; valid sibling signal preserved as PARTIAL

Reviewer-discovered defect before checkpoint: request-wide hypothesis validation initially prevented sibling preservation for one malformed hypothesis. Validation was moved to per-item emission; regression 34/34 PASS after correction.

External note: unrelated artifact_tool spreadsheet startup warning appeared in earlier runs; final unittest itself completed PASS.