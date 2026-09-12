# LORA-05A Integration Contract

## Input
- raw packet bytes
- local monotonic receive time

## Output
Transport-neutral semantic updates with `transport=LORA`, `source_id`, `session_id`, message class, receive time, and one semantic section: SYSTEM, TARGET, SPATIAL, EVENT, or DIAGNOSTIC. LINK updates are local receiver observations.

## Required real Dashboard bindings
All remain **ADAPTER_MAPPING_REQUIRED** until the actual Dashboard 2.1 source is inspected:

| Logical binding | Status |
|---|---|
| system sink | ADAPTER_MAPPING_REQUIRED |
| target sink | ADAPTER_MAPPING_REQUIRED |
| spatial sink | ADAPTER_MAPPING_REQUIRED |
| event sink/callback | ADAPTER_MAPPING_REQUIRED |
| diagnostic sink | ADAPTER_MAPPING_REQUIRED |
| link-status sink | ADAPTER_MAPPING_REQUIRED |

## Canonical-state rule
The future binding must feed the same canonical Dashboard business state already used by HTTP. This package does not create HTTP-specific or LoRa-specific competing target/spatial authorities. Transport metadata may remain separate.

## Excluded policy
No HTTP↔LoRa auto-failover, source-selection priority, retry/ACK, physical transport, or UI notification policy is defined here.
