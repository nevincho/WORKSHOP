# LORA-02 — Protocol + Codec Implementation

Status: PASS / isolated reference package.

Artifact: `LORA_02_PROTOCOL_CODEC.tar.gz`

Contains:
- `PROTOCOL_SPEC.md`
- `FILE_MANIFEST.md`
- `tangra_lora_v1/models.py`
- `tangra_lora_v1/codec.py`
- `tangra_lora_v1/mock_transport.py`
- `tests/test_codec.py`
- `fixtures/v1_vectors.json`
- `fixtures/performance.json`

Validation: 47/47 deterministic tests PASS; Python compile PASS. No production/runtime/Dashboard/WIDE files modified. No physical transport or command path included.

Canonical fixture sizes with optional timestamp present: HEARTBEAT 38 B, TARGET 36 B, SPATIAL 63 B, EVENT 41 B, DIAGNOSTIC 37 B.

Wire envelope: `TG` magic, v1, message ID, flags, source_id:u16, session_id:u32, sequence:u16, uptime_s:u32, payload_len:u8, optional timestamp_ms:u32, payload, CRC16-CCITT-FALSE.

Protocol max packet size: 192 bytes. This is a protocol bound only and is not an RF/LoRa MTU claim.
