# N1 — Frozen M2 NavigationEvidence Contract Extraction

TASK_ID: TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
FROZEN_M2_COMMIT: 75417cb4356a79e61d1196f3f859fa7cd7ba08e8
FROZEN_M2_BLOB: 5616d5930c8ffca0cef7876d6c192bc7627efb2c

| M2 field | Meaning | Required by frozen M2 | Units | Frame | Validity / use | Existing candidate authority | Current availability |
|---|---|---|---|---|---|---|---|
| target_ref | mission target identity | required whenever navigation is present | identity | N/A | exact equality with M1 target_ref | CurrentTargetManager → HOROS identity | AVAILABLE |
| timestamp | navigation evidence source time | required | seconds | timebase-preserved | finite, not future, <=0.5 s old | HOROS state timestamp | AVAILABLE contractually; exact local call site to verify |
| frame_ref | navigation coordinate frame identity | required | frame id | exact match to M1 frame_ref | no implicit conversion; mismatch suppresses M2 | HOROS local frame metadata | AVAILABLE conceptually; exact runtime string NOT VERIFIED |
| lifecycle | target spatial lifecycle | required for LOST handling | enum | same target state | LOST has explicit M2 semantics | HOROS lifecycle | AVAILABLE |
| metric_status | metric usability status | required and must equal M1 metric_status | enum | same measurement state | VERIFIED / NOT_VERIFIED / UNUSABLE / CONFLICT / INVALID | HOROS metric state / upstream M1 | AVAILABLE; physical VERIFIED may remain conditional |
| observation_age_s | age of underlying observation | required | seconds | N/A | finite, >=0, <=0.5 s | HOROS freshness/timestamp path | AVAILABLE contractually |
| uncertainty_m | scalar positional uncertainty | optional in frozen M2; N1 requires it for VERIFIED active TRACK | metres | same position state | finite, >=0; >5 m degrades | HOROS position covariance | COVARIANCE EXISTS; exact runtime covariance layout/units NOT VERIFIED |
| target_xyz_m | target metric position | required for OBSERVE/TRACK guidance beyond NO_GUIDANCE | metres | frame_ref | finite vec3; not fabricated | HOROS target XYZ | AVAILABLE when metric HOROS state exists |
| carrier_xyz_m | carrier/reference position | required for AVAILABLE TRACK; absence degrades | metres | frame_ref | finite vec3 | carrier-relative HOROS frame origin | AVAILABLE only when frame semantics explicitly prove carrier-relative origin |
| carrier_heading_deg | carrier heading | optional; frozen M2 validates only if present | degrees | unspecified by M2 | finite if present | gps_bridge / MAVLink candidate | NOT REQUIRED; exact authoritative producer/frame NOT VERIFIED; N1 emits None |
| carrier_altitude_m | carrier altitude | optional; frozen M2 validates only if present | metres | unspecified by M2 | finite if present | gps_bridge / MAVLink candidate | NOT REQUIRED; exact authoritative producer/datum NOT VERIFIED; N1 emits None |
| search_relative_vector_m | explicit reacquire/search displacement | required only for REACQUIRE with geometry | metres | frame_ref | finite vec3, VERIFIED geometry | no exact current authoritative producer established | UNAVAILABLE by default; N1 never synthesizes it |
| provenance | contributing source lineage | optional | N/A | N/A | preserved/extended | HOROS / explicit search source | AVAILABLE |

## Frozen M2 branch semantics

- HOLD / ABORT / mission complete do not require NavigationEvidence.
- TRACK / OBSERVE with navigation=None -> DEGRADED / NO_GUIDANCE.
- VERIFIED target XYZ + matching carrier XYZ + acceptable uncertainty -> AVAILABLE / MAINTAIN_OBSERVATION.
- Missing carrier XYZ -> DEGRADED / MAINTAIN_OBSERVATION.
- NOT_VERIFIED metric -> DEGRADED / MAINTAIN_OBSERVATION.
- uncertainty_m > 5.0 -> DEGRADED / MAINTAIN_OBSERVATION.
- REACQUIRE requires explicit search_relative_vector_m for geometry-bearing guidance; N1 does not synthesize it.
- M2 does not derive movement coordinates from target XYZ/carrier XYZ.
