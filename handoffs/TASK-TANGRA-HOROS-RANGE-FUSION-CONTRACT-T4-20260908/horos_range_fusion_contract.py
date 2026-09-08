from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from math import isfinite, sqrt
from time import perf_counter_ns
from typing import Optional, Tuple


class EvidenceValidity(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    INVALID = "INVALID"


class MetricUsability(str, Enum):
    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNUSABLE = "UNUSABLE"


class FusionState(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    CONFLICT = "CONFLICT"
    INVALID = "INVALID"


@dataclass(frozen=True)
class RangeEvidence:
    source_type: str
    source_version: str
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_ref: Optional[str]
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: Optional[float]
    validity: EvidenceValidity
    metric_usability: MetricUsability
    independence_group: str
    calibration_status: str = "NOT_APPLICABLE"
    transform_status: str = "NOT_APPLICABLE"
    provenance: Tuple[Tuple[str, str], ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class RejectedEvidence:
    source_type: str
    source_version: str
    reason: str
    provenance: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class HorosRangeObservation:
    contract_id: str
    contract_version: str
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_ref: Optional[str]
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: float
    validity: EvidenceValidity
    metric_usability: MetricUsability
    state: FusionState
    contributing_sources: Tuple[str, ...]
    rejected_sources: Tuple[RejectedEvidence, ...]
    conflict: bool
    provenance: Tuple[Tuple[str, str], ...]
    processing_time_ms: float
    reason: str = ""


@dataclass(frozen=True)
class FusionConfig:
    max_relative_pair_disagreement: float = 0.30
    max_normalized_residual: float = 3.0
    degrade_relative_disagreement: float = 0.10
    degrade_normalized_residual: float = 1.5
    uncertainty_floor_relative: float = 0.01
    min_confidence: float = 0.05

    def validate(self) -> None:
        vals = (self.max_relative_pair_disagreement, self.max_normalized_residual,
                self.degrade_relative_disagreement, self.degrade_normalized_residual,
                self.uncertainty_floor_relative, self.min_confidence)
        if not all(isfinite(float(v)) for v in vals):
            raise ValueError("malformed_config")
        if not (0.0 < self.max_relative_pair_disagreement < 2.0):
            raise ValueError("malformed_config")
        if not (0.0 < self.max_normalized_residual):
            raise ValueError("malformed_config")
        if not (0.0 < self.degrade_relative_disagreement < self.max_relative_pair_disagreement):
            raise ValueError("malformed_config")
        if not (0.0 < self.degrade_normalized_residual < self.max_normalized_residual):
            raise ValueError("malformed_config")
        if self.uncertainty_floor_relative < 0.0:
            raise ValueError("malformed_config")
        if not (0.0 < self.min_confidence <= 1.0):
            raise ValueError("malformed_config")


@dataclass(frozen=True)
class ExistingMonocularClassSizeInput:
    source_version: str
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: Optional[float]
    valid: bool
    metric_verified: bool
    frame_id: Optional[str] = None
    timestamp: Optional[float] = None
    target_ref: Optional[str] = None
    independence_group: str = "MONOCULAR_CLASS_SIZE"
    provenance: Tuple[Tuple[str, str], ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class SparseGeometryRangeInput:
    source_version: str
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: Optional[float]
    valid: bool
    production_metric_verified: bool
    transform_valid: bool
    transform_production_verified: bool
    frame_id: Optional[str] = None
    timestamp: Optional[float] = None
    target_ref: Optional[str] = None
    independence_group: str = "SPARSE_TARGET_GEOMETRY_RANGE"
    provenance: Tuple[Tuple[str, str], ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class LosRangeCompatible:
    measurement_type: str
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: float
    valid: bool
    metric_usable: bool
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_ref: Optional[str]
    provenance: Tuple[Tuple[str, str], ...]
    bearing: None = None
    los: None = None
    reason: str = ""


def adapt_monocular_class_size(src: ExistingMonocularClassSizeInput) -> RangeEvidence:
    return RangeEvidence(
        source_type="MONOCULAR_CLASS_SIZE",
        source_version=src.source_version,
        frame_id=src.frame_id,
        timestamp=src.timestamp,
        target_ref=src.target_ref,
        range_m=src.range_m,
        sigma_m=src.sigma_m,
        confidence=src.confidence,
        validity=EvidenceValidity.VALID if src.valid else EvidenceValidity.INVALID,
        metric_usability=MetricUsability.VERIFIED if src.metric_verified else MetricUsability.NOT_VERIFIED,
        independence_group=src.independence_group,
        provenance=src.provenance + (("adapter", "MONOCULAR_CLASS_SIZE_TO_RANGE_EVIDENCE"),),
        reason=src.reason,
    )


def adapt_sparse_geometry(src: SparseGeometryRangeInput) -> RangeEvidence:
    if not src.valid:
        validity = EvidenceValidity.INVALID
    elif src.production_metric_verified:
        validity = EvidenceValidity.VALID
    else:
        validity = EvidenceValidity.DEGRADED
    if not src.transform_valid:
        usability = MetricUsability.UNUSABLE
    elif src.production_metric_verified and src.transform_production_verified:
        usability = MetricUsability.VERIFIED
    else:
        usability = MetricUsability.NOT_VERIFIED
    return RangeEvidence(
        source_type="SPARSE_TARGET_GEOMETRY_RANGE",
        source_version=src.source_version,
        frame_id=src.frame_id,
        timestamp=src.timestamp,
        target_ref=src.target_ref,
        range_m=src.range_m,
        sigma_m=src.sigma_m,
        confidence=src.confidence,
        validity=validity,
        metric_usability=usability,
        independence_group=src.independence_group,
        calibration_status="VERIFIED" if src.production_metric_verified else "NOT_VERIFIED",
        transform_status="VERIFIED" if src.transform_production_verified else ("INVALID" if not src.transform_valid else "NOT_VERIFIED"),
        provenance=src.provenance + (("adapter", "TASK3_TO_RANGE_EVIDENCE"),),
        reason=src.reason,
    )


class HorosRangeFusionContract:
    CONTRACT_ID = "HOROS_RANGE_FUSION_SHADOW"
    CONTRACT_VERSION = "1.0"

    def __init__(self, config: FusionConfig | None = None) -> None:
        self.config = config or FusionConfig()

    def fuse(self, inputs: Tuple[RangeEvidence, ...]) -> HorosRangeObservation:
        t0 = perf_counter_ns()
        try:
            self.config.validate()
        except Exception as exc:
            return self._invalid(t0, (), str(exc))

        normalized = []
        rejected = []
        for e in inputs:
            ok, reason = self._usable(e)
            if not ok:
                rejected.append(RejectedEvidence(e.source_type, e.source_version, reason, e.provenance))
            else:
                normalized.append(e)

        if not normalized:
            return self._invalid(t0, tuple(rejected), "no_usable_range_evidence")
        if self._has_context_conflict([e.target_ref for e in normalized]):
            return self._invalid(t0, tuple(rejected), "target_reference_conflict")
        if self._has_context_conflict([e.frame_id for e in normalized]):
            return self._invalid(t0, tuple(rejected), "frame_reference_conflict")

        groups: dict[str, list[RangeEvidence]] = {}
        for e in normalized:
            groups.setdefault(e.independence_group, []).append(e)
        independent = []
        for group in sorted(groups):
            members = groups[group]
            chosen = min(members, key=self._effective_sigma)
            independent.append(chosen)
            for e in members:
                if e is not chosen:
                    rejected.append(RejectedEvidence(e.source_type, e.source_version, "correlated_duplicate_not_counted", e.provenance))

        frame_id = self._consensus_optional([e.frame_id for e in independent])
        target_ref = self._consensus_optional([e.target_ref for e in independent])
        timestamp = self._latest_timestamp(independent)

        if len(independent) == 1:
            e = independent[0]
            metric = e.metric_usability
            validity = EvidenceValidity.VALID if (e.validity == EvidenceValidity.VALID and metric == MetricUsability.VERIFIED) else EvidenceValidity.DEGRADED
            state = FusionState.VALID if validity == EvidenceValidity.VALID else FusionState.DEGRADED
            sigma = max(float(e.sigma_m), abs(float(e.range_m)) * self.config.uncertainty_floor_relative)
            return HorosRangeObservation(self.CONTRACT_ID, self.CONTRACT_VERSION, frame_id, timestamp, target_ref, float(e.range_m), sigma, float(e.confidence), validity, metric, state, (self._source_label(e),), tuple(rejected), False, e.provenance + (("fusion", "single_source_passthrough"),), (perf_counter_ns()-t0)/1e6)

        conflict = self._conflict(independent)
        if conflict:
            z_center = sum(float(e.range_m) for e in independent) / len(independent)
            spread = max(abs(float(e.range_m) - z_center) for e in independent)
            sigma = max(spread, max(float(e.sigma_m) for e in independent), abs(z_center)*self.config.uncertainty_floor_relative)
            return HorosRangeObservation(self.CONTRACT_ID, self.CONTRACT_VERSION, frame_id, timestamp, target_ref, None, sigma, min(float(e.confidence) for e in independent), EvidenceValidity.DEGRADED, self._aggregate_metric(independent), FusionState.CONFLICT, tuple(self._source_label(e) for e in independent), tuple(rejected), True, self._collect_provenance(independent) + (("fusion", "unresolved_conflict_no_range_selected"),), (perf_counter_ns()-t0)/1e6, "independent_source_conflict")

        weights=[]; ranges=[]
        for e in independent:
            eff_sigma=self._effective_sigma(e); weights.append(float(e.confidence)/(eff_sigma*eff_sigma)); ranges.append(float(e.range_m))
        wsum=sum(weights)
        if not isfinite(wsum) or wsum <= 0:
            return self._invalid(t0, tuple(rejected), "invalid_fusion_weights")
        z=sum(w*r for w,r in zip(weights,ranges))/wsum
        formal_sigma=sqrt(1.0/wsum)
        disagreement_sigma=sqrt(sum(w*(r-z)**2 for w,r in zip(weights,ranges))/wsum)
        sigma=max(formal_sigma, disagreement_sigma, abs(z)*self.config.uncertainty_floor_relative)
        metric=self._aggregate_metric(independent)
        soft_disagreement=self._soft_disagreement(independent)
        all_verified=metric==MetricUsability.VERIFIED and all(e.validity==EvidenceValidity.VALID for e in independent)
        fully_valid=all_verified and not soft_disagreement
        state=FusionState.VALID if fully_valid else FusionState.DEGRADED
        validity=EvidenceValidity.VALID if fully_valid else EvidenceValidity.DEGRADED
        confidence=min(1.0,sum(float(e.confidence) for e in independent)/len(independent))
        return HorosRangeObservation(self.CONTRACT_ID,self.CONTRACT_VERSION,frame_id,timestamp,target_ref,z,sigma,confidence,validity,metric,state,tuple(self._source_label(e) for e in independent),tuple(rejected),False,self._collect_provenance(independent)+(("fusion","compatible_independent_uncertainty_weighted"),),(perf_counter_ns()-t0)/1e6)

    def _usable(self,e):
        if not e.source_type or not e.source_version or not e.independence_group: return False,"malformed_evidence_identity"
        if e.validity==EvidenceValidity.INVALID: return False,e.reason or "source_invalid"
        if e.metric_usability==MetricUsability.UNUSABLE: return False,e.reason or "metric_unusable"
        if e.range_m is None or e.sigma_m is None or e.confidence is None: return False,"missing_range_uncertainty_or_confidence"
        vals=(e.range_m,e.sigma_m,e.confidence)
        if not all(isfinite(float(v)) for v in vals): return False,"non_finite_range_uncertainty_or_confidence"
        if e.range_m<=0 or e.sigma_m<=0: return False,"non_positive_range_or_uncertainty"
        if not (0.0<e.confidence<=1.0) or e.confidence<self.config.min_confidence: return False,"invalid_or_too_low_confidence"
        return True,""

    def _effective_sigma(self,e): return float(e.sigma_m)/sqrt(max(float(e.confidence),self.config.min_confidence))

    def _conflict(self,es):
        for i in range(len(es)):
            for j in range(i+1,len(es)):
                a,b=es[i],es[j]; za,zb=float(a.range_m),float(b.range_m)
                rel=abs(za-zb)/max((za+zb)*.5,1e-12)
                combined=sqrt(self._effective_sigma(a)**2+self._effective_sigma(b)**2)
                nr=abs(za-zb)/max(combined,1e-12)
                if rel>self.config.max_relative_pair_disagreement and nr>self.config.max_normalized_residual: return True
        return False

    def _soft_disagreement(self,es):
        for i in range(len(es)):
            for j in range(i+1,len(es)):
                a,b=es[i],es[j]; za,zb=float(a.range_m),float(b.range_m)
                rel=abs(za-zb)/max((za+zb)*.5,1e-12)
                combined=sqrt(self._effective_sigma(a)**2+self._effective_sigma(b)**2)
                nr=abs(za-zb)/max(combined,1e-12)
                if rel>self.config.degrade_relative_disagreement or nr>self.config.degrade_normalized_residual: return True
        return False

    @staticmethod
    def _has_context_conflict(values):
        vals=[v for v in values if v is not None]
        return len(set(vals))>1

    @staticmethod
    def _aggregate_metric(es):
        if any(e.metric_usability==MetricUsability.UNUSABLE for e in es): return MetricUsability.UNUSABLE
        if all(e.metric_usability==MetricUsability.VERIFIED for e in es): return MetricUsability.VERIFIED
        return MetricUsability.NOT_VERIFIED
    @staticmethod
    def _source_label(e): return f"{e.source_type}:{e.source_version}"
    @staticmethod
    def _collect_provenance(es):
        out=[]
        for e in es: out.extend(e.provenance); out.append(("contributor",f"{e.source_type}:{e.source_version}"))
        return tuple(out)
    @staticmethod
    def _consensus_optional(values):
        vals=[v for v in values if v is not None]
        if not vals: return None
        return vals[0] if all(v==vals[0] for v in vals) else None
    @staticmethod
    def _latest_timestamp(es):
        vals=[float(e.timestamp) for e in es if e.timestamp is not None and isfinite(float(e.timestamp))]
        return max(vals) if vals else None
    def _invalid(self,t0,rejected,reason):
        return HorosRangeObservation(self.CONTRACT_ID,self.CONTRACT_VERSION,None,None,None,None,None,0.0,EvidenceValidity.INVALID,MetricUsability.UNUSABLE,FusionState.INVALID,(),tuple(rejected),False,(("fusion","invalid"),),(perf_counter_ns()-t0)/1e6,reason)


def to_los_range_compatible(obs: HorosRangeObservation) -> LosRangeCompatible:
    valid=obs.state in (FusionState.VALID,FusionState.DEGRADED) and obs.range_m is not None
    usable=obs.metric_usability!=MetricUsability.UNUSABLE and valid
    return LosRangeCompatible("LOS_RANGE_COMPATIBLE_RANGE_ONLY",obs.range_m if valid else None,obs.sigma_m,obs.confidence,valid,usable,obs.frame_id,obs.timestamp,obs.target_ref,obs.provenance+(("adapter","HOROS_LOS_RANGE_COMPATIBILITY_RANGE_ONLY"),),None,None,obs.reason)
