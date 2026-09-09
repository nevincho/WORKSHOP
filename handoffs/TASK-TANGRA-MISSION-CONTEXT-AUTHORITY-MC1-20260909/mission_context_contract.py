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
        error = _validate_authority_stamp(stamp, expected)
        if error is not None:
            if error == "authority_stamp_required":
                raise TypeError(error)
            raise ValueError(error)
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

def _validate_authority_stamp(stamp: object, expected: AuthorityOwner) -> Optional[str]:
    if type(stamp) is not AuthorityStamp:
        return "authority_stamp_required"
    if type(stamp.owner) is not AuthorityOwner:
        return "authority_owner_type_invalid"
    if stamp.owner is not expected:
        return "authority_owner_mismatch"
    if type(stamp.source_ref) is not str or not stamp.source_ref.strip():
        return "authority_source_ref_required"
    if type(stamp.revision) is not int or stamp.revision < 0:
        return "authority_revision_invalid"
    return None

def _field_valid(value: object, stamp: object, expected: AuthorityOwner, value_kind: str) -> Tuple[bool, Optional[str]]:
    if value_kind == "bool":
        if type(value) is not bool:
            return False, "value_bool_required"
    elif value_kind == "intent":
        if type(value) is not OperatorIntent:
            return False, "value_operator_intent_required"
    else:
        return False, "internal_value_kind_invalid"
    stamp_error = _validate_authority_stamp(stamp, expected)
    if stamp_error is not None:
        return False, stamp_error
    return True, None

def map_to_m1_context(context: MissionContext) -> M1ContextMapping:
    if type(context) is not MissionContext:
        return M1ContextMapping(False, OperatorIntent.NONE, False, False, False, ("mission_context_required",))

    checks = (
        ("mission_active", context.mission_active, context.mission_active_stamp, AuthorityOwner.MISSION_ACTIVATION, "bool"),
        ("operator_intent", context.operator_intent, context.operator_intent_stamp, AuthorityOwner.OPERATOR_INTENT, "intent"),
        ("system_ready", context.system_ready, context.system_ready_stamp, AuthorityOwner.SYSTEM_READINESS, "bool"),
        ("safety_available", context.safety_available, context.safety_available_stamp, AuthorityOwner.SAFETY_AVAILABILITY, "bool"),
    )

    reasons = []
    field_validity = {}
    for field_name, value, stamp, expected_owner, value_kind in checks:
        valid, error = _field_valid(value, stamp, expected_owner, value_kind)
        field_validity[field_name] = valid
        if not valid:
            reasons.append(f"{field_name}_{error}")

    if reasons:
        operator_valid = field_validity["operator_intent"]
        conservative_intent = (
            context.operator_intent
            if operator_valid and context.operator_intent in (OperatorIntent.ABORT, OperatorIntent.HOLD)
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
