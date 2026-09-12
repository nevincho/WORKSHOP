# LORA-03 Test Evidence

- LORA-03 receiver/link observer tests: **31/31 PASS**.
- LORA-02 codec regression: **47/47 PASS** using the accepted local artifact unchanged.
- Python `compileall`: PASS.
- Physical transports: none.
- Wall-clock sleeps/threads/sockets: none.
- Production/runtime/Dashboard/WIDE changes: none.

Covered scenarios:
- initial NO_DATA; first valid -> FRESH
- normal progression
- single/repeated duplicate
- single/multi gap with inferred missing count
- out-of-order current-session packet
- 65534 -> 65535 -> 0 -> 1 wrap
- old pre-wrap packet after wrap
- new session at sequence 0
- new session at nonzero sequence
- old-session packet after restart
- same-session uptime regression
- first packet after long silence
- FRESH -> STALE -> DISCONNECTED -> FRESH
- corruption during FRESH
- corruption burst and recovery
- unknown compatible TLV
- unknown nonzero EVENT ID
- unsupported protocol version
- duplicate EVENT suppression
- same EVENT reference on new sequence suppression
- new EVENT reference delivery
- same EVENT reference in new session delivery
- late TARGET suppression
- old-session SPATIAL suppression
- DIAGNOSTIC loss isolation
- multiple-source isolation
- mock drop/duplicate/reorder/corrupt
- receiver metrics proven absent from encoded packets

Freshness is refreshed only by packets that establish a newly accepted session or advance the current-session sequence baseline. Duplicate/replay/late/old-session/corrupt observations do not refresh freshness.
