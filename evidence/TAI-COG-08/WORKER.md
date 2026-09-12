# TAI-COG-08 — WORKER EVIDENCE

RESULT: PASS

Engineering repo: `nevincho/TANGRA-2.0`
Branch: `tai-cog-08`
Base: `f65d9a19eba5828715808ac246c921524bd04e82`
Candidate checkpoint: `ebd695a9081d9e47efe4e24d42f8927653e81292`

Created only under `TANGRA_2_0/00_FOUNDATION/TAI_COG_08/`:
- README.md
- fixtures/sample_analysis_result.json
- tangra_offline_analysis/__init__.py
- tangra_offline_analysis/analysis.py
- tests/test_offline_analysis.py

Implemented:
- `CognitiveAnalysisRequest`
- `CognitiveAnalysisResult`
- `CognitiveClaim`
- `OfflineCognitiveAnalyzer`
- `ResourceMode.POST_MISSION_FULL` boundary
- bounded categories OBSERVATION / INFERENCE / HYPOTHESIS / UNKNOWN / SOURCE_GAP / NO_CONCLUSION
- deterministic-only propagation path for VERIFIED_CAUSE
- EvidencePacket evidence-reference validation
- optional immutable DiagnosticResult / ExperimentResult passthrough
- MissionContext / SystemIdentity context
- COG-06 `CognitiveBackend.analyze()` invocation
- explicit UNAVAILABLE / FAILED / UNSUPPORTED handling
- zero operational authority
- StructuredReport-compatible `ReportClaim` conversion

Critical VERIFIED_CAUSE rule:
- backend-generated VERIFIED_CAUSE is rejected;
- COG-04 diagnostic `NO_CONCLUSION` cannot be promoted;
- propagation is accepted only when the referenced EvidencePacket event is already `ClaimClass.VERIFIED_CAUSE` with `Provenance.DERIVED_DETERMINISTICALLY`.

Validation:
- py_compile PASS
- unittest 20/20 PASS
- deterministic StubBackend integration PASS
- source evidence immutability PASS
- deterministic diagnostic/evaluator preservation PASS
- serialization round-trip PASS
- report-claim compatibility PASS
- branch containment: 5 commits ahead, 0 behind; 5 added files only under TAI_COG_08

Validation environment: local Phase-A compatibility modules matching consumed reviewed COG-00/02/04/06 interfaces. No GitHub CI, Pi5, Hailo, runtime, or production execution claimed.
