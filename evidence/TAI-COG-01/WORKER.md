# TAI-COG-01 — WORKER EVIDENCE

TASK_ID: TAI-COG-01
PROJECT: TANGRA / TAI
DATE: 2026-09-12
EXECUTION_CLASS: WORKER / repository-side Phase A engineering

## Implementation location
Repository: nevincho/TANGRA-2.0
Branch: tai-cog-01
Base checkpoint: 7036cb78580d446ba700e318daf0bbe8c60d4afc
Final branch head: 56a670e9afc3fa9e91e3e835c496b1f26928e1e1
Path: TANGRA_2_0/00_FOUNDATION/TAI_COG_01/

## Files added
- README.md
- tangra_state_recorder/__init__.py
- tangra_state_recorder/recorder.py
- tests/test_recorder.py
- fixtures/sample_record.jsonl

No TAI-COG-00 file or pre-existing TANGRA component was modified.

## Recorder interface
- StateEventRecorder.submit(event) -> RecorderResult
- StateEventRecorder.record_sync(event) -> RecorderResult (offline/test helper)
- StateEventRecorder.iter_records() -> Iterator[RecordedEvent]
- StateEventRecorder.replay() -> list[StateEvent]
- StateEventRecorder.start()/stop()

RecordedEvent is metadata-only envelope: sequence_id, recorded_at, producer_id, event. It reuses StateEvent rather than duplicating its schema.

## Design properties
- append-only JSONL within each retained file;
- deterministic monotonically assigned sequence IDs protected by a lock;
- UTC ISO-8601 recorded_at timestamp;
- explicit producer_id;
- bounded queue; submit uses put_nowait and no disk I/O;
- one daemon writer thread;
- bounded rotation by max_records_per_file and max_files;
- malformed StateEvent rejected before enqueue/write;
- malformed persisted record rejected during read/replay;
- worker I/O failure increments io_failures and does not raise into producer path;
- UNKNOWN/SOURCE_GAP and all COG-00 provenance/realism semantics are serialized unchanged;
- Python standard library only.

## Direct validation
Local deterministic validation against the implemented package:
- py_compile: PASS
- unittest: 12/12 PASS, 0 FAIL, 0 ERROR

Direct tests cover:
- StateEvent round-trip and replay equivalence;
- sequence ordering 1,2,3;
- SENSED_DIRECTLY/LIVE, RECEIVED_EXTERNALLY/REPLAY, DERIVED_DETERMINISTICALLY/SHADOW, SIMULATED/SYNTHETIC, UNKNOWN/HISTORICAL preservation;
- UNKNOWN and SOURCE_GAP preservation;
- malformed event rejection;
- malformed persisted record rejection;
- retention/rotation bound;
- synchronous I/O error fail-open result;
- producer submit returns before disk I/O;
- asynchronous worker I/O failure isolated from producer;
- deterministic timestamp/producer/sequence metadata;
- static JSONL fixture replay preserving SIMULATED provenance versus SYNTHETIC realism.

One pre-final fixture defect was found by the new test: provenance was incorrectly written as SYNTHETIC. COG-00 correctly rejected it because provenance uses SIMULATED while realism uses SYNTHETIC. Fixture corrected; final 12/12 PASS.

## COG-00 regression evidence
The COG-01 branch was created directly from reviewed COG-00 checkpoint 7036cb78580d446ba700e318daf0bbe8c60d4afc.

Final branch comparison shows only five new TAI_COG_01 files. COG-00 remains bit-identical:
- contracts.py blob SHA: 228d33108bd7b5494a5814653dd4ee38ab26869c
- test_contracts.py blob SHA: 8cad16a3aecf3cf28e14b44c03380caaddae62bb

These are the same reviewed COG-00 blobs that previously passed 12/12 tests. No COG-00 code path changed. COG-00 regression status: PASS BY IMMUTABLE BLOB IDENTITY + prior reviewed test evidence; not a new runtime execution claim.

## Runtime/production impact
NONE. No Pi5 access. No production/runtime integration. No HQ/Hailo/NanoTracker/CA/CURRENT_TARGET/HOROS modification. No diagnostics, Evidence Packet Builder, Digital Twin, adaptation, STT/TTS, LLM, FC/carrier/actuation or Codex.

## Duplication check
No duplicate event schema introduced. StateEvent is imported from TAI-COG-00. RecordedEvent contains recorder metadata only.
