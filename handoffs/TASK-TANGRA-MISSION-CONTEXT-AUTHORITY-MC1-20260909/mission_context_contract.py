from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional, Tuple

class MissionActivation(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"

class OperatorIntent(str, Enum):
    NONE = "NONE"
    OBSERVE = "OBSERVE"
    TRACK = "TRACK"
    HOLD = "HOLD"
    COMPLETE = "COMPLETE"
    ABORT = "ABORT"

class AuthorityOwner(str, Enum):
    MISSION_ACTIVATION = "MISSION_ACTIVATION_AUTHORITY"
    OPERATOR_INTENT = "OPERATOR_INTENT_AUTHORITY"
    SYSTEM_READINESS = "SYSTEM_READINESS_AUTHORITY"
    SAFETY_AVAILABILITY = "SAFETY_AVAILABILITY_AUTHORITY"

@dataclass(frozen=True)
class AuthorityStamp:
    owner: AuthorityOwner
    source_ref: str
    revision: int

@dataclass(frozen=True)
class MissionContext:
    mission_active: Optional[bool] = None
    operator_intent: Optional[OperatorIntent] = None
    system_ready: Optional[bool] = None
    safety_available: Optional[bool] = None
    mission_active_stamp: Optional[AuthorityStamp] = None
    operator_intent_stamp: Optional[AuthorityStamp] = None
    system_ready_stamp: Optional[AuthorityStamp] = None
    safety_available_stamp: Optional[AuthorityStamp] = None

@dataclass(frozen=True)
class M1ContextMapping:
    mission_active: bool
    operator_intent: OperatorIntent
    system_ready: bool
    safety_available: bool
    authoritative: bool
    reasons: Tuple[str, ...]
    production_authority: bool = False
    contract_version: str = "MISSION_CONTEXT_MC1_V1"

class MissionContextStore:
    def __init__(self):
        self._context = MissionContext()

    @property
    def context(self) -> MissionContext:
        return self._context

    @staticmethod
    def _validate_stamp(stamp: AuthorityStamp, expected: AuthorityOwner, previous: Optional[AuthorityStamp]) -> None:
        if not isinstance(stamp, AuthorityStamp):
            raise TypeError("authority_stamp_required")
        if stamp.owner != expected:
            raise ValueError("authority_owner_mismatch")
        if not stamp.source_ref or not isinstance(stamp.source_ref, str):
            raise ValueError("authority_source_ref_required")
        if not isinstance(stamp.revision, int) or isinstance(stamp.revision, bool) or stamp.revision < 0:
            raise ValueError("authority_revision_invalid")
        if previous is not None:
            if stamp.source_ref != previous.source_ref:
                raise ValueError("authority_source_change_requires_reset")
            if stamp.revision <= previous.revision:
                raise ValueError("authority_revision_not_monotonic")

    def set_mission_active(self, value: bool, stamp: AuthorityStamp) -> MissionContext:
        if type(value) is not bool:
            raise TypeError("mission_active_bool_required")
        self._validate_stamp(stamp, AuthorityOwner.MISSION_ACTIVATION, self._context.mission_active_stamp)
        self._context = replace(self._context, mission_active=value, mission_active_stamp=stamp)
        return self._context

    def set_operator_intent(self, value: OperatorIntent, stamp: AuthorityStamp) -> MissionContext:
        if not isinstance(value, OperatorIntent):
            raise TypeError("operator_intent_enum_required")
        self._validate_stamp(stamp, AuthorityOwner.OPERATOR_INTENT, self._context.operator_intent_stamp)
        self._context = replace(self._context, operator_intent=value, operator_intent_stamp=stamp)
        return self._context

    def set_system_ready(self, value: bool, stamp: AuthorityStamp) -> MissionContext:
        if type(value) is not bool:
            raise TypeError("system_ready_bool_required")
        self._validate_stamp(stamp, AuthorityOwner.SYSTEM_READINESS, self._context.system_ready_stamp)
        self._context = replace(self._context, system_ready=value, system_ready_stamp=stamp)
        return self._context

    def set_safety_available(self, value: bool, stamp: AuthorityStamp) -> MissionContext:
        if type(value) is not bool:
            raise TypeError("safety_available_bool_required")
        self._validate_stamp(stamp, AuthorityOwner.SAFETY_AVAILABILITY, self._context.safety_available_stamp)
        self._context = replace(self._context, safety_available=value, safety_available_stamp=stamp)
        return self._context

    def reset_authorities(self) -> MissionContext:
        self._context = MissionContext()
        return self._context

def map_to_m1_context(context: MissionContext) -> M1ContextMapping:
    reasons = []
    if context.mission_active is None or context.mission_active_stamp is None:
        reasons.append("mission_active_unavailable")
    if context.operator_intent is None or context.operator_intent_stamp is None:
        reasons.append("operator_intent_unavailable")
    if context.system_ready is None or context.system_ready_stamp is None:
        reasons.append("system_ready_unavailable")
    if context.safety_available is None or context.safety_available_stamp is None:
        reasons.append("safety_available_unavailable")
    if reasons:
        conservative_intent = (
            context.operator_intent
            if context.operator_intent in (OperatorIntent.ABORT, OperatorIntent.HOLD)
            and context.operator_intent_stamp is not None
            else OperatorIntent.NONE
        )
        return M1ContextMapping(
            mission_active=False,
            operator_intent=conservative_intent,
            system_ready=False,
            safety_available=False,
            authoritative=False,
            reasons=tuple(reasons),
        )
    return M1ContextMapping(
        mission_active=context.mission_active,
        operator_intent=context.operator_intent,
        system_ready=context.system_ready,
        safety_available=context.safety_available,
        authoritative=True,
        reasons=(),
    )
