# HB-04 — TANGRA System Health v1 PC Engine Package

Standalone, integration-ready Windows Dashboard 2.1 System Health v1 normalization engine implementing accepted HB-02/HB-03.

## Scope
- PC-side only.
- Exactly 12 canonical concepts.
- Consumes existing Dashboard merged telemetry and existing Runtime Controller status snapshots.
- No Pi/runtime writes, new telemetry protocol, UI, persistence/history, recovery, SOURCE_GAP remediation, or new numeric thresholds.
- WIDE alone consumes its existing source-native `max_age_s` freshness bound.

## Public API
```python
from system_health_v1 import SystemHealthV1Engine
engine = SystemHealthV1Engine()
normalized = engine.normalize(telemetry_payload, pi_status_payload)
```

`normalized["concepts"]` contains exactly the 12 HB-03 envelopes.

## Test
`python -m unittest discover -s tests -v`

No third-party dependency is required.
