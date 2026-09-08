# TASK 7 RE-REVIEW REQUEST
Cycle-1 PASS_WITH_CONDITIONS corrected only inside TASK7.

Corrections: explicit AdvisoryContext gates target identity change and source timestamp regression; carrier pose now requires finite timestamp, identity, frame match and shadow freshness before world_navigation_available can become true. Invalid/stale pose is discarded for world navigation while target-relative passive advisory remains possible. No pose is fabricated or estimated.

Rerun: 22/22 PASS. HOST benchmark n=100000 mean 0.00376034039 ms median 0.003375 ms p95 0.003566 ms max 1.797074 ms.

No T1–T6 path modified. No production integration, command transport, flight-control or TASK8 work.
