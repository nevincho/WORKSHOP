from dataclasses import dataclass
from typing import Optional
import math

EXPECTED_SOURCE = "WIDE_IMX708"
EXPECTED_PROVENANCE = "WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC"
VALID_SECTORS = {"LEFT", "CENTER", "RIGHT"}
CENTER_HALF_WIDTH_NORM = 0.20
COORD_TOLERANCE = 1e-6


@dataclass(frozen=True)
class MC1AuthorityContext:
    mission_active: bool
    operator_allows_acquisition: bool
    system_ready: bool
    safety_available: bool


@dataclass(frozen=True)
class HQAuthorityState:
    authoritative_target_active: bool


@dataclass(frozen=True)
class AcquisitionInput:
    cue_id: int
    source: str
    timestamp_monotonic_s: float
    expires_at_s: float
    image_x_norm: float
    image_y_norm: float
    horizontal_offset_norm: float
    sector: str
    quality: float
    persistence_frames: int
    provenance: str


@dataclass(frozen=True)
class BridgeResult:
    accepted: bool
    reason: str
    acquisition: Optional[AcquisitionInput] = None


@dataclass(frozen=True)
class M1AcquisitionDecision:
    state: str
    action: str
    cue_id: Optional[int]
    sector: Optional[str]
    horizontal_offset_norm: Optional[float]
    reason: str


def _expected_sector(offset: float) -> str:
    if offset < -CENTER_HALF_WIDTH_NORM:
        return "LEFT"
    if offset > CENTER_HALF_WIDTH_NORM:
        return "RIGHT"
    return "CENTER"


def validate_wide_acquisition_cue(
    cue,
    now_s: float,
    authority: MC1AuthorityContext,
    hq: HQAuthorityState,
    min_quality: float = 0.60,
    min_persistence_frames: int = 2,
) -> BridgeResult:
    """MC1-side validation of frozen WideAcquisitionCue v1 semantics.

    This function grants no target, navigation, guidance or FC authority.
    It only converts a valid non-authoritative WIDE cue into a bounded
    acquisition input for M1.
    """
    if not math.isfinite(now_s):
        return BridgeResult(False, "INVALID_NOW")
    if not (0.0 <= min_quality <= 1.0) or min_persistence_frames < 1:
        return BridgeResult(False, "INVALID_GATE_CONFIG")

    if not (
        authority.mission_active
        and authority.operator_allows_acquisition
        and authority.system_ready
        and authority.safety_available
    ):
        return BridgeResult(False, "MISSION_NOT_PERMITTED")

    if hq.authoritative_target_active:
        return BridgeResult(False, "HQ_AUTHORITY_ACTIVE")

    if cue is None:
        return BridgeResult(False, "NO_CUE")

    try:
        if cue.schema_version != 1:
            return BridgeResult(False, "UNSUPPORTED_SCHEMA")
        if cue.source != EXPECTED_SOURCE or cue.provenance != EXPECTED_PROVENANCE:
            return BridgeResult(False, "INVALID_SOURCE_OR_PROVENANCE")
        values = (
            float(cue.timestamp_monotonic_s),
            float(cue.max_age_s),
            float(cue.image_x_norm),
            float(cue.image_y_norm),
            float(cue.horizontal_offset_norm),
            float(cue.motion_area_norm),
            float(cue.quality),
        )
        if not all(math.isfinite(v) for v in values):
            return BridgeResult(False, "MALFORMED_CUE")
        if cue.max_age_s <= 0.0:
            return BridgeResult(False, "MALFORMED_CUE")
        if not (0.0 <= cue.image_x_norm <= 1.0 and 0.0 <= cue.image_y_norm <= 1.0):
            return BridgeResult(False, "MALFORMED_CUE")
        if not (-1.0 <= cue.horizontal_offset_norm <= 1.0):
            return BridgeResult(False, "MALFORMED_CUE")
        if cue.sector not in VALID_SECTORS:
            return BridgeResult(False, "MALFORMED_CUE")
        if not (0.0 <= cue.motion_area_norm <= 1.0 and 0.0 <= cue.quality <= 1.0):
            return BridgeResult(False, "MALFORMED_CUE")
        if int(cue.persistence_frames) < 1:
            return BridgeResult(False, "MALFORMED_CUE")

        expected_offset = (cue.image_x_norm - 0.5) * 2.0
        if abs(cue.horizontal_offset_norm - expected_offset) > COORD_TOLERANCE:
            return BridgeResult(False, "INCONSISTENT_CUE_GEOMETRY")
        if cue.sector != _expected_sector(cue.horizontal_offset_norm):
            return BridgeResult(False, "INCONSISTENT_CUE_GEOMETRY")
    except Exception:
        return BridgeResult(False, "MALFORMED_CUE")

    age_s = now_s - cue.timestamp_monotonic_s
    if not math.isfinite(age_s) or age_s < 0.0 or age_s > cue.max_age_s:
        return BridgeResult(False, "STALE_CUE")
    if cue.quality < min_quality:
        return BridgeResult(False, "LOW_QUALITY")
    if cue.persistence_frames < min_persistence_frames:
        return BridgeResult(False, "LOW_PERSISTENCE")

    acquisition = AcquisitionInput(
        cue_id=cue.cue_id,
        source=cue.source,
        timestamp_monotonic_s=cue.timestamp_monotonic_s,
        expires_at_s=cue.timestamp_monotonic_s + cue.max_age_s,
        image_x_norm=cue.image_x_norm,
        image_y_norm=cue.image_y_norm,
        horizontal_offset_norm=cue.horizontal_offset_norm,
        sector=cue.sector,
        quality=cue.quality,
        persistence_frames=cue.persistence_frames,
        provenance=cue.provenance,
    )
    return BridgeResult(True, "ACCEPT", acquisition)


class M1AcquisitionStateMachine:
    """Bounded M1 acquisition semantic only; no M2/M3/FC output."""

    def __init__(self):
        self._active: Optional[AcquisitionInput] = None
        self._state = "SEARCH"

    @property
    def state(self) -> str:
        return self._state

    def step(
        self,
        now_s: float,
        acquisition: Optional[AcquisitionInput] = None,
        hq_authoritative_target_active: bool = False,
    ) -> M1AcquisitionDecision:
        if not math.isfinite(now_s):
            self._active = None
            self._state = "SEARCH"
            return M1AcquisitionDecision("SEARCH", "NO_ACTION", None, None, None, "INVALID_TIME")

        if hq_authoritative_target_active:
            self._active = None
            self._state = "AUTHORITATIVE_TRACK"
            return M1AcquisitionDecision(
                "AUTHORITATIVE_TRACK", "NO_WIDE_OVERRIDE", None, None, None, "HQ_AUTHORITY_ACTIVE"
            )

        if self._active is not None and now_s > self._active.expires_at_s:
            self._active = None
            self._state = "SEARCH"
            return M1AcquisitionDecision("SEARCH", "NO_ACTION", None, None, None, "CUE_TIMEOUT")

        if acquisition is not None:
            if now_s > acquisition.expires_at_s or now_s < acquisition.timestamp_monotonic_s:
                self._active = None
                self._state = "SEARCH"
                return M1AcquisitionDecision("SEARCH", "NO_ACTION", None, None, None, "CUE_TIMEOUT")
            self._active = acquisition
            self._state = "ACQUIRE"
            return M1AcquisitionDecision(
                "ACQUIRE",
                "ORIENT_REQUEST_PENDING",
                acquisition.cue_id,
                acquisition.sector,
                acquisition.horizontal_offset_norm,
                "VALID_WIDE_CUE",
            )

        if self._active is not None:
            self._state = "ACQUIRE"
            return M1AcquisitionDecision(
                "ACQUIRE",
                "ORIENT_REQUEST_PENDING",
                self._active.cue_id,
                self._active.sector,
                self._active.horizontal_offset_norm,
                "AWAITING_HQ_OR_TIMEOUT",
            )

        self._state = "SEARCH"
        return M1AcquisitionDecision("SEARCH", "NO_ACTION", None, None, None, "NO_VALID_CUE")
