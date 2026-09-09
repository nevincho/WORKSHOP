# M1 Integration Handoff

TASK_ID: TASK-TANGRA-MISSION-CONTEXT-AUTHORITY-MC1-20260909

No production integration is authorized.

The future integration site must obtain a MissionContext snapshot only from explicit authoritative setters, call map_to_m1_context(), and map exactly four values into frozen M1.

If mapping.authoritative is True:
- mission_active = mapping.mission_active
- operator_intent = frozen_m1.OperatorIntent(mapping.operator_intent.value)
- system_ready = mapping.system_ready
- safety_available = mapping.safety_available

If mapping.authoritative is False:
use the returned fail-closed values exactly. Do not substitute target presence, detector/HOROS state, T7 advisory, connectivity, UI state, generic ACTIVE, or generated telemetry.

Other frozen M1 inputs (target_ref, timestamp, frame_ref, lifecycle, XYZ/Vxyz/covariance/prediction, metric_status, target_class, observation_age_s, provenance, carrier_pose) remain owned by their existing upstream contracts and are outside this package.

No M1/M2 modification is required or allowed by this handoff.
