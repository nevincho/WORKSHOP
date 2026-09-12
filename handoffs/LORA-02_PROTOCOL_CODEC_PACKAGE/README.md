# LORA-02 — Protocol + Codec Implementation

Status: PASS / isolated reference package.

Original accepted artifact: `LORA_02_PROTOCOL_CODEC.tar.gz` from commit `f24e5c3064b0331df0c231f752f3ff5571c931a6`.

Current compatibility update: TARGET/SPATIAL `target_ref` maximum is 32 bytes. Wire layout, identity semantics, tracking/spatial authority, EVENT `subject_ref` 16-byte limit, CRC, versioning and all other v1 semantics are unchanged.

The current expanded `tangra_lora_v1/` files are the reviewable codec source for this bounded update. `TARGET_REF_32_COMPATIBILITY.md` records the exact compatibility boundary and regression result.

Validation: LORA-02 49/49 PASS; LORA-03 31/31 PASS; LORA-05A 21/21 PASS; `CURRENT_TARGET_0001` (19 bytes) TARGET/SPATIAL roundtrip PASS; compile PASS.

No production/runtime/Dashboard/WIDE/physical transport/command changes.
