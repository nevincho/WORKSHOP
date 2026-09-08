# TASK 6 TEST RESULTS

Primary exact-chain suite: 18/18 PASS.
Bounded review-correction test: 1/1 PASS.
Aggregate TASK6 validation: 19/19 PASS.

- top_down_baseline: PASS
- mild_oblique_10: PASS
- moderate_oblique_measured: PASS
- strong_oblique_measured: PASS
- three_target_scales: PASS
- multiple_ranges: PASS
- yaw_variation: PASS
- known_orientation_factor: PASS
- uncertain_orientation_increases_sigma: PASS
- incorrect_orientation_containment: PASS
- semantic_loss: PASS
- span_collapse: PASS
- partial_silhouette primary probe: PASS
- candidate_conflict: PASS (`candidate_disagreement` from asymmetric wrong projection-factor fixture)
- insufficient_orientation_fail_closed: PASS
- production_not_promoted: PASS
- deterministic_repeatability: PASS
- frozen_t1_t4_unchanged: PASS
- review correction `test_partial_silhouette_fails_closed`: PASS; five partial-silhouette exact-chain probes each produced `<2` usable TASK3 candidates, `insufficient_independent_evidence`, and no VERIFIED metric promotion.

Frozen T1-T4 Git blob hashes matched before and after exact-chain execution. T5 reviewed artifact remained untouched; TASK6 candidate/correction diff contains no TASK1-TASK5 source path changes.
