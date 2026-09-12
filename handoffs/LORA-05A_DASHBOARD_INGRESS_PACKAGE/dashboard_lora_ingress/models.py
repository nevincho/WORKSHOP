from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
from tangra_lora_v1 import (
    MessageType, RuntimeState, HQState, DetectorState, CAAuthority,
    IdentityProvenance, TrackingState, ContinuityState,
    PhysicalMetricState, ValidityState, SpatialProvenance,
    DiagnosticType, DiagnosticRecord,
)

@dataclass(frozen=True)
class SystemUpdate:
    runtime_state: RuntimeState
    runtime_uptime_s: int
    cpu_usage: float
    ram_usage: float
    cpu_temperature: float
    runtime_fps: float
    hq_state: HQState
    detector_state: DetectorState
    ca_authority: CAAuthority
    active_track_count: Optional[int] = None

@dataclass(frozen=True)
class TargetUpdate:
    target_ref: bytes
    identity_provenance: IdentityProvenance
    tracking_state: TrackingState
    target_class: Optional[int] = None
    continuity_state: Optional[ContinuityState] = None

@dataclass(frozen=True)
class SpatialUpdate:
    target_ref: bytes
    observation_reference: int
    metric_usable: bool
    physical_metric_state: PhysicalMetricState
    validity: ValidityState
    spatial_provenance: SpatialProvenance
    xyz_m: Optional[Tuple[float, float, float]] = None
    velocity_mps: Optional[Tuple[float, float, float]] = None
    range_m: Optional[float] = None
    uncertainty_m: Optional[float] = None

@dataclass(frozen=True)
class EventUpdate:
    event_type: int
    event_reference: int
    subject_ref: Optional[bytes] = None
    payload: Optional[bytes] = None

@dataclass(frozen=True)
class DiagnosticUpdate:
    diagnostic_type: DiagnosticType
    records: tuple[DiagnosticRecord, ...]

@dataclass(frozen=True)
class LinkUpdate:
    link_state: str
    last_valid_age: Optional[float]
    valid_packets: int
    invalid_packets: int
    duplicates: int
    out_of_order: int
    inferred_missing_packets: int
    session_changes: int

@dataclass(frozen=True)
class DashboardStateUpdate:
    source_id: int
    session_id: Optional[int]
    message_class: Optional[MessageType]
    receive_time: float
    transport: str = 'LORA'
    system: Optional[SystemUpdate] = None
    target: Optional[TargetUpdate] = None
    spatial: Optional[SpatialUpdate] = None
    event: Optional[EventUpdate] = None
    diagnostic: Optional[DiagnosticUpdate] = None
    link: Optional[LinkUpdate] = None
