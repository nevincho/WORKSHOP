from dataclasses import dataclass
from typing import Optional
import math

EXPECTED_SOURCE = "WIDE_IMX708"
EXPECTED_PROVENANCE = "WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC"
EXPECTED_GUIDANCE_TYPE = "ORIENT_OBSERVATION_AXIS"
VALID_SECTORS = {"LEFT", "CENTER", "RIGHT"}


@dataclass(frozen=True)
class M2OrientationGuidance:
    status: str
    guidance_type: str
    cue_id: int
    source: str
    provenance: str
    timestamp_monotonic_s: float
    expires_at_s: float
    image_x_norm: float
    image_y_norm: float
    horizontal_offset_norm: float
    sector: str
    mission_authority_valid: bool


@dataclass(frozen=True)
class M3PassiveOrientationIntent:
    status: str
    intent_type: str
    cue_id: Optional[int]
    source: Optional[str]
    provenance: Optional[str]
    expires_at_s: Optional[float]
    image_x_norm: Optional[float]
    image_y_norm: Optional[float]
    horizontal_offset_norm: Optional[float]
    sector: Optional[str]
    reason: str


def _none(reason: str) -> M3PassiveOrientationIntent:
    return M3PassiveOrientationIntent(
        status="SUPPRESSED",
        intent_type="NO_INTENT",
        cue_id=None,
        source=None,
        provenance=None,
        expires_at_s=None,
        image_x_norm=None,
        image_y_norm=None,
        horizontal_offset_norm=None,
        sector=None,
        reason=reason,
    )


def _sector_from_offset(offset: float, center_half_width_norm: float = 0.20) -> str:
    if offset < -center_half_width_norm:
        return "LEFT"
    if offset > center_half_width_norm:
        return "RIGHT"
    return "CENTER"


def build_m3_orientation_intent(
    guidance: Optional[M2OrientationGuidance],
    now_s: float,
    hq_authoritative_target_active: bool = False,
) -> M3PassiveOrientationIntent:
    """Translate passive M2 orientation guidance into passive M3 intent only.

    This function deliberately contains no carrier adapter, FC interface,
    heading/yaw conversion, actuator values, transport or command-send path.
    """
    if not math.isfinite(now_s):
        return _none("INVALID_TIME")
    if hq_authoritative_target_active:
        return _none("HQ_AUTHORITY_ACTIVE")
    if guidance is None:
        return _none("NO_M2_GUIDANCE")

    try:
        if not guidance.mission_authority_valid:
            return _none("MISSION_AUTHORITY_LOST")
        if guidance.status != "AVAILABLE":
            return _none("GUIDANCE_SUPPRESSED_OR_CANCELLED")
        if guidance.guidance_type != EXPECTED_GUIDANCE_TYPE:
            return _none("UNSUPPORTED_SEMANTIC")
        if guidance.source != EXPECTED_SOURCE or guidance.provenance != EXPECTED_PROVENANCE:
            return _none("INVALID_PROVENANCE")

        values = (
            float(guidance.timestamp_monotonic_s),
            float(guidance.expires_at_s),
            float(guidance.image_x_norm),
            float(guidance.image_y_norm),
            float(guidance.horizontal_offset_norm),
        )
        if not all(math.isfinite(v) for v in values):
            return _none("MALFORMED_DIRECTION")
        if guidance.expires_at_s < guidance.timestamp_monotonic_s:
            return _none("MALFORMED_DIRECTION")
        if not (0.0 <= guidance.image_x_norm <= 1.0 and 0.0 <= guidance.image_y_norm <= 1.0):
            return _none("MALFORMED_DIRECTION")
        if not (-1.0 <= guidance.horizontal_offset_norm <= 1.0):
            return _none("MALFORMED_DIRECTION")

        expected_offset = (guidance.image_x_norm - 0.5) * 2.0
        if abs(guidance.horizontal_offset_norm - expected_offset) > 1e-9:
            return _none("MALFORMED_DIRECTION")
        if guidance.sector not in VALID_SECTORS:
            return _none("MALFORMED_DIRECTION")
        if guidance.sector != _sector_from_offset(guidance.horizontal_offset_norm):
            return _none("MALFORMED_DIRECTION")

        if now_s < guidance.timestamp_monotonic_s or now_s > guidance.expires_at_s:
            return _none("STALE_GUIDANCE")
    except Exception:
        return _none("MALFORMED_DIRECTION")

    return M3PassiveOrientationIntent(
        status="VALID",
        intent_type="ORIENT_OBSERVATION_AXIS",
        cue_id=guidance.cue_id,
        source=guidance.source,
        provenance=guidance.provenance,
        expires_at_s=guidance.expires_at_s,
        image_x_norm=guidance.image_x_norm,
        image_y_norm=guidance.image_y_norm,
        horizontal_offset_norm=guidance.horizontal_offset_norm,
        sector=guidance.sector,
        reason="VALID_PASSIVE_ORIENTATION_INTENT",
    )
