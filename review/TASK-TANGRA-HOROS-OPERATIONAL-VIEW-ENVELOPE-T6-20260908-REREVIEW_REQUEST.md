# TASK 6 REREVIEW REQUEST

Candidate correction commit: `8732b62dbd96f4072f73c624bb5ed08e24b799dc`.

Cycle 1 condition: the original `partial_silhouette` harness check proved probe execution but did not independently assert fail-closed outcome.

Bounded correction only:
- added `handoffs/TASK-TANGRA-HOROS-OPERATIONAL-VIEW-ENVELOPE-T6-20260908/test_view_envelope_validation.py`;
- five exact-chain partial-silhouette probes must each yield `<2` TASK3 usable candidates, `t3_error=insufficient_independent_evidence`, and no VERIFIED metric promotion;
- focused correction test PASS;
- no T1–T5 file changed;
- no runtime, pose, tracker, 6DoF, production or TASK7 work added.

Please re-review the full TASK6 candidate plus this bounded correction.
