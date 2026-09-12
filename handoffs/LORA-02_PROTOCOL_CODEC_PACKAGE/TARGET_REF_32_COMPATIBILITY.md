# LORA-02 target_ref 32-byte compatibility update

Status: PASS / bounded compatibility change.

- TARGET/SPATIAL `target_ref`: 1..32 bytes.
- EVENT `subject_ref`: unchanged at 1..16 bytes.
- Encoding remains `u8 length + opaque bytes`; envelope/message layout unchanged.
- Identity provenance, target identity semantics, tracking authority and spatial authority unchanged.
- `CURRENT_TARGET_0001` is 19 bytes and round-trips unchanged through TARGET and SPATIAL.
- LORA-03 and LORA-05A require no source/contract changes because both already preserve `target_ref` as opaque bytes and delegate ordering/decoding to LORA-02/LORA-03.

Validation: LORA-02 49/49 PASS; LORA-03 31/31 PASS; LORA-05A 21/21 PASS; compile PASS.
