# TASK 4 Re-review Request — correction cycle 1

Review only the two bounded Cycle 1 conditions for TASK-TANGRA-HOROS-RANGE-FUSION-CONTRACT-T4-20260908.

Corrections:
1. conflicting non-null `target_ref` or `frame_id` now fails closed before fusion;
2. compatible but materially disagreeing independent evidence now preserves the fused range but marks state/validity DEGRADED under explicit soft thresholds below the hard CONFLICT thresholds.

Corrected complete suite: 21/21 PASS.
Corrected host benchmark: n=100000; mean 0.01194369248 ms; median 0.011006 ms; p95 0.011808 ms; max 11.092934 ms.
No production integration, no TASK 5 work, no protected component changes.
