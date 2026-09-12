# TAI-COG-15 WORKER EVIDENCE

RESULT: COMPLETE

Engineering repository: `nevincho/TANGRA-2.0`
Branch: `tai-cog-15`
Base: `36e92fefcd993fa5e4f556d82958dbeb02a2421a`
Engineering head: `73106ae590dfdfb4a596fb74c55ff741e8ba92a7`

Implemented files under `TANGRA_2_0/00_FOUNDATION/TAI_COG_15/` only:
- README.md
- fixtures/initial_registry.json
- tangra_diagnostic_registry/__init__.py
- tangra_diagnostic_registry/registry.py
- tests/test_registry.py

Implemented contracts:
- DiagnosticToolDescriptor
- DiagnosticToolRegistry
- DiagnosticToolIdentity
- DiagnosticToolAvailability
- DiagnosticExecutionClass
- DiagnosticEvidenceRequirement
- DiagnosticResourceProfile
- DiagnosticRegistrationResult
- DiagnosticLookupResult
- DiagnosticResourceMode

Reuse confirmed:
- diagnostic domains imported from COG-12 `DiagnosticDomain`;
- expected result contract fixed to COG-04 `DiagnosticResult.SCHEMA` (`TAI_DIAGNOSTIC_RESULT_V1`);
- no parallel diagnostic-result authority introduced.

Initial registry contains one descriptor for each domain: DETECTION, TRACKING, PREDICTION, RANGE, HOROS, SENSOR, PERFORMANCE, COMMUNICATIONS, COGNITIVE_BACKEND, SYSTEM.

Resource policy:
- `MISSION_CONSTRAINED` available only to explicitly `LIGHTWEIGHT_READ_ONLY` descriptors;
- heavy descriptors use POST_MISSION_FULL and/or OFFLINE_ENGINEERING;
- unsupported mode returns `UNSUPPORTED_MODE`; no escalation;
- missing dependency returns `UNAVAILABLE`; unknown tool returns `NOT_FOUND`.

Authority/safety:
- all descriptors side-effect-free and read-only;
- authority `NONE`; operational authority empty;
- no execute/run/dispatch/invoke/shell/activate API on registry;
- no diagnostic algorithms implemented.

Validation:
- py_compile PASS;
- unittest 28/28 PASS, 0 failures, 0 errors;
- deterministic serialization/enumeration PASS;
- duplicate IDs rejected;
- malformed/side-effectful/non-read-only/authority-escalating descriptors rejected;
- immutable descriptor test PASS.

No Pi/runtime/model/Codex/COG-16 work performed.
