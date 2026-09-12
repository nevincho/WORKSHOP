# LORA-05A — Dashboard-side LoRa ingress package

Isolated Workshop package only. It depends on the accepted LORA-02 `tangra_lora_v1` codec and LORA-03 `lora03_link` observer; neither is vendored or reimplemented here.

Pipeline:

`bytes + monotonic receive time -> LORA-03 (which invokes LORA-02 decode) -> semantic router -> abstract DashboardStateSink`

No physical radio, socket, serial/SPI/USB, Dashboard 2.1 source, HTTP modification, WIDE implementation, command path, IFF, readiness, actuation, or production integration is included.

Receiver-derived link state is local metadata only. There is no dependency on transmitted `lora_connected`.
