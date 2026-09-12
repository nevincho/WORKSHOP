# LORA-04 — Source Binding Gate

Status: BLOCKED AT FIRST GATE / NO IMPLEMENTATION STARTED
Date: 2026-09-12

## Reason
LORA-04 requires inspection of the current authoritative TANGRA development source and exact binding of every transmitted field to an existing source file and symbol before adapter implementation.

The connected repositories available in this Workshop are documentation/evidence repositories (`nevincho/TANGRA-DOCS`, `nevincho/TANGRA-2.0`) and `nevincho/WORKSHOP`. The current implementation authority remains the local engineering workspace `D:\RaspberryPi5\TANGRA\...` and the Pi runtime `/home/khan/ai-drone/droneguard_1_0`; that source is not accessible through the present Workshop tools.

Canonical telemetry evidence confirms semantic availability of several fields, but it does not prove exact current source-file/symbol bindings for the authoritative development copy. Therefore none of those fields may be promoted to `VERIFIED_BINDING` solely from documentation.

## Source binding table

| FIELD | SOURCE FILE | SOURCE SYMBOL/FIELD | SEMANTIC STATUS | BINDING STATUS |
|---|---|---|---|---|
| runtime_state | current development source not inspectable | documented telemetry: `ai_status`, `droneguard_status`, `runtime_controller_state`, `system_status`, Runtime Controller `state` | AVAILABLE | NOT_VERIFIED |
| runtime_uptime | current development source not inspectable | documented telemetry: `runtime_uptime_sec`, `dashboard_state.system.tangra_uptime_sec` | AVAILABLE | NOT_VERIFIED |
| cpu_usage | current development source not inspectable | `cpu_usage` | AVAILABLE; exact system/process semantic not independently proven | NOT_VERIFIED |
| ram_usage | current development source not inspectable | `ram_usage` | AVAILABLE; exact unit/system semantic not independently proven | NOT_VERIFIED |
| cpu_temperature | current development source not inspectable | `cpu_temp` | AVAILABLE | NOT_VERIFIED |
| runtime_fps | current development source not inspectable | `fps` | AVAILABLE | NOT_VERIFIED |
| hq_state | current development source not inspectable | `camera_status`, Runtime Controller `camera_status` | AVAILABLE | NOT_VERIFIED |
| detector_state | current development source not inspectable | `detector_backend`, `hailo_status`, Runtime Controller `hailo` | AVAILABLE | NOT_VERIFIED |
| ca_authority | current development source not inspectable | `kalman_algorithm=CA_KALMAN_PRIMARY`, `tracking_authority=UPSTREAM_CA_KALMAN` | AVAILABLE authority/config identity | NOT_VERIFIED |
| active_track_count | current development source not inspectable | `active_trackers` | AVAILABLE / optional | OPTIONAL_AVAILABLE but exact binding NOT_VERIFIED |
| target_ref | current development source not inspectable | documented continuity precedence: `global_object_uid → current_target_id → object_id → global_track_uid → id`; CurrentTargetManager is mission continuity authority | semantic authority documented | NOT_VERIFIED |
| identity_provenance | current development source not inspectable | derived only from whichever verified continuity field is actually bound | contractually required with target_ref | NOT_VERIFIED |
| target_class | current development source not inspectable | exact authoritative current field not established by accessible evidence | optional | NOT_VERIFIED |
| tracking_state | current development source not inspectable | exact authoritative current field not established by accessible evidence | required TARGET semantic | NOT_VERIFIED |
| continuity_state | current development source not inspectable | no authoritative CurrentTargetManager state/freshness exposed in HB-00 surface | optional | SOURCE_GAP / OMIT |
| spatial target_ref | current development source not inspectable | must match verified target identity source | required | NOT_VERIFIED |
| observation_reference | current development source not inspectable | HOROS frame/observation reference exact symbol not proven | required | NOT_VERIFIED |
| xyz | current development source not inspectable | HOROS maintains XYZ | semantic source documented; validity-gated | NOT_VERIFIED |
| velocity | current development source not inspectable | HOROS maintains Vxyz | optional semantic source documented | NOT_VERIFIED |
| range | current development source not inspectable | HOROS provenance / `input_range_m`; class-size range path documented | AVAILABLE when valid | NOT_VERIFIED |
| metric_usable | current development source not inspectable | `metric_usable` | AVAILABLE | NOT_VERIFIED |
| physical_metric_state | current development source not inspectable | `physical_metric_state` | AVAILABLE | NOT_VERIFIED |
| validity | current development source not inspectable | documented metric/range validity | AVAILABLE | NOT_VERIFIED |
| uncertainty | current development source not inspectable | HOROS maintains covariance/uncertainty; exact export symbol not proven | optional | NOT_VERIFIED |
| spatial_provenance | current development source not inspectable | HOROS provenance / range provenance | AVAILABLE semantic context | NOT_VERIFIED |
| EVENT bindings | current development source not inspectable | no stable transition source can be safely bound without current source inspection | optional capability | NOT_VERIFIED |
| DIAGNOSTIC bindings | current development source not inspectable | `runtime_profile.*`, `hailo_inference_ms`, HOROS errors are documented available | optional | OPTIONAL_AVAILABLE but exact binding NOT_VERIFIED |

## Adapter-owned metadata

The following do not require DroneGuard source creation and remain valid design choices once source binding is unblocked:

- `source_id`: adapter configuration, stable per node, not target/tracking/radio identity.
- `session_id`: adapter-owned u32 session token changed on adapter/runtime session restart; no synchronized clock required.
- `sequence`: adapter-owned single global u16 sequence per `(source_id, session_id)`, increment every emitted packet, wrap `65535 → 0`.

No implementation was created because the FIRST GATE failed before adapter construction.

## Evidence consulted

- `TANGRA-DOCS/REPORTS/TANGRA_TELEMETRY_SIGNAL_REFERENCE_20260912.md`
- `TANGRA-DOCS/CURRENT_BASELINE.md`
- LORA-02 accepted protocol/codec package
- LORA-03 accepted receiver semantics package

## Protected-boundary result

No DroneGuard, Dashboard, HTTP, WIDE, HQ, detector, NanoTracker, CA, CurrentTarget, HOROS, Range, command, IFF, readiness, actuation, or production file was modified.

## Required unblock

Provide Workshop/Codex read access to the current authoritative development source rooted at `D:\RaspberryPi5\TANGRA\...` (or an exact read-only source snapshot of the relevant runtime files). Then rerun only the LORA-04 FIRST GATE, bind each required field to current source file + symbol, and proceed with adapter implementation only if required bindings pass.
