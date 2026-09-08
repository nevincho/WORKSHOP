from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
import math

class GuidanceState(str, Enum):
    AVAILABLE='AVAILABLE'; DEGRADED='DEGRADED'; SUPPRESSED='SUPPRESSED'
class GuidanceIntent(str, Enum):
    NO_GUIDANCE='NO_GUIDANCE'; HOLD='HOLD'; ABORT_HOLD='ABORT_HOLD'; MAINTAIN_OBSERVATION='MAINTAIN_OBSERVATION'; REACQUIRE_TARGET='REACQUIRE_TARGET'; MOVE_RELATIVE='MOVE_RELATIVE'; SET_ALTITUDE='SET_ALTITUDE'; SET_HEADING='SET_HEADING'
class MetricStatus(str, Enum):
    VERIFIED='VERIFIED'; NOT_VERIFIED='NOT_VERIFIED'; UNUSABLE='UNUSABLE'; CONFLICT='CONFLICT'; INVALID='INVALID'
class Lifecycle(str, Enum):
    OBSERVED='OBSERVED'; ESTIMATED='ESTIMATED'; PREDICTED='PREDICTED'; COASTING='COASTING'; DEGRADED='DEGRADED'; LOST='LOST'
@dataclass(frozen=True)
class NavigationEvidence:
    target_ref: Optional[str]; timestamp: float; frame_ref: Optional[str]; lifecycle: Optional[Lifecycle]; metric_status: MetricStatus; observation_age_s: Optional[float]
    uncertainty_m: Optional[float]=None; target_xyz_m: Optional[Tuple[float,float,float]]=None; carrier_xyz_m: Optional[Tuple[float,float,float]]=None
    carrier_heading_deg: Optional[float]=None; carrier_altitude_m: Optional[float]=None; search_relative_vector_m: Optional[Tuple[float,float,float]]=None; provenance: Tuple[Tuple[str,str],...]=()
@dataclass(frozen=True)
class GuidanceInput:
    mission_decision: object; navigation: Optional[NavigationEvidence]; evaluated_at: float
@dataclass(frozen=True)
class GuidanceContext:
    previous_target_ref: Optional[str]=None; previous_timestamp: Optional[float]=None
@dataclass(frozen=True)
class GuidancePolicy:
    stale_after_s: float=0.5; degrade_uncertainty_m: float=5.0
@dataclass(frozen=True)
class PassiveGuidanceDecision:
    state: GuidanceState; intent: GuidanceIntent; target_ref: Optional[str]; source_timestamp: float; frame_ref: Optional[str]; metric_status: MetricStatus
    relative_vector_m: Optional[Tuple[float,float,float]]; altitude_m: Optional[float]; heading_deg: Optional[float]; reason: str; provenance: Tuple[Tuple[str,str],...]
    production_authority: bool=False; contract_version: str='M2_SHADOW_V1'

class PassiveGuidanceTranslator:
    def __init__(self, policy: GuidancePolicy=GuidancePolicy()): self.policy=policy
    @staticmethod
    def _finite_vec(v,n=3): return v is None or (len(v)==n and all(math.isfinite(float(x)) for x in v))
    @staticmethod
    def _metric(v):
        try: return MetricStatus(getattr(v,'value',v))
        except Exception: return MetricStatus.INVALID
    def evaluate(self, src: GuidanceInput, context: GuidanceContext=GuidanceContext()) -> PassiveGuidanceDecision:
        m=src.mission_decision; ts=getattr(m,'timestamp',float('nan')); target=getattr(m,'target_ref',None); frame=getattr(m,'frame_ref',None); metric=self._metric(getattr(m,'metric_status','INVALID'))
        prov=tuple(getattr(m,'provenance',()))+(('m2','PASSIVE_GUIDANCE_TRANSLATION'),)
        def out(state,intent,reason,rel=None,alt=None,head=None,nav=None):
            return PassiveGuidanceDecision(state,intent,target,ts,frame,metric,rel,alt,head,reason,prov+(() if nav is None else tuple(nav.provenance)))
        if getattr(m,'version',None)!='M1_SHADOW_V1' or getattr(m,'production_authority',True) is not False: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'invalid_or_authoritative_m1_contract')
        if not math.isfinite(float(ts)) or not math.isfinite(float(src.evaluated_at)): return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'malformed_timestamp')
        if context.previous_timestamp is not None and ts<context.previous_timestamp: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'timestamp_regression')
        if context.previous_target_ref is not None and target!=context.previous_target_ref: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'target_identity_discontinuity_requires_reset')
        age=src.evaluated_at-ts
        if age<0 or age>self.policy.stale_after_s: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'stale_or_discontinuous_m1_decision')
        action=getattr(getattr(m,'action',None),'value',getattr(m,'action',None)); state=getattr(getattr(m,'state',None),'value',getattr(m,'state',None)); upstream_degraded=(state=='DEGRADED')
        if action=='NO_ACTION': return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'m1_no_action')
        if action=='HOLD': return out(GuidanceState.AVAILABLE,GuidanceIntent.HOLD,'m1_hold')
        if action=='ABORT' or state=='ABORT': return out(GuidanceState.AVAILABLE,GuidanceIntent.ABORT_HOLD,'m1_abort_passive_hold')
        if action=='MISSION_COMPLETE' or state=='MISSION_COMPLETE': return out(GuidanceState.AVAILABLE,GuidanceIntent.HOLD,'mission_complete_hold')
        if state=='TARGET_LOST' and action!='REACQUIRE': return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'lost_state_without_reacquire_intent')
        nav=src.navigation
        if nav is None:
            if action=='REACQUIRE': return out(GuidanceState.DEGRADED,GuidanceIntent.REACQUIRE_TARGET,'reacquire_without_search_geometry')
            return out(GuidanceState.DEGRADED,GuidanceIntent.NO_GUIDANCE,'navigation_evidence_missing')
        if not math.isfinite(nav.timestamp) or nav.target_ref!=target or nav.frame_ref!=frame: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'navigation_identity_or_frame_mismatch',nav=nav)
        if nav.timestamp>src.evaluated_at or src.evaluated_at-nav.timestamp>self.policy.stale_after_s: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'stale_navigation_evidence',nav=nav)
        if nav.observation_age_s is None or not math.isfinite(nav.observation_age_s) or nav.observation_age_s<0 or nav.observation_age_s>self.policy.stale_after_s: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'stale_or_unknown_observation',nav=nav)
        if not self._finite_vec(nav.target_xyz_m) or not self._finite_vec(nav.carrier_xyz_m) or not self._finite_vec(nav.search_relative_vector_m): return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'malformed_navigation_vector',nav=nav)
        if nav.carrier_heading_deg is not None and not math.isfinite(nav.carrier_heading_deg): return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'malformed_carrier_heading',nav=nav)
        if nav.carrier_altitude_m is not None and not math.isfinite(nav.carrier_altitude_m): return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'malformed_carrier_altitude',nav=nav)
        if nav.uncertainty_m is not None and (not math.isfinite(nav.uncertainty_m) or nav.uncertainty_m<0): return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'malformed_uncertainty',nav=nav)
        nav_metric=self._metric(nav.metric_status)
        if nav_metric!=metric: return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'metric_status_mismatch',nav=nav)
        if nav.lifecycle==Lifecycle.LOST:
            if action=='REACQUIRE': return out(GuidanceState.DEGRADED,GuidanceIntent.REACQUIRE_TARGET,'lost_reacquire_semantic_only',nav=nav)
            return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'lost_navigation_state',nav=nav)
        if nav_metric in (MetricStatus.UNUSABLE,MetricStatus.CONFLICT,MetricStatus.INVALID): return out(GuidanceState.DEGRADED,GuidanceIntent.HOLD,'unusable_metric_evidence',nav=nav)
        uncertain=nav.uncertainty_m is not None and nav.uncertainty_m>self.policy.degrade_uncertainty_m
        if action=='REACQUIRE':
            if nav.search_relative_vector_m is None: return out(GuidanceState.DEGRADED,GuidanceIntent.REACQUIRE_TARGET,'reacquire_without_search_geometry',nav=nav)
            if nav_metric!=MetricStatus.VERIFIED: return out(GuidanceState.DEGRADED,GuidanceIntent.REACQUIRE_TARGET,'reacquire_geometry_not_verified',nav=nav)
            return out(GuidanceState.DEGRADED if (uncertain or upstream_degraded) else GuidanceState.AVAILABLE,GuidanceIntent.REACQUIRE_TARGET,'reacquire_with_explicit_search_geometry',rel=tuple(float(x) for x in nav.search_relative_vector_m),nav=nav)
        if action not in ('OBSERVE_TARGET','MAINTAIN_TRACK'): return out(GuidanceState.SUPPRESSED,GuidanceIntent.NO_GUIDANCE,'unsupported_m1_action',nav=nav)
        if nav_metric==MetricStatus.NOT_VERIFIED: return out(GuidanceState.DEGRADED,GuidanceIntent.MAINTAIN_OBSERVATION,'metric_not_verified_no_navigation_authority',nav=nav)
        if nav.target_xyz_m is None: return out(GuidanceState.DEGRADED,GuidanceIntent.NO_GUIDANCE,'target_geometry_missing',nav=nav)
        if nav.carrier_xyz_m is None: return out(GuidanceState.DEGRADED,GuidanceIntent.MAINTAIN_OBSERVATION,'carrier_pose_missing_target_relative_only',nav=nav)
        if uncertain: return out(GuidanceState.DEGRADED,GuidanceIntent.MAINTAIN_OBSERVATION,'uncertainty_above_shadow_threshold',nav=nav)
        if upstream_degraded: return out(GuidanceState.DEGRADED,GuidanceIntent.MAINTAIN_OBSERVATION,'upstream_mission_degraded_preserved',nav=nav)
        return out(GuidanceState.AVAILABLE,GuidanceIntent.MAINTAIN_OBSERVATION,'verified_geometry_observation_guidance',nav=nav)
