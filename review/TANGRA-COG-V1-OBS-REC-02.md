# TANGRA-COG-V1-OBS-REC-02 — Independent Reviewer

DATE: 2026-10-04
ROLE: INDEPENDENT REVIEWER
TARGET: nevincho/TANGRA-2.0:tangra-cog-v1-obs-rec-02@c1b4c171f4747ab0d2936a32633284084a01638a
BASE: tangra-cog-v1-obs-rec-01@ef9db4b3691e3807982d4cdc0cddd80dfe310195
VERDICT: PASS

## Scope review

PASS.

Final base-to-head diff contains exactly four task files: the existing COG-01 recorder, the reviewed OBS-REC-01 capture adapter, one durability qualification suite, and one exact restoration of the canonical frozen COG-01 static fixture required by the pre-existing regression test.

No protected runtime, Mission IPC, camera, Hailo, tracker, Kalman, CurrentTargetManager, HOROS, COG-15, COG-16 or COG-22 file changed.

## Sequence continuity

PASS.

Recorder startup scans valid retained JSONL evidence and sets next sequence to highest retained sequence + 1. A caller-provided lower start_sequence cannot cause reuse. Restart qualification proves sequence 1,2 -> restart -> 3 -> restart with start_sequence=1 -> 4, with chronological unique replay.

Complete corruption is not silently accepted or removed. Existing COG-01 replay-time hard-error semantics are preserved.

## Torn-tail recovery

PASS.

Recovery is intentionally narrow: only the undecodable, non-newline-terminated final line of the newest JSONL file is eligible. Valid preceding records remain replayable. The torn bytes are preserved in one overwrite-only recorder-torn-tail.quarantine file, then the active JSONL is truncated and fsynced.

A complete malformed record still raises on replay.

Recovery status records file, discarded bytes, policy and after_sequence. RECOVERED_AFTER_CRASH is only assigned when the mission's last retained sequence equals the recovery boundary, preventing stale historical recovery state from misclassifying a later incomplete mission.

## Mission finalization

PASS.

OBS-REC-01 STOP now includes explicit completion_state=COMPLETE plus capture counters and recorder loss counters.

Recorder mission_status distinguishes:
- COMPLETE: valid STOP retained;
- RECOVERED_AFTER_CRASH: START retained, no STOP, and current tail-recovery boundary follows that mission's last retained sequence;
- INCOMPLETE: START/evidence without STOP and without matching crash-tail recovery.

A STOP is never inferred from absence of errors.

Drain has an explicit timeout and remains fail-open.

## Byte retention

PASS with explicit storage-boundary interpretation.

max_total_bytes and max_mission_bytes deterministically constrain JSONL event evidence while preserving existing file/record bounds. Low-priority MISSION_NUMERIC_AGGREGATE evidence is discarded first. Lifecycle markers, errors/failures, state transitions and evidence-loss records have highest retention priority.

If pressure is impossible to satisfy using only low-priority evidence, lower-priority non-protected evidence is removed before protected evidence. Any removal is counted; no evidence is fabricated.

Auxiliary overhead is separately bounded: recorder-status.json is a single fixed-shape atomic sidecar; recorder-torn-tail.quarantine is a single overwrite-only file. Byte caps are therefore exact for the JSONL evidence store, with bounded auxiliary overhead rather than unbounded hidden files.

## Loss accounting

PASS.

Persisted/exposed recorder status includes:
- queue overflow;
- I/O failures;
- malformed input;
- retention dropped records;
- retention dropped bytes;
- aggregate/other/priority retention classes;
- tail recovery count/status.

OBS-REC-01 retains mission capture dropped_inputs, queue_overflows and recorder_failures in mission evidence. Mission status surfaces evidence coverage as incomplete when loss or missing completion is observed.

## Producer-path safety

PASS.

submit() validates/serializes and performs only bounded put_nowait queue insertion. Filesystem work remains on the recorder worker. Queue-full returns fail-open RecorderResult and does not block Mission.

## Qualification review

Final authoritative GitHub Actions run: 37197316122
Executed head: edbf92eefd6e92999086a4f315750ee0a49c1086

PASS:
- py_compile
- OBS-REC-02: 9/9
- OBS-REC-01 regression: 6/6
- existing COG-01 regression: 12/12
- total: 27 PASS / 0 FAIL

Final repository head c1b4c171f4747ab0d2936a32633284084a01638a differs from the executed qualification head only by deletion of the temporary qualification workflow; all four task blobs are unchanged.

## Conclusion

OBS-REC-02 closes the requested repository-side durability boundary without replacing COG-01, adding a database, introducing control authority, or wiring production/Pi runtime.

VERDICT: PASS
