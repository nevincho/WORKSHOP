from dataclasses import dataclass
from typing import Optional, Sequence, Tuple
import math


@dataclass(frozen=True)
class WideAcquisitionCue:
    schema_version: int
    cue_id: int
    source: str
    timestamp_monotonic_s: float
    max_age_s: float
    image_x_norm: float
    image_y_norm: float
    horizontal_offset_norm: float
    sector: str
    motion_area_norm: float
    quality: float
    persistence_frames: int
    provenance: str = "WIDE_MOTION_DIFFERENCE_NON_METRIC"

    def age_s(self, now_s: float) -> float:
        return now_s - self.timestamp_monotonic_s

    def is_fresh(self, now_s: float) -> bool:
        age = self.age_s(now_s)
        return math.isfinite(age) and age >= 0.0 and age <= self.max_age_s

    def validate(self) -> bool:
        if self.schema_version != 1 or self.source != "WIDE_IMX708":
            return False
        if self.provenance != "WIDE_MOTION_DIFFERENCE_NON_METRIC":
            return False
        vals = (
            self.timestamp_monotonic_s,
            self.max_age_s,
            self.image_x_norm,
            self.image_y_norm,
            self.horizontal_offset_norm,
            self.motion_area_norm,
            self.quality,
        )
        if not all(math.isfinite(v) for v in vals):
            return False
        if self.max_age_s <= 0.0 or self.persistence_frames < 1:
            return False
        if not (0.0 <= self.image_x_norm <= 1.0 and 0.0 <= self.image_y_norm <= 1.0):
            return False
        if not (-1.0 <= self.horizontal_offset_norm <= 1.0):
            return False
        if not (0.0 <= self.motion_area_norm <= 1.0 and 0.0 <= self.quality <= 1.0):
            return False
        if self.sector not in {"LEFT", "CENTER", "RIGHT"}:
            return False
        return True


def cue_is_acceptable(cue: Optional[WideAcquisitionCue], now_s: float) -> bool:
    return cue is not None and cue.validate() and cue.is_fresh(now_s)


class WideCueGenerator:
    """Deterministic, non-metric motion cue generator.

    Input is an already-downscaled grayscale frame represented as a 2D
    sequence of integer samples in [0, 255]. State is bounded to the latest
    previous frame plus a persistence counter. No neural inference, tracking,
    metric geometry, target identity or command authority is present.
    """

    def __init__(
        self,
        width: int = 160,
        height: int = 90,
        pixel_diff_threshold: int = 20,
        min_motion_area_norm: float = 0.005,
        min_persistence_frames: int = 2,
        max_age_s: float = 0.5,
        center_half_width_norm: float = 0.20,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("invalid dimensions")
        if not (0 <= pixel_diff_threshold <= 255):
            raise ValueError("invalid pixel threshold")
        if not (0.0 < min_motion_area_norm <= 1.0):
            raise ValueError("invalid motion area threshold")
        if min_persistence_frames < 1:
            raise ValueError("invalid persistence")
        if max_age_s <= 0.0:
            raise ValueError("invalid max_age")
        if not (0.0 < center_half_width_norm < 1.0):
            raise ValueError("invalid center sector width")

        self.width = width
        self.height = height
        self.pixel_diff_threshold = pixel_diff_threshold
        self.min_motion_area_norm = min_motion_area_norm
        self.min_persistence_frames = min_persistence_frames
        self.max_age_s = max_age_s
        self.center_half_width_norm = center_half_width_norm
        self._prev: Optional[Tuple[Tuple[int, ...], ...]] = None
        self._persistence = 0
        self._cue_id = 0

    def _validate_frame(self, frame: Sequence[Sequence[int]]) -> Tuple[Tuple[int, ...], ...]:
        if len(frame) != self.height:
            raise ValueError("unexpected frame height")
        rows = []
        for row in frame:
            if len(row) != self.width:
                raise ValueError("unexpected frame width")
            vals = tuple(int(v) for v in row)
            if any(v < 0 or v > 255 for v in vals):
                raise ValueError("pixel out of range")
            rows.append(vals)
        return tuple(rows)

    def _sector(self, x_norm: float) -> str:
        offset = (x_norm - 0.5) * 2.0
        if offset < -self.center_half_width_norm:
            return "LEFT"
        if offset > self.center_half_width_norm:
            return "RIGHT"
        return "CENTER"

    def process(self, frame, timestamp_monotonic_s: float) -> Optional[WideAcquisitionCue]:
        if not math.isfinite(timestamp_monotonic_s):
            self._persistence = 0
            return None
        try:
            cur = self._validate_frame(frame)
        except Exception:
            self._persistence = 0
            return None

        prev = self._prev
        self._prev = cur
        if prev is None:
            self._persistence = 0
            return None

        changed = 0
        sx = 0
        sy = 0
        diff_sum = 0
        for y in range(self.height):
            prow = prev[y]
            crow = cur[y]
            for x in range(self.width):
                d = abs(crow[x] - prow[x])
                if d >= self.pixel_diff_threshold:
                    changed += 1
                    sx += x
                    sy += y
                    diff_sum += d

        total = self.width * self.height
        area = changed / total
        if changed == 0 or area < self.min_motion_area_norm:
            self._persistence = 0
            return None

        self._persistence += 1
        if self._persistence < self.min_persistence_frames:
            return None

        x_norm = sx / changed / max(1, self.width - 1)
        y_norm = sy / changed / max(1, self.height - 1)
        offset = max(-1.0, min(1.0, (x_norm - 0.5) * 2.0))
        mean_diff = diff_sum / changed / 255.0
        quality = max(
            0.0,
            min(1.0, 0.5 * area / self.min_motion_area_norm + 0.5 * mean_diff),
        )
        self._cue_id += 1
        cue = WideAcquisitionCue(
            schema_version=1,
            cue_id=self._cue_id,
            source="WIDE_IMX708",
            timestamp_monotonic_s=timestamp_monotonic_s,
            max_age_s=self.max_age_s,
            image_x_norm=x_norm,
            image_y_norm=y_norm,
            horizontal_offset_norm=offset,
            sector=self._sector(x_norm),
            motion_area_norm=area,
            quality=quality,
            persistence_frames=self._persistence,
        )
        return cue if cue.validate() else None
