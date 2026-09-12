from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional, Union

MAX_REF_LEN = 16
MAX_TARGET_REF_LEN = 32
MAX_EVENT_PAYLOAD = 128
MAX_DIAG_RECORDS = 8

class MessageType(IntEnum):
    HEARTBEAT = 1
    TARGET = 2
    SPATIAL = 3
    EVENT = 4
    DIAGNOSTIC = 5

class RuntimeState(IntEnum):
    UNKNOWN = 0; STARTING = 1; RUNNING = 2; STOPPED = 3; ERROR = 4
class HQState(IntEnum):
    UNKNOWN = 0; AVAILABLE = 1; UNAVAILABLE = 2; ERROR = 3
class DetectorState(IntEnum):
    UNKNOWN = 0; AVAILABLE = 1; UNAVAILABLE = 2; ERROR = 3
class CAAuthority(IntEnum):
    UNKNOWN = 0; CA_PRIMARY = 1; OTHER = 2
class TrackingState(IntEnum):
    UNKNOWN = 0; DETECTED = 1; TRACKING = 2; LOST = 3
class ContinuityState(IntEnum):
    UNKNOWN = 0; ACTIVE = 1; HELD = 2; LOST = 3
class ValidityState(IntEnum):
    UNKNOWN = 0; VALID = 1; INVALID = 2; DEGRADED = 3
class PhysicalMetricState(IntEnum):
    UNKNOWN = 0; PHYSICAL = 1; PROVISIONAL = 2; NON_PHYSICAL = 3; UNAVAILABLE = 4
class IdentityProvenance(IntEnum):
    UNKNOWN = 0; GLOBAL_OBJECT_UID = 1; CURRENT_TARGET_ID = 2; OBJECT_ID = 3; GLOBAL_TRACK_UID = 4; OTHER = 255
class SpatialProvenance(IntEnum):
    UNKNOWN = 0; HOROS = 1; MONOCULAR_CLASS_SIZE = 2; RANGE_ESTIMATOR = 3; OTHER = 255
class DiagnosticType(IntEnum):
    RUNTIME_TIMING = 1; HAILO_TIMING = 2; HOROS_STATUS = 3; TELEMETRY_ERROR = 4; METRIC_CONTEXT = 5
class DiagnosticMetric(IntEnum):
    LOOP_MS_X10 = 1; CAPTURE_MS_X10 = 2; DETECTOR_MS_X10 = 3; TRACKER_MS_X10 = 4
    HAILO_INFERENCE_MS_X10 = 16; HAILO_PRE_MS_X10 = 17; HAILO_POST_MS_X10 = 18
    HOROS_ERROR_COUNT = 32; HOROS_DEGRADED_CODE = 33
    TELEMETRY_ERROR_CODE = 48; METRIC_CONTEXT_CODE = 64

@dataclass(frozen=True)
class EnvelopeMeta:
    source_id: int
    session_id: int
    sequence: int
    source_uptime_s: int
    source_timestamp_ms: Optional[int] = None

@dataclass(frozen=True)
class Heartbeat:
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
class Target:
    target_ref: bytes
    identity_provenance: IdentityProvenance
    tracking_state: TrackingState
    target_class: Optional[int] = None
    continuity_state: Optional[ContinuityState] = None

@dataclass(frozen=True)
class Spatial:
    target_ref: bytes
    observation_reference: int
    metric_usable: bool
    physical_metric_state: PhysicalMetricState
    validity: ValidityState
    spatial_provenance: SpatialProvenance
    xyz_m: Optional[tuple[float, float, float]] = None
    velocity_mps: Optional[tuple[float, float, float]] = None
    range_m: Optional[float] = None
    uncertainty_m: Optional[float] = None

@dataclass(frozen=True)
class Event:
    event_type: int
    event_reference: int
    subject_ref: Optional[bytes] = None
    payload: Optional[bytes] = None

@dataclass(frozen=True)
class DiagnosticRecord:
    metric: DiagnosticMetric
    value: int

@dataclass(frozen=True)
class Diagnostic:
    diagnostic_type: DiagnosticType
    records: tuple[DiagnosticRecord, ...] = field(default_factory=tuple)

SemanticMessage = Union[Heartbeat, Target, Spatial, Event, Diagnostic]

@dataclass(frozen=True)
class DecodedPacket:
    meta: EnvelopeMeta
    message_type: MessageType
    message: SemanticMessage

@dataclass(frozen=True)
class DecodeResult:
    ok: bool
    packet: Optional[DecodedPacket] = None
    error: Optional[str] = None
