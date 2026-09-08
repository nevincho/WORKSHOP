# TASK 6 — FROZEN ARTIFACT IDENTITY

Exact reviewed implementation artifacts materialized for execution:

| Task | Reviewed commit | Path | Git blob SHA |
|---|---|---|---|
| T1 | `c7b378841979f82b037c47be3571fa72a7b70e51` | `handoffs/TASK-TANGRA-HOROS-SPARSE-TARGET-GEOMETRY-T1-20260908/sparse_target_geometry.py` | `91f81e882af557f2d2106a8648ee283bfbdee81e` |
| T2 | `4bd4b5d38357db501de07511aeabaa4c0ae058e1` | `handoffs/TASK-TANGRA-HOROS-AI-CALIBRATED-GEOMETRY-T2-20260908/ai_calibrated_geometry_adapter.py` | `83202583f93ca43b134132f84d5cd51d7b59bcbe` |
| T3 | `c121ce25dbba84520c6f8e644281a7cb2bf3ee73` | `handoffs/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/sparse_geometry_range_source.py` | `d15e09dc63384d93719fdab30b50634750cfd65c` |
| T4 | `7f628a727b89599ea6977053ea12211b10e0ffcd` | `handoffs/TASK-TANGRA-HOROS-RANGE-FUSION-CONTRACT-T4-20260908/horos_range_fusion_contract.py` | `af995bdaab486b0c677bcd35c6166d90d253bbfb` |
| T5 | `e48eaa71d49721786b6acc490a32c7af800161bf` | `handoffs/TASK-TANGRA-HOROS-GEOMETRY-RANGE-TEMPORAL-STABILITY-T5-20260908/temporal_stability_harness.py` | `afb024f0baffe58226e933c630b0a6be8cf29939` |

T1–T4 were materialized as temporary local modules for exact execution. Git blob identities matched before and after the complete TASK6 run. T5 identity was verified from its reviewed commit; T5 was not used as a substitute estimator and was not modified.

The committed TASK6 harness intentionally imports local materialized names `t1`, `t2`, `t3`, `t4`; these are execution-time exact frozen materializations, not TASK6-owned rewrites. Reproduction therefore requires materializing the four reviewed blobs above beside the harness before running it. No frozen source copy is committed under TASK6.
