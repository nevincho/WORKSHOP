from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
import math

class FrameSemantics(str, Enum):
    CARRIER_RELATIVE_LOCAL_METRIC = "CARRIER_RELATIVE_LOCAL_METRIC"

class MetricStatus(str, Enum):
    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNUSABLE = "UNUSABLE"
    CONFLICT = "CONFLICT"
    INVALID = "INVALID"

class Lifecycle(str, Enum):
    OBSERVED = "OBSERVED"
    ESTIMATED = "ESTIMATED"
    PREDICTED = "PREDICTED"
    COASTING = "COASTING"
    DEGRADED = "DEGRADED"
    LOST = "LOST"

COVARIANCE_SEMANTICS = "POSITION_COVARIANCE_3X3_M2"
CONTRACT_VERSION = "M2_NAVIGATION_EVIDENCE_N1_V1"

@dataclass(frozen=True)
class HorosTargetNavigationSource:
    target_ref: str
    timestamp: float
    frame_ref: str
    frame_semantics: FrameSemantics
    lifecycle: Lifecycle
    metric_status: MetricStatus
    observation_age_s: float
    target_xyz_m: Optional[Tuple[float, float, float]]
    position_covariance_m2: Optional[Tuple[float, ...]]
    covariance_semantics: Optional[str]
    carrier_origin_is_zero: bool
    provenance: Tuple[Tuple[str, str], ...] = ()
    production_authority: bool = False

@dataclass(frozen=True)
class ExplicitSearchGeometry:
    target_ref: str
    timestamp: float
    frame_ref: str
    metric_status: MetricStatus
    relative_vector_m: Tuple[float, float, float]
    provenance: Tuple[Tuple[str, str], ...] = ()
    production_authority: bool = False

@dataclass(frozen=True)
class NavigationAdapterPolicy:
    stale_after_s: float = 0.5

@dataclass(frozen=True)
class NavigationAdapterResult:
    m2_kwargs: Optional[Tuple[Tuple[str, object], ...]]
    usable_for_active_track: bool
    reason: str
    provenance: Tuple[Tuple[str, str], ...]
    production_authority: bool = False
    contract_version: str = CONTRACT_VERSION

    def as_dict(self):
        return None if self.m2_kwargs is None else dict(self.m2_kwargs)

def _finite_number(value) -> bool:
    return type(value) in (int, float) and not isinstance(value, bool) and math.isfinite(float(value))

def _finite_vec3(value) -> bool:
    return type(value) is tuple and len(value) == 3 and all(_finite_number(v) for v in value)

def _valid_ref(value) -> bool:
    return type(value) is str and bool(value.strip())

def _valid_provenance(value) -> bool:
    return type(value) is tuple and all(type(item) is tuple and len(item) == 2 and type(item[0]) is str and type(item[1]) is str for item in value)

def _covariance_uncertainty_m(covariance, semantics) -> Optional[float]:
    if covariance is None or type(semantics) is not str or semantics != COVARIANCE_SEMANTICS:
        return None
    if type(covariance) is not tuple or len(covariance) != 9:
        return None
    if not all(_finite_number(v) for v in covariance):
        return None
    p = tuple(float(v) for v in covariance)
    if p[1] != p[3] or p[2] != p[6] or p[5] != p[7]:
        return None
    if p[0] < 0 or p[4] < 0 or p[8] < 0:
        return None
    if p[0]*p[4] - p[1]*p[1] < -1e-12:
        return None
    if p[0]*p[8] - p[2]*p[2] < -1e-12:
        return None
    if p[4]*p[8] - p[5]*p[5] < -1e-12:
        return None
    det = p[0]*(p[4]*p[8]-p[5]*p[7]) - p[1]*(p[3]*p[8]-p[5]*p[6]) + p[2]*(p[3]*p[7]-p[4]*p[6])
    if det < -1e-12:
        return None
    return math.sqrt(max(0.0, p[0] + p[4] + p[8]))

def build_m2_navigation_evidence(source: HorosTargetNavigationSource, expected_target_ref: str, expected_frame_ref: str, evaluated_at: float, search: Optional[ExplicitSearchGeometry] = None, policy: NavigationAdapterPolicy = NavigationAdapterPolicy()) -> NavigationAdapterResult:
    fallback_prov = (("n1", "M2_NAVIGATION_EVIDENCE_ADAPTER"),)
    if type(source) is not HorosTargetNavigationSource:
        return NavigationAdapterResult(None, False, "horos_source_required", fallback_prov)
    if not _valid_provenance(source.provenance):
        return NavigationAdapterResult(None, False, "source_provenance_invalid", fallback_prov)
    base_prov = source.provenance + fallback_prov

    def fail(reason):
        return NavigationAdapterResult(None, False, reason, base_prov)

    if type(policy) is not NavigationAdapterPolicy or not _finite_number(policy.stale_after_s) or policy.stale_after_s < 0 or policy.stale_after_s > 0.5:
        return fail("invalid_freshness_policy")
    if not _valid_ref(expected_target_ref):
        return fail("expected_target_ref_invalid")
    if not _valid_ref(expected_frame_ref):
        return fail("expected_frame_ref_invalid")
    if source.production_authority is not False:
        return fail("authoritative_source_flag_rejected")
    if not _valid_ref(source.target_ref) or source.target_ref != expected_target_ref:
        return fail("target_identity_mismatch")
    if not _valid_ref(source.frame_ref) or source.frame_ref != expected_frame_ref:
        return fail("frame_mismatch")
    if type(source.frame_semantics) is not FrameSemantics or source.frame_semantics is not FrameSemantics.CARRIER_RELATIVE_LOCAL_METRIC:
        return fail("unsupported_frame_semantics")
    if source.carrier_origin_is_zero is not True:
        return fail("carrier_origin_not_authoritative")
    if type(source.lifecycle) is not Lifecycle or type(source.metric_status) is not MetricStatus:
        return fail("invalid_state_enum")
    if not _finite_number(source.timestamp) or not _finite_number(evaluated_at):
        return fail("malformed_timestamp")
    age = float(evaluated_at) - float(source.timestamp)
    if age < 0 or age > policy.stale_after_s:
        return fail("stale_horos_evidence")
    if not _finite_number(source.observation_age_s) or source.observation_age_s < 0 or source.observation_age_s > policy.stale_after_s:
        return fail("stale_or_unknown_observation")

    target_xyz = source.target_xyz_m
    if source.lifecycle is Lifecycle.LOST:
        target_xyz = None
    elif target_xyz is not None and not _finite_vec3(target_xyz):
        return fail("malformed_target_xyz")
    elif source.metric_status is MetricStatus.VERIFIED and target_xyz is None:
        return fail("verified_target_xyz_missing")

    uncertainty = None
    if source.metric_status is MetricStatus.VERIFIED and source.lifecycle is not Lifecycle.LOST:
        uncertainty = _covariance_uncertainty_m(source.position_covariance_m2, source.covariance_semantics)
        if uncertainty is None:
            return fail("verified_covariance_unavailable_or_invalid")
    elif source.position_covariance_m2 is not None:
        uncertainty = _covariance_uncertainty_m(source.position_covariance_m2, source.covariance_semantics)
        if uncertainty is None:
            return fail("malformed_covariance")

    search_vec = None
    provenance = base_prov
    if search is not None:
        if type(search) is not ExplicitSearchGeometry:
            return fail("search_geometry_type_invalid")
        if search.production_authority is not False:
            return fail("authoritative_search_flag_rejected")
        if not _valid_ref(search.target_ref) or search.target_ref != source.target_ref:
            return fail("search_target_mismatch")
        if not _valid_ref(search.frame_ref) or search.frame_ref != source.frame_ref:
            return fail("search_frame_mismatch")
        if search.metric_status is not MetricStatus.VERIFIED:
            return fail("search_metric_not_verified")
        if not _finite_number(search.timestamp) or float(evaluated_at)-float(search.timestamp) < 0 or float(evaluated_at)-float(search.timestamp) > policy.stale_after_s:
            return fail("stale_search_geometry")
        if not _finite_vec3(search.relative_vector_m):
            return fail("malformed_search_vector")
        if not _valid_provenance(search.provenance):
            return fail("search_provenance_invalid")
        search_vec = tuple(float(v) for v in search.relative_vector_m)
        provenance += search.provenance

    kwargs = (("target_ref", source.target_ref),("timestamp", float(source.timestamp)),("frame_ref", source.frame_ref),("lifecycle", source.lifecycle.value),("metric_status", source.metric_status.value),("observation_age_s", float(source.observation_age_s)),("uncertainty_m", uncertainty),("target_xyz_m", None if target_xyz is None else tuple(float(v) for v in target_xyz)),("carrier_xyz_m", (0.0,0.0,0.0)),("carrier_heading_deg", None),("carrier_altitude_m", None),("search_relative_vector_m", search_vec),("provenance", provenance))
    usable = source.lifecycle is not Lifecycle.LOST and source.metric_status is MetricStatus.VERIFIED and target_xyz is not None and uncertainty is not None
    return NavigationAdapterResult(kwargs, usable, "navigation_evidence_ready" if usable else "navigation_evidence_nonactive", provenance)
