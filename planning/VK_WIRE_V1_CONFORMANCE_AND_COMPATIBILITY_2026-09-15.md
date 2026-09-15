# VK Wire v1 — Conformance / Compatibility Plan
Date: 2026-09-15
Status: ARCHITECTURE/CONFORMANCE DESIGN — NO RUNTIME MODIFICATION

## Cross-language conformance procedure
A candidate implementation must parse the normative specification without consulting Python source, consume the exact repository golden/rejection vectors, and produce machine-comparable evidence.

For every golden vector it must: validate schema; produce expected canonical UTF-8 bytes; produce expected SHA-256 where applicable; produce expected StateClass eligibility and causal/frontier interpretation. For every rejection vector it must reject with the expected protocol category and must not partially admit the object.

CROSS-LANGUAGE CONFORMANCE PASS requires: (1) normative spec independent Reviewer PASS; (2) reference Python implementation passing all vectors; (3) at least one independently implemented non-Python codec/validator passing the same vectors byte-for-byte and category-for-category; (4) SHA-256 equality for all digest vectors; (5) causal/frontier/replay/conflict fixtures equal; (6) evidence identifies implementation/version/toolchain and exact vector commit; (7) no unresolved normative ambiguity. Kotlin/C++/Rust/JS may later add evidence; v1 PASS does not require all future languages.

## DIST-02 compatibility classification
Classification: B — CONFORMANT WITH BOUNDED COMPATIBILITY CORRECTIONS.

Accepted semantics remain compatible, but current Python representation is not v1-conformant because:
- no `wire_profile_version` fields;
- `_canonical` accepts arbitrary Any/to_dict/Mapping, stringifies non-string keys and accepts tuples;
- Python JSON permits implementation-dependent numeric domain and can emit floating point/NaN unless constrained;
- no signed-64 range enforcement;
- no NFC normalization/collision rejection;
- canonical escaping is delegated to Python json behavior rather than the normative v1 encoder;
- parent arrays are not required sorted/unique beyond reconciliation distinctness;
- identifier/digest lexical constraints are absent;
- timestamp format is unconstrained;
- closed-schema/unknown-field/version negotiation rules are absent.

These are bounded codec/schema validation corrections; they do not require changing accepted causal semantics. Implementation correction is NOT authorized in VK-WIRE-01.

## DIST-03 compatibility assessment
DIST-03 remains IMPLEMENTED / STATIC REVIEW PASS / BEHAVIORAL VALIDATION BLOCKED; this task does not reclassify it.

Future v1 compatibility work is required because DIST-03 constructs DIST-02 DurableRecord directly and therefore inherits its current serializer. In addition, legacy memory payload fields `confidence` and `importance` may be Python floats; v1 prohibits floating numeric tokens. A future compatibility adapter must define an explicit record-type schema representation (for example bounded decimal strings or scaled integers) and migration/version behavior without changing memory meaning. No choice is made here. `observed_at` from legacy `recorded_at` also requires RFC3339 UTC validation/canonicalization. Parents must satisfy v1 canonical lineage ordering. Existing explicit SHARED_REPLICATED export policy is compatible and must remain protected.

## Bounded implementation backlog
WIRE-02: implement a pure v1 canonical codec/validator behind a new explicit API; retain DIST-02 semantic objects.
WIRE-03: add Python conformance runner consuming repository vectors.
WIRE-04: specify `vk.memory.compat.v1` field schema for confidence/importance/time and a non-destructive migration/encoding adapter.
WIRE-05: build one independent non-Python codec/validator (language chosen later) solely for conformance evidence.
WIRE-06: run cross-language byte/digest/rejection/causal matrix and independent review.
Only after WIRE-06 PASS and DIST-03 behavioral PASS+checkpoint may DIST-04 implementation begin.

## Transport independence
Canonical record bytes and semantics are unchanged across IPC, LAN, HTTP, WebSocket, removable storage, store-and-forward or future transports. Framing/authentication/retry are transport concerns outside v1 semantic encoding.

## Portable Seed / Survival compatibility
Micro-LIVE/platform adapters can implement v1 without Python. Bootstrap Intelligence receives deterministic parser/validator results only; it cannot make invalid records valid or redefine StateClass, integrity, lineage, sequence, frontier or version handling.

## NOT VERIFIED
No current implementation has run these vectors. No non-Python implementation exists. Cross-language byte equality is therefore NOT VERIFIED.