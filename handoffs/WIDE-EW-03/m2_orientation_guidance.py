from dataclasses import dataclass
from typing import Optional
import math

EXPECTED_SOURCE = "WIDE_IMX708"
EXPECTED_PROVENANCE = "WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC"
VALID_SECTORS = {"LEFT", "CENTER", "RIGHT"}


@dataclass(frozen=True)
class M1OrientationRequest:
    state: str
    action: str
    cue_id: int
    source: str
    provenance: str
    timestamp_monotonic_s: float
    expires_at_s: float
    image_x_norm: float
    image_y_norm: float
    horizontal_offset_norm: float
    sector: str
    quality: float
    persistence_frames: int
    mission_authority_valid: bool


@dataclass(frozen=True)
class M2PassiveOrientationGuidance:
    status: str
    guidance_type: str
    cue_id: Optional[int]
    source: Optional[str]
    provenance: Optional[str]
    expires_at_s: Optional[float]
    image_x_norm: Optional[float]
    image_y_norm: Optional[float]
    horizontal_offset_norm: Optional[float]
    sector: Optional[str]
    reason: str


def _suppressed(reason: str) -> M2PassiveOrientationGuidance:
    return M2PassiveOrientationGuidance(
        "SUPPRESSED", "NO_GUIDANCE", None, None, None, None,
        None, None, None, None, reason
    )


def _sector_from_offset(offset: float, center_half_width_norm: float = 0.20) -> str:
    if offset < -center_half_width_norm:
        return "LEFT"
    if offset > center_half_width_norm:
        return "RIGHT"
    return "CENTER"


def build_m2_orientation_guidance(
    m1: Optional[M1OrientationRequest],
    now_s: float,
    hq_authoritative_target_active: bool = False,
) -> M2PassiveOrientationGuidance:
    """Passive M1→M2 translation only. Produces no M3 or FC output."""
    if not math.isfinite(now_s):
        return _suppressed("INVALID_TIME")
    if hq_authoritative_target_active:
        return _suppressed("HQ_AUTHORITY_ACTIVE")
    if m1 is None:
        return _suppressed("NO_ACQUISITION")

    try:
        if not m1.mission_authority_valid:
            return _suppressed("MISSION_AUTHORITY_LOST")
        if m1.state != "ACQUIRE" or m1.action != "ORIENT_REQUEST_PENDING":
            return _suppressed("ACQUISITION_NOT_PENDING")
        if m1.source != EXPECTED_SOURCE or m1.provenance != EXPECTED_PROVENANCE:
            return _suppressed("INVALID_PROVENANCE")

        values = (
            float(m1.timestamp_monotonic_s), float(m1.expires_at_s),
            float(m1.image_x_norm), float(m1.image_y_norm),
            float(m1.horizontal_offset_norm), float(m1.quality),
        )
        if not all(math.isfinite(v) for v in values):
            return _suppressed("MALFORMED_DIRECTION")
        if not (0.0 <= m1.image_x_norm <= 1.0 and 0.0 <= m1.image_y_norm <= 1.0):
            return _suppressed("MALFORMED_DIRECTION")
        if not (-1.0 <= m1.horizontal_offset_norm <= 1.0):
            return _suppressed("MALFORMED_DIRECTION")

        expected_offset = (m1.image_x_norm - 0.5) * 2.0
        if abs(m1.horizontal_offset_norm - expected_offset) > 1e-9:
            return _suppressed("MALFORMED_DIRECTION")
        if m1.sector not in VALID_SECTORS:
            return _suppressed("MALFORMED_DIRECTION")
        if m1.sector != _sector_from_offset(m1.horizontal_offset_norm):
            return _suppressed("MALFORMED_DIRECTION")

        if now_s < m1.timestamp_monotonic_s or now_s > m1.expires_at_s:
            return _suppressed("STALE_ACQUISITION")
    except Exception:
        return _suppressed("MALFORMED_DIRECTION")

    return M2PassiveOrientationGuidance(
        status="AVAILABLE",
        guidance_type="ORIENT_OBSERVATION_AXIS",
        cue_id=m1.cue_id,
        source=m1.source,
        provenance=m1.provenance,
        expires_at_s=m1.expires_at_s,
        image_x_norm=m1.image_x_norm,
        image_y_norm=m1.image_y_norm,
        horizontal_offset_norm=m1.horizontal_offset_norm,
        sector=m1.sector,
        reason="VALID_WIDE_ACQUISITION",
    )
