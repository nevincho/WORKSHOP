# N1 Independent Review — Cycle 1

TASK_ID: TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
REVIEWED_COMMIT: b34abc9ddda315b0fc903424bb65e51d18d18f5a
RESULT: FAIL
FREEZE_RECOMMENDATION: NO

Findings:
1. `base_prov = tuple(getattr(source, "provenance", ()))` executes before exact source/provenance validation. A malformed direct object with non-iterable provenance can raise instead of deterministic fail-closed.
2. `NavigationAdapterPolicy.stale_after_s` is not independently validated. NaN or a value looser than frozen M2's 0.5 s policy can make N1's `usable_for_active_track` freshness classification unsound even though frozen M2 would later suppress stale data.
3. Explicit search provenance is concatenated without exact structure validation and can also raise on malformed input.

Required bounded repair:
- validate source type before reading provenance;
- require exact provenance tuple-of-string-pairs;
- validate policy type/value and forbid freshness >0.5 s or non-finite/negative values;
- validate search provenance before concatenation;
- add adversarial regression tests.

No redesign required. M1/M2/M3 semantics remain unchanged.
BLOCKER: bounded implementation defect only.
