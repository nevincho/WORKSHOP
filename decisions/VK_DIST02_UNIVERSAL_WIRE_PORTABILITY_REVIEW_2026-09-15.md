# VK DIST-02 Universal Wire / Serialization Portability Review

Date: 2026-09-15
Status: ARCHITECTURE REVIEW — CORRECTIONS REQUIRED BEFORE DIST-04 IMPLEMENTATION
Scope: review only; no VK runtime or DIST-02 implementation changes.

## Result
DIST-02 distributed semantics are substantially platform-neutral: logical/node identity, immutable durable records, per-origin causal sequence, lineage, replica frontiers, checkpoints, reconciliation, StateClass, replay/conflict rules and non-causal timestamps do not inherently depend on OS, CPU, filesystem, transport or Python.

The current serialized interchange is not yet a sufficient language-independent wire specification. It is deterministic Python implementation code, not a normative cross-language protocol. DIST-04 implementation must therefore wait for a bounded wire-contract correction gate.

## Python-specific / underspecified risks
- `_canonical()` recognizes Python Enum, Mapping, list/tuple and `to_dict()` objects; those object semantics are not portable.
- mapping keys are converted with `str(k)`, permitting collisions; wire object keys must already be strings.
- Python integers are arbitrary precision; cross-language integer range is unspecified.
- arbitrary payload/provenance can contain floats; cross-language floating canonicalization is unspecified and non-finite numbers are not explicitly rejected.
- UTF-8 is used, but Unicode normalization policy is unspecified.
- member ordering and string escaping depend on Python JSON encoder behavior rather than a normative wire rule.
- null versus omitted semantics are not defined for optional fields.
- unknown enum behavior and forward compatibility are not defined.
- timestamps are free-form strings; they are correctly non-causal but need a normative interchange syntax.
- schema_version exists, but protocol/wire negotiation, record schema compatibility and unknown-field behavior are incomplete.
- SHA-256/lowercase hex behavior is implementation-implied rather than fully declared as a wire rule.
- IDs are strings without normative validity constraints.
- ReplicaFrontier map/gap encoding and ordering require language-independent rules.
- payload/provenance use unrestricted `Any`; wire values need a finite portable value algebra.

## Required pre-DIST-04 wire contract
Define `VK Distributed Wire Profile v1` before synchronization-engine implementation. It must specify:
- transport-independent data model;
- permitted primitive value algebra: object with UTF-8 string keys, array, string, bounded integer, boolean, null; floats excluded unless separately standardized;
- exact integer range;
- canonical UTF-8 serialization, member ordering and escaping;
- Unicode policy;
- null versus omitted rules;
- timestamp profile;
- enum and unknown-value behavior;
- required/optional fields and unknown-field behavior;
- protocol, contract and record-schema version compatibility rules;
- digest algorithm identifier, exact digest input and encoding;
- deterministic golden byte/digest vectors for Python, Kotlin and C/C++ conformance tests;
- canonical DurableRecord, ReplicaFrontier, Checkpoint and ReconciliationRecord examples;
- rejection vectors for invalid keys, integers, numbers, text, enums and versions.

A published canonical JSON specification may be evaluated as a building block, but adoption is NOT DECIDED here; its numeric/text constraints must first match VK requirements.

## Independence invariant
Normative distributed semantics and wire bytes MUST NOT depend on OS/filesystem, CPU endianness/word size, Python classes, local DB representation, transport framing, host discovery, device type or inference runtime. Platform implementations are codecs/adapters conforming to the same vectors. Identical semantic content emitted by Python, Kotlin or C/C++ must produce identical canonical bytes and integrity digest.

## NOT VERIFIED
- Cross-language golden-vector reproduction has not been executed.
- Kotlin/C/C++ codecs do not exist and are not required by this review.
- No normative canonical serialization profile has been selected.
- Maximum field/string/record sizes and resource limits remain unspecified.
- Peer authentication belongs to later transport work, not this review.
