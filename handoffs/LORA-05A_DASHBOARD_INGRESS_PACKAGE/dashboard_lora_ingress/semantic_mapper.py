from __future__ import annotations
from tangra_lora_v1 import Heartbeat, Target, Spatial, Event, Diagnostic, DecodedPacket, MessageType
from .models import (
    DashboardStateUpdate, SystemUpdate, TargetUpdate, SpatialUpdate,
    EventUpdate, DiagnosticUpdate,
)

class SemanticIngressRouter:
    """Pure mapping boundary. It does not infer authority or synthesize missing values."""
    def map_packet(self, packet: DecodedPacket, receive_time: float) -> DashboardStateUpdate:
        m = packet.message
        common = dict(
            source_id=packet.meta.source_id,
            session_id=packet.meta.session_id,
            message_class=packet.message_type,
            receive_time=float(receive_time),
        )
        if packet.message_type == MessageType.HEARTBEAT:
            assert isinstance(m, Heartbeat)
            return DashboardStateUpdate(**common, system=SystemUpdate(
                m.runtime_state, m.runtime_uptime_s, m.cpu_usage, m.ram_usage,
                m.cpu_temperature, m.runtime_fps, m.hq_state, m.detector_state,
                m.ca_authority, m.active_track_count,
            ))
        if packet.message_type == MessageType.TARGET:
            assert isinstance(m, Target)
            return DashboardStateUpdate(**common, target=TargetUpdate(
                bytes(m.target_ref), m.identity_provenance, m.tracking_state,
                m.target_class, m.continuity_state,
            ))
        if packet.message_type == MessageType.SPATIAL:
            assert isinstance(m, Spatial)
            return DashboardStateUpdate(**common, spatial=SpatialUpdate(
                bytes(m.target_ref), m.observation_reference, m.metric_usable,
                m.physical_metric_state, m.validity, m.spatial_provenance,
                m.xyz_m, m.velocity_mps, m.range_m, m.uncertainty_m,
            ))
        if packet.message_type == MessageType.EVENT:
            assert isinstance(m, Event)
            return DashboardStateUpdate(**common, event=EventUpdate(
                m.event_type, m.event_reference,
                None if m.subject_ref is None else bytes(m.subject_ref),
                None if m.payload is None else bytes(m.payload),
            ))
        if packet.message_type == MessageType.DIAGNOSTIC:
            assert isinstance(m, Diagnostic)
            return DashboardStateUpdate(**common, diagnostic=DiagnosticUpdate(
                m.diagnostic_type, tuple(m.records),
            ))
        raise ValueError(f'unsupported message type {packet.message_type!r}')
