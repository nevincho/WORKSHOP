# TAI-COG-17 — WORKER EVIDENCE

Result: ENGINEERING COMPLETE
Date: 2026-09-12

Engineering repository: nevincho/TANGRA-2.0
Branch: tai-cog-17
Base: 8c786120bdb8dd29fa98056dbcbd01ddf277846c
Head: 000da0117c320f17aac53de39ccfc20a5376f669

Implemented five new COG-17 files only: README, bounded replay-policy fixture, package export, replay implementation, tests.

Reuse confirmed: COG-01 RecordedEvent; COG-02 EvidencePacket/EvidenceRecord; COG-12 ReplayOperation directly (`ReplaySourceType` is an alias); COG-15 DiagnosticToolRegistry exact IDs/resource policy; COG-16 DiagnosticExecutor for every diagnostic; COG-04 DiagnosticResult/NO_CONCLUSION remains authoritative.

Supported replay sources: REPLAY_LATEST_AVAILABLE, REPLAY_EVENT_WINDOW, REPLAY_EVIDENCE_PACKET. EVENT_WINDOW uses fixed inclusive sequence/time bounds, max 128 items. Duplicate requested tool IDs are rejected. Latest selection is deterministic sequence order. Evidence-packet replay validates exact evidence source ref.

Evidence projection preserves historical evidence_ref, event_id, sequence_id, recorded timestamp, producer identity, source component/capability, provenance, claim class, state domain, validity and freshness. StateEvent.value must already be a dictionary diagnostic sample; missing/non-projectable values are never synthesized. Duplicate evidence refs are rejected rather than rewritten.

Per-tool projection filters the replay source only to evidence types declared by that exact COG-15 descriptor before dispatch through COG-16. One tool failure is isolated; successful sibling results remain intact and overall status becomes PARTIAL.

Resource containment: MISSION_CONSTRAINED -> UNSUPPORTED_MODE. No fallback/escalation. No filesystem scanning/network/runtime access.

Source immutability checks cover both RecordedEvent sources and EvidencePacket serialization before/after replay.

Validation: py_compile PASS; bounded unittest harness 34/34 PASS, 0 failures/errors after final source-ref/record-validation tightening. Source blob validated locally and repository content SHA matched final implementation.

A recurring artifact_tool spreadsheet warmup traceback occurred before unittest startup; unrelated to COG-17. unittest itself PASS.
