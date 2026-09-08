from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from time import perf_counter_ns
from typing import Optional, Tuple

class Lifecycle(str, Enum):
    OBSERVED='OBSERVED'; ESTIMATED='ESTIMATED'; PREDICTED='PREDICTED'; COASTING='COASTING'; DEGRADED='DEGRADED'; LOST='LOST'
class MetricState(str, Enum): VALID='VALID'; DEGRADED='DEGRADED'; CONFLICT='CONFLICT'; INVALID='INVALID'
class MetricUsability(str, Enum): VERIFIED='VERIFIED'; NOT_VERIFIED='NOT_VERIFIED'; UNUSABLE='UNUSABLE'
class EnvelopeState(str, Enum): RELIABLE='RELIABLE'; DEGRADED='DEGRADED'; UNUSABLE='UNUSABLE'; UNKNOWN='UNKNOWN'
class AdvisoryState(str, Enum): AVAILABLE='AVAILABLE'; DEGRADED='DEGRADED'; SUPPRESSED='SUPPRESSED'
class ObservationAction(str, Enum): HOLD='HOLD'; OBSERVE='OBSERVE'; REPOSITION_REQUEST='REPOSITION_REQUEST'; MAINTAIN_OBSERVATION_GEOMETRY='MAINTAIN_OBSERVATION_GEOMETRY'; TRACK_STATE_UNUSABLE='TRACK_STATE_UNUSABLE'; NO_GUIDANCE_AVAILABLE='NO_GUIDANCE_AVAILABLE'

@dataclass(frozen=True)
class CarrierPoseRef:
    pose_ref:str; timestamp:float; frame_id:str; valid:bool; provenance:Tuple[Tuple[str,str],...]=()
@dataclass(frozen=True)
class EnvelopeEvidence:
    state:EnvelopeState; angle_deg:Optional[float]; scale_qualification:Optional[str]; orientation_qualified:bool; production_verified:bool; provenance:Tuple[Tuple[str,str],...]=()
@dataclass(frozen=True)
class HorosGuidanceInput:
    schema_version:str; target_ref:str; timestamp:float; frame_ref:str; lifecycle:Lifecycle; metric_state:MetricState; metric_usability:MetricUsability
    xyz_m:Optional[Tuple[float,float,float]]=None; vxyz_mps:Optional[Tuple[float,float,float]]=None; covariance:Optional[Tuple[float,...]]=None
    prediction_ref:Optional[str]=None; range_state:Optional[str]=None; confidence:float=0.0; carrier_pose:Optional[CarrierPoseRef]=None; envelope:Optional[EnvelopeEvidence]=None
    provenance:Tuple[Tuple[str,str],...]=()
@dataclass(frozen=True)
class FreshnessConfig:
    stale_after_s:float; status:str='SHADOW_TEST_NOT_PRODUCTION_VERIFIED'
@dataclass(frozen=True)
class PassiveGuidanceAdvisory:
    contract_id:str; contract_version:str; advisory_state:AdvisoryState; action:ObservationAction; target_ref:str; source_timestamp:float; evaluated_at:float
    age_s:float; stale:bool; metric_state:MetricState; metric_usability:MetricUsability; geometry_envelope_state:EnvelopeState; confidence:float
    uncertainty:Optional[Tuple[float,...]]; carrier_pose_available:bool; world_navigation_available:bool; production_authority:bool; reason:str; provenance:Tuple[Tuple[str,str],...]; processing_time_ms:float

class PassiveGuidancePolicy:
    CONTRACT_ID='TANGRA_PASSIVE_GUIDANCE_ADVISORY'; CONTRACT_VERSION='1.0'
    def __init__(self, freshness:FreshnessConfig):
        if not isfinite(freshness.stale_after_s) or freshness.stale_after_s <= 0: raise ValueError('malformed_freshness_config')
        self.freshness=freshness
    @staticmethod
    def _finite_vec(v,n): return v is None or (len(v)==n and all(isfinite(float(x)) for x in v))
    def evaluate(self, src:HorosGuidanceInput, now:float)->PassiveGuidanceAdvisory:
        t0=perf_counter_ns()
        def out(state,action,reason,env=EnvelopeState.UNKNOWN,stale=False,age=0.0):
            pose=src.carrier_pose is not None and src.carrier_pose.valid
            world=pose and state != AdvisoryState.SUPPRESSED
            return PassiveGuidanceAdvisory(self.CONTRACT_ID,self.CONTRACT_VERSION,state,action,src.target_ref,src.timestamp,now,age,stale,src.metric_state,src.metric_usability,env,max(0.0,min(1.0,src.confidence)),src.covariance,pose,world,False,reason,src.provenance+(("policy","PASSIVE_SHADOW_ONLY"),("freshness_status",self.freshness.status)),(perf_counter_ns()-t0)/1e6)
        try:
            if not src.schema_version or not src.target_ref or not src.frame_ref: return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'malformed_identity')
            if not isfinite(src.timestamp) or not isfinite(now) or not isfinite(src.confidence) or not 0<=src.confidence<=1: return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'malformed_numeric_input')
            if not self._finite_vec(src.xyz_m,3) or not self._finite_vec(src.vxyz_mps,3): return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'malformed_state_vector')
            if src.covariance is not None and (not src.covariance or not all(isfinite(float(x)) for x in src.covariance)): return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'malformed_covariance')
            age=now-src.timestamp
            if age < 0: return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'timestamp_discontinuity',age=age)
            env=src.envelope.state if src.envelope else EnvelopeState.UNKNOWN
            if age > self.freshness.stale_after_s: return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'stale_target_state',env,True,age)
            if src.lifecycle==Lifecycle.LOST: return out(AdvisoryState.SUPPRESSED,ObservationAction.TRACK_STATE_UNUSABLE,'target_lost',env,False,age)
            if src.lifecycle==Lifecycle.COASTING: return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'coasting_metric_navigation_suppressed',env,False,age)
            if src.metric_state in (MetricState.CONFLICT,MetricState.INVALID) or src.metric_usability==MetricUsability.UNUSABLE: return out(AdvisoryState.SUPPRESSED,ObservationAction.TRACK_STATE_UNUSABLE,'metric_state_unusable',env,False,age)
            if env==EnvelopeState.UNUSABLE: return out(AdvisoryState.SUPPRESSED,ObservationAction.TRACK_STATE_UNUSABLE,'observation_geometry_unusable',env,False,age)
            if src.xyz_m is None: return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'metric_position_unavailable',env,False,age)
            if src.metric_state==MetricState.DEGRADED or src.lifecycle==Lifecycle.DEGRADED or env in (EnvelopeState.DEGRADED,EnvelopeState.UNKNOWN):
                action=ObservationAction.MAINTAIN_OBSERVATION_GEOMETRY if env==EnvelopeState.DEGRADED else ObservationAction.OBSERVE
                return out(AdvisoryState.DEGRADED,action,'degraded_evidence_preserved',env,False,age)
            if env==EnvelopeState.RELIABLE:
                return out(AdvisoryState.AVAILABLE,ObservationAction.OBSERVE,'reliable_passive_observation_advisory',env,False,age)
            return out(AdvisoryState.DEGRADED,ObservationAction.OBSERVE,'envelope_not_supplied_or_unknown',env,False,age)
        except Exception:
            return out(AdvisoryState.SUPPRESSED,ObservationAction.NO_GUIDANCE_AVAILABLE,'malformed_input_fail_closed')
