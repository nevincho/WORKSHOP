from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
import math

class MissionState(str, Enum):
    IDLE='IDLE'; OBSERVE='OBSERVE'; TRACK='TRACK'; DEGRADED='DEGRADED'; TARGET_LOST='TARGET_LOST'; HOLD='HOLD'; MISSION_COMPLETE='MISSION_COMPLETE'; ABORT='ABORT'
class MissionAction(str, Enum):
    NO_ACTION='NO_ACTION'; OBSERVE_TARGET='OBSERVE_TARGET'; MAINTAIN_TRACK='MAINTAIN_TRACK'; HOLD='HOLD'; REACQUIRE='REACQUIRE'; MISSION_COMPLETE='MISSION_COMPLETE'; ABORT='ABORT'
class Lifecycle(str, Enum):
    OBSERVED='OBSERVED'; ESTIMATED='ESTIMATED'; PREDICTED='PREDICTED'; COASTING='COASTING'; DEGRADED='DEGRADED'; LOST='LOST'
class MetricStatus(str, Enum):
    VERIFIED='VERIFIED'; NOT_VERIFIED='NOT_VERIFIED'; UNUSABLE='UNUSABLE'; CONFLICT='CONFLICT'; INVALID='INVALID'
class OperatorIntent(str, Enum):
    NONE='NONE'; OBSERVE='OBSERVE'; TRACK='TRACK'; HOLD='HOLD'; COMPLETE='COMPLETE'; ABORT='ABORT'

@dataclass(frozen=True)
class CarrierPose:
    xyz: Tuple[float,float,float]; timestamp: float; frame: str; valid: bool=True
@dataclass(frozen=True)
class MissionInput:
    mission_active: bool; operator_intent: OperatorIntent; target_ref: Optional[str]; timestamp: float; frame_ref: Optional[str]
    lifecycle: Optional[Lifecycle]=None; xyz: Optional[Tuple[float,float,float]]=None; vxyz: Optional[Tuple[float,float,float]]=None
    covariance: Optional[Tuple[float,...]]=None; prediction: Optional[Tuple[float,float,float]]=None; metric_status: MetricStatus=MetricStatus.NOT_VERIFIED
    target_class: Optional[str]=None; observation_age_s: Optional[float]=None; provenance: Tuple[Tuple[str,str],...]=(); carrier_pose: Optional[CarrierPose]=None
    system_ready: Optional[bool]=None; safety_available: Optional[bool]=None
@dataclass(frozen=True)
class MissionDecision:
    state: MissionState; action: MissionAction; target_ref: Optional[str]; timestamp: float; frame_ref: Optional[str]; metric_status: MetricStatus
    confidence_authority: str; world_guidance_context_available: bool; reason: str; provenance: Tuple[Tuple[str,str],...]
    version: str='M1_SHADOW_V1'; production_authority: bool=False
@dataclass(frozen=True)
class MissionPolicy:
    stale_after_s: float=0.5; transient_degrade_frames: int=2

class MissionManager:
    def __init__(self, policy=MissionPolicy()):
        self.policy=policy; self._target=None; self._last_timestamp=None; self._degrade_count=0; self._last_stable=MissionState.IDLE
    @staticmethod
    def _finite_tuple(v): return v is None or (len(v)>0 and all(math.isfinite(float(x)) for x in v))
    def decide(self,i):
        def out(state,action,reason,world=False):
            return MissionDecision(state,action,i.target_ref,i.timestamp,i.frame_ref,i.metric_status,'SHADOW_NON_AUTHORITATIVE',world,reason,i.provenance)
        if not math.isfinite(i.timestamp) or i.timestamp<0: return out(MissionState.HOLD,MissionAction.NO_ACTION,'malformed_timestamp')
        if not self._finite_tuple(i.xyz) or not self._finite_tuple(i.vxyz) or not self._finite_tuple(i.prediction): return out(MissionState.HOLD,MissionAction.NO_ACTION,'malformed_spatial_state')
        if i.covariance is not None and (not self._finite_tuple(i.covariance) or any(x<0 for x in i.covariance)): return out(MissionState.HOLD,MissionAction.NO_ACTION,'malformed_covariance')
        if self._last_timestamp is not None and i.timestamp<self._last_timestamp: return out(MissionState.HOLD,MissionAction.NO_ACTION,'timestamp_regression')
        self._last_timestamp=i.timestamp
        if i.operator_intent==OperatorIntent.ABORT: self._last_stable=MissionState.ABORT; return out(MissionState.ABORT,MissionAction.ABORT,'operator_abort')
        if i.operator_intent==OperatorIntent.COMPLETE: self._last_stable=MissionState.MISSION_COMPLETE; return out(MissionState.MISSION_COMPLETE,MissionAction.MISSION_COMPLETE,'operator_complete')
        if i.operator_intent==OperatorIntent.HOLD: self._last_stable=MissionState.HOLD; return out(MissionState.HOLD,MissionAction.HOLD,'operator_hold')
        if not i.mission_active: self._target=None; self._degrade_count=0; self._last_stable=MissionState.IDLE; return out(MissionState.IDLE,MissionAction.NO_ACTION,'no_active_mission')
        if i.system_ready is not True or i.safety_available is not True: return out(MissionState.HOLD,MissionAction.HOLD,'readiness_or_safety_unavailable')
        if i.observation_age_s is None or not math.isfinite(i.observation_age_s) or i.observation_age_s<0 or i.observation_age_s>self.policy.stale_after_s: return out(MissionState.HOLD,MissionAction.NO_ACTION,'stale_or_unknown_observation')
        if not i.target_ref: return out(MissionState.TARGET_LOST,MissionAction.REACQUIRE,'target_unavailable')
        if self._target is not None and i.target_ref!=self._target: self._target=i.target_ref; self._degrade_count=0; self._last_stable=MissionState.OBSERVE; return out(MissionState.OBSERVE,MissionAction.OBSERVE_TARGET,'target_identity_changed')
        self._target=i.target_ref
        if i.lifecycle==Lifecycle.LOST: self._degrade_count=0; self._last_stable=MissionState.TARGET_LOST; return out(MissionState.TARGET_LOST,MissionAction.REACQUIRE,'authoritative_target_lost')
        degraded=i.lifecycle in (Lifecycle.DEGRADED,Lifecycle.COASTING) or i.metric_status in (MetricStatus.UNUSABLE,MetricStatus.CONFLICT,MetricStatus.INVALID)
        if degraded:
            self._degrade_count+=1
            if self._degrade_count<=self.policy.transient_degrade_frames and self._last_stable in (MissionState.OBSERVE,MissionState.TRACK): return out(MissionState.DEGRADED,MissionAction.OBSERVE_TARGET,'bounded_transient_degradation')
            self._last_stable=MissionState.DEGRADED; return out(MissionState.DEGRADED,MissionAction.REACQUIRE,'persistent_degradation')
        self._degrade_count=0
        if i.xyz is None: self._last_stable=MissionState.OBSERVE; return out(MissionState.OBSERVE,MissionAction.OBSERVE_TARGET,'target_observed_without_metric_xyz')
        world=i.carrier_pose is not None and i.carrier_pose.valid and self._finite_tuple(i.carrier_pose.xyz)
        if i.lifecycle==Lifecycle.OBSERVED or i.operator_intent==OperatorIntent.OBSERVE: self._last_stable=MissionState.OBSERVE; return out(MissionState.OBSERVE,MissionAction.OBSERVE_TARGET,'valid_observation',world)
        self._last_stable=MissionState.TRACK; return out(MissionState.TRACK,MissionAction.MAINTAIN_TRACK,'valid_authoritative_track',world)
