from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
import math

class CommandState(str, Enum):
    VALID='VALID'
    DEGRADED='DEGRADED'
    SUPPRESSED='SUPPRESSED'

class CommandType(str, Enum):
    NO_COMMAND='NO_COMMAND'
    HOLD='HOLD'
    MOVE_RELATIVE='MOVE_RELATIVE'
    SET_ALTITUDE='SET_ALTITUDE'
    SET_HEADING='SET_HEADING'
    ARM='ARM'
    DISARM='DISARM'
    TAKEOFF='TAKEOFF'
    LAND='LAND'

class MetricStatus(str, Enum):
    VERIFIED='VERIFIED'; NOT_VERIFIED='NOT_VERIFIED'; UNUSABLE='UNUSABLE'; CONFLICT='CONFLICT'; INVALID='INVALID'

@dataclass(frozen=True)
class CommandContext:
    previous_target_ref: Optional[str]=None
    previous_timestamp: Optional[float]=None
    previous_frame_ref: Optional[str]=None

@dataclass(frozen=True)
class CommandPolicy:
    stale_after_s: float=0.5

@dataclass(frozen=True)
class PassiveHighLevelCommand:
    state: CommandState
    command_type: CommandType
    source_guidance_state: str
    source_guidance_intent: str
    source_guidance_reason: str
    target_ref: Optional[str]
    source_timestamp: float
    frame_ref: Optional[str]
    metric_status: MetricStatus
    relative_vector_m: Optional[Tuple[float,float,float]]
    altitude_m: Optional[float]
    heading_deg: Optional[float]
    abort_semantic: bool
    reason: str
    provenance: Tuple[Tuple[str,str],...]
    production_authority: bool=False
    contract_version: str='M3_SHADOW_V1'

class PassiveHighLevelCommandTranslator:
    """Pure semantic M2->M3 translation. No transport, planning or actuation."""

    def __init__(self, policy: CommandPolicy=CommandPolicy()):
        self.policy=policy

    @staticmethod
    def _metric(v):
        try:
            return MetricStatus(getattr(v,'value',v))
        except Exception:
            return MetricStatus.INVALID

    @staticmethod
    def _finite_vec(v):
        return v is None or (len(v)==3 and all(math.isfinite(float(x)) for x in v))

    def translate(self, guidance, evaluated_at: float, context: CommandContext=CommandContext()) -> PassiveHighLevelCommand:
        state=str(getattr(getattr(guidance,'state',None),'value',getattr(guidance,'state','')))
        intent=str(getattr(getattr(guidance,'intent',None),'value',getattr(guidance,'intent','')))
        target=getattr(guidance,'target_ref',None)
        source_reason=str(getattr(guidance,'reason',''))
        ts=getattr(guidance,'source_timestamp',float('nan'))
        frame=getattr(guidance,'frame_ref',None)
        metric=self._metric(getattr(guidance,'metric_status','INVALID'))
        rel=getattr(guidance,'relative_vector_m',None)
        alt=getattr(guidance,'altitude_m',None)
        head=getattr(guidance,'heading_deg',None)
        prov=tuple(getattr(guidance,'provenance',()))+(('m3','PASSIVE_HIGH_LEVEL_COMMAND_TRANSLATION'),)

        def out(cs, ct, reason, r=None, a=None, h=None, abort=False):
            return PassiveHighLevelCommand(
                cs,ct,state,intent,source_reason,target,ts,frame,metric,r,a,h,abort,reason,prov
            )

        if getattr(guidance,'contract_version',None)!='M2_SHADOW_V1':
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'invalid_m2_contract_version')
        if getattr(guidance,'production_authority',True) is not False:
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'authoritative_m2_input_rejected')
        if not math.isfinite(float(ts)) or not math.isfinite(float(evaluated_at)):
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'malformed_timestamp')
        if context.previous_timestamp is not None and ts<context.previous_timestamp:
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'timestamp_regression')
        if context.previous_target_ref is not None and target!=context.previous_target_ref:
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'target_identity_mismatch')
        if context.previous_frame_ref is not None and frame!=context.previous_frame_ref:
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'frame_discontinuity')
        age=evaluated_at-ts
        if age<0 or age>self.policy.stale_after_s:
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'stale_or_discontinuous_guidance')
        if not self._finite_vec(rel):
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'nonfinite_relative_vector')
        if alt is not None and not math.isfinite(float(alt)):
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'nonfinite_altitude')
        if head is not None and not math.isfinite(float(head)):
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'nonfinite_heading')

        if state=='SUPPRESSED':
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'m2_suppressed')

        if intent=='NO_GUIDANCE':
            return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'m2_no_guidance')

        if intent=='HOLD':
            return out(CommandState.VALID if state=='AVAILABLE' else CommandState.DEGRADED,
                       CommandType.HOLD,'m2_hold')

        if intent=='ABORT_HOLD':
            return out(CommandState.VALID if state=='AVAILABLE' else CommandState.DEGRADED,
                       CommandType.HOLD,'m2_abort_hold_semantic',abort=True)

        if intent in ('MAINTAIN_OBSERVATION','REACQUIRE_TARGET'):
            return out(CommandState.DEGRADED if state=='DEGRADED' else CommandState.SUPPRESSED,
                       CommandType.NO_COMMAND,'semantic_guidance_without_explicit_movement')

        if intent in ('MOVE_RELATIVE','SET_ALTITUDE','SET_HEADING'):
            if state!='AVAILABLE':
                return out(CommandState.DEGRADED,CommandType.NO_COMMAND,'movement_requires_available_guidance')
            if metric!=MetricStatus.VERIFIED:
                return out(CommandState.DEGRADED,CommandType.NO_COMMAND,'movement_requires_verified_metric')
            if not frame or not isinstance(frame,str) or not frame.strip():
                return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'movement_reference_frame_missing')

        if intent=='MOVE_RELATIVE':
            if rel is None:
                return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'move_relative_parameter_missing')
            return out(CommandState.VALID,CommandType.MOVE_RELATIVE,'explicit_verified_move_relative',
                       r=tuple(float(x) for x in rel))

        if intent=='SET_ALTITUDE':
            if alt is None:
                return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'set_altitude_parameter_missing')
            return out(CommandState.VALID,CommandType.SET_ALTITUDE,'explicit_verified_set_altitude',a=float(alt))

        if intent=='SET_HEADING':
            if head is None:
                return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'set_heading_parameter_missing')
            return out(CommandState.VALID,CommandType.SET_HEADING,'explicit_verified_set_heading',h=float(head))

        return out(CommandState.SUPPRESSED,CommandType.NO_COMMAND,'unsupported_or_reserved_guidance_intent')
