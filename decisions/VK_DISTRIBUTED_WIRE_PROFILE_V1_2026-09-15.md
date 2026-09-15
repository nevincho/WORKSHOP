# VK Distributed Wire Profile v1
Date: 2026-09-15
Status: NORMATIVE SPECIFICATION — IMPLEMENTATION NOT MODIFIED

## Scope and precedence
This document defines the language-independent wire representation for accepted VK-DIST-02 distributed semantics. Python is a reference implementation only. Transport framing, storage and filesystem layout are out of scope.
Invariant: same logical value -> same canonical bytes -> same SHA-256 digest -> same causal interpretation.

## 1. Encoding and canonical-wire acceptance
A v1 wire document is exactly one JSON object encoded as UTF-8 without BOM. UTF-8 MUST be shortest-form valid Unicode. Malformed UTF-8, lone surrogates, duplicate object keys, non-object top level or trailing non-whitespace data are invalid. Every protocol object MUST contain `wire_profile_version`: integer 1.

Wire objects themselves MUST arrive in canonical form. A receiver parses with duplicate-key detection, validates the value domain/schema, canonicalizes the parsed object, and byte-compares canonical output with the received document after transport framing has removed only framing bytes; any difference (including insignificant whitespace, alternative escaping, non-NFC strings or noncanonical numbers) is INVALID_ENCODING. Thus transports may frame bytes differently but cannot redefine record bytes.

## 2. Canonical JSON
Every string and object key is Unicode NFC. If normalization makes two keys equal, reject INVALID_SCHEMA. Object keys are strings only and ordered lexicographically by Unicode scalar-value sequence after NFC. Arrays retain schema-defined order. No whitespace is emitted. Separators are exactly `,` and `:`.
Strings use `\"` for quotation mark, `\\` for reverse solidus and lowercase `\u00xx` for every U+0000..U+001F control; all other valid Unicode scalar values are emitted directly as UTF-8. Solidus is not escaped. Surrogates are prohibited. Empty object/array are `{}`/`[]`; booleans `true`/`false`; null `null`.

## 3. Wire-safe recursive value domain
Allowed: object<string,value>, array<value>, NFC string, signed v1 integer, boolean, null. Prohibited: implementation objects/classes, bytes, sets, tuple as a distinct type, floating point, decimal numeric tokens, NaN/infinity, dates and platform handles. Such concepts require explicit versioned schema representation.

## 4. Numeric profile
JSON numeric tokens are base-10 integers -9223372036854775808..9223372036854775807. Canonical syntax: `0` or optional `-` plus non-zero digit then digits. `-0`, leading zeros, plus, exponent and decimal point are prohibited. No coercion. Overflow = INVALID_TYPE; sequence-domain violation = INVALID_SEQUENCE.

## 5. Null versus omitted
Absent and null are distinct. Required fields are present and non-null unless schema says nullable. DurableRecord `claim_class`, `admission_state`, `observed_at` are required nullable keys. `parents`, `provenance`, `payload` are required containers and use empty containers when empty. Optional extension fields are omitted when absent unless extension schema says otherwise.

## 6. Enums
Exact case-sensitive strings. StateClass: SHARED_REPLICATED, NODE_LOCAL, TRANSIENT, SECRETS, DERIVED_REBUILDABLE. Unknown semantic enum = INVALID_ENUM; no fallback/default mapping.

## 7. StateClass safety
StateClass is explicit. Durability/storage never implies replication eligibility. Only exact SHARED_REPLICATED is synchronization eligible. No receiver may infer it from database presence, record type, transport or persistence location.

## 8. Time
`observed_at` is null or canonical RFC3339 UTC `YYYY-MM-DDTHH:MM:SS[.fraction]Z`; fraction 1..9 digits with trailing fractional zeros removed. Pre-wire application values with offsets may be exactly converted to UTC, but canonical wire always uses Z. Invalid = INVALID_SCHEMA. Wall time is never causal authority.

## 9. Identifiers
Identifiers are non-empty NFC strings, max 255 UTF-8 bytes, no controls. `record_id` is globally unique opaque or deterministic under its record-type contract; `vk_identity_id` identifies LogicalIdentity; `node_id` identifies a node; checkpoint/reconciliation IDs are opaque. No timestamp-based causal precedence.

## 10. origin_sequence
Integer 1..9223372036854775807. Initial accepted sequence 1; contiguous history increments exactly one. Same record_id+digest = idempotent replay; same record_id+different digest = record conflict; occupied origin_node_id+sequence with different record = sequence conflict. Missing predecessor creates gap/held state. v1 never wraps on overflow.

## 11. Lineage
`parents` required array. Root `[]`; one or multiple parents allowed. Parent order is semantically irrelevant, therefore canonical parents are unique and sorted by Unicode scalar sequence after NFC. Duplicate/unsorted/self-parent = INVALID_LINEAGE. Missing parents cause dependency/gap handling; they are never invented. Detectable cycle = INVALID_LINEAGE. Divergence is preserved.

## 12. ReplicaFrontier
Fields: wire_profile_version, schema_version, contiguous, gaps. `contiguous`: node_id -> 0..MAX; missing node means 0. `gaps`: node_id -> strictly increasing unique sequence array, each >=1 and > contiguous. Empty maps `{}`. Canonical key ordering applies. Equal contiguous+gaps = EQUAL; componentwise >= with at least one > = DOMINATES; <= analogously; otherwise DIVERGED, preserving DIST-02 semantics.

## 13. Checkpoint
Fields: wire_profile_version, checkpoint_id, vk_identity_id, frontier, canonical_state_digest, manifest_digest, schema_version. It declares a validated frontier plus canonical-state/manifest digests and never erases history. Both digest fields are exactly 64 lowercase hex characters. The Checkpoint object's own `integrity_digest` is a derived value, not a field of the v1 Checkpoint object: SHA-256 over the canonical bytes of the complete Checkpoint object listed above. If a future envelope carries that derived digest, the envelope schema must define it separately. Filesystem/database layout is irrelevant.

## 14. ReconciliationRecord
Fields: wire_profile_version, reconciliation_id, vk_identity_id, input_record_ids, result, provenance, policy, authority, schema_version. At least two distinct inputs. `input_record_ids` is semantically a set, therefore unique and canonical-sorted. Originals remain preserved. Its derived integrity digest is SHA-256 over canonical bytes of this complete object and is not an additional v1 object field. No newest-file/timestamp winner.

## 15. DurableRecord and integrity
Required fields: wire_profile_version, record_id, record_type, vk_identity_id, origin_node_id, origin_sequence, state_class, provenance, payload, parents, claim_class, admission_state, schema_version, observed_at, integrity_digest.
Integrity is SHA-256. Remove exactly top-level `integrity_digest`, canonicalize all remaining fields, hash those bytes, encode exactly 64 lowercase hexadecimal ASCII. Verification recomputes and compares; malformed/mismatch = INVALID_INTEGRITY. The complete transmitted DurableRecord, including integrity_digest, must itself satisfy canonical-wire byte acceptance. No LLM override.

## 16. Versioning
wire_profile_version is required integer 1. Peers advertise supported profiles before semantic exchange. Unsupported older/newer = UNSUPPORTED_VERSION. Silent downgrade prohibited. Object schema_version does not imply wire compatibility. Unsupported mandatory semantics fail explicitly.

## 17. Extensibility
Normative v1 objects are closed by default. Future extension schemas classify fields SAFE_TO_IGNORE or MUST_UNDERSTAND. Only explicitly declared SAFE_TO_IGNORE fields may be ignored. Unknown fields otherwise = UNSUPPORTED_REQUIRED_FIELD. Integrity treatment must be defined by the extension.

## 18. Error model
INVALID_ENCODING, INVALID_SCHEMA, INVALID_TYPE, INVALID_ENUM, INVALID_SEQUENCE, INVALID_LINEAGE, INVALID_INTEGRITY, UNSUPPORTED_VERSION, UNSUPPORTED_REQUIRED_FIELD. Post-parse semantic outcomes remain IDEMPOTENT_REPLAY, RECORD_ID_CONFLICT, ORIGIN_SEQUENCE_CONFLICT, HELD_SEQUENCE_GAP.

## Semantic preservation
LogicalIdentity, NodeIdentity, DurableRecord, ReplicaFrontier, Checkpoint, ReconciliationRecord and accepted replay/conflict/frontier/divergence/gap/reconciliation semantics remain DIST-02 semantics. Representation is narrowed for portability; semantic change requires separate review.

## Bootstrap boundary
Parsing, canonicalization, integrity, StateClass, lineage, sequence, frontier and version handling are deterministic implementation behavior. Bootstrap Intelligence may consume outcomes but cannot redefine them or validate malformed wire data.