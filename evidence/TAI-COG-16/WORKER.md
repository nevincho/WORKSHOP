# TAI-COG-16 — WORKER EVIDENCE

Result: ENGINEERING COMPLETE
Date: 2026-09-12

Engineering repository: nevincho/TANGRA-2.0
Branch: tai-cog-16
Base: 73106ae590dfdfb4a596fb74c55ff741e8ba92a7
Head: 8c786120bdb8dd29fa98056dbcbd01ddf277846c

Implemented five new COG-16 files only: README, bounded fixture, package export, executor implementation, tests.

Execution path: DiagnosticExecutionRequest -> exact COG-15 lookup -> resource-mode/dependency/evidence checks -> exact registered deterministic handler -> existing COG-04 DiagnosticResult -> DiagnosticExecutionResult.

Ten initial COG-15 tools have deterministic handlers. Evidence is explicit bounded JSON-safe data, max 128 items / default 64, canonical ordering, exact evidence refs, timestamps/freshness retained, path syntax rejected in evidence refs, no filesystem/network retrieval.

Causal safety: COG-04 DiagnosticConclusion exposes only NO_CONCLUSION. COG-16 does not add VERIFIED_CAUSE semantics. anomaly_detected never manufactures a cause.

System aggregation consumes supplied COG-04 diagnostic-result payloads only; missing required subsystem domains or UNKNOWN/NOT_TESTED inputs produce UNKNOWN.

Validation harness: py_compile PASS; unit tests 38/38 PASS, 0 failures/errors. Covered exact lookup, all ten handlers, unregistered-handler rejection, evidence bounds/canonicalization, missing evidence, UNKNOWN behavior, COG-04 result reuse, mode containment, dependency UNAVAILABLE, handler FAILED isolation, system UNKNOWN preservation, zero authority and forbidden-surface checks.

A recurring artifact_tool spreadsheet warmup traceback occurred before unittest startup; unrelated to COG-16. unittest itself PASS.
