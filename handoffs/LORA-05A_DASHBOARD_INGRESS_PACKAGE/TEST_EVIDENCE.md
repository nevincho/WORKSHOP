# LORA-05A Test Evidence

Final deterministic validation:

- LORA-02 accepted regression: **47/47 PASS**.
- LORA-03 accepted regression: **31/31 PASS**.
- LORA-05A ingress tests: **21/21 PASS**.
- Python compile validation: **PASS** for LORA-02 codec, LORA-03 observer, LORA-05A package/tests.
- Wall-clock sleeps: none.
- Physical transport: none.
- Dashboard 2.1 source inspected/modified: no.
- Runtime/DroneGuard/HTTP/WIDE/command paths modified: no.

The reconstructed validation copy of the LORA-02 archive was recovered directly from accepted WORKSHOP commit `f24e5c3064b0331df0c231f752f3ff5571c931a6`. Its source SHA-256 values exactly match the dependency hashes recorded by the accepted LORA-03 fixture:

- `codec.py`: `5ab0b90e6a4bf498ee56cd8faf849aaf156a4871b4e8ab5599e010ff7321ab49`
- `models.py`: `c71cf62464ec0c2054a84abb08a8bc0b62396063e124a782f204eaf8630472a0`
- `mock_transport.py`: `91a716a780f4481fe9435434a1369b9c76a600ec53b6666104aef697c0ef62b5`
- `__init__.py`: `988a9ef31d9682b1f7bf0d3c7f080b56588bffb125f6b9b24c549d131e7370f1`

LORA-03 observer source was reused from accepted package `543f0771d420e460b3ae3e631cd285e9f880e691` unchanged.

Covered LORA-05A scenarios include all five message-class mappings, duplicate/event idempotence, late TARGET/SPATIAL suppression, old-session suppression, corruption/incompatible-version rejection, compatible unknown EVENT handling, deterministic FRESH/STALE/DISCONNECTED/recovery, multi-source isolation, invalid metric absence, optional field absence, opaque target references, end-to-end provenance preservation, and local-only link metrics.
