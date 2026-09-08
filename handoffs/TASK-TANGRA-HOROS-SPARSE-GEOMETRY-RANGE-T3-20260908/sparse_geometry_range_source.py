from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import hypot, isfinite, sqrt
from statistics import median
from time import perf_counter_ns
from typing import Optional, Tuple

import numpy as np

Point2 = Tuple[float, float]


class RangeValidity(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    INVALID = "INVALID"


@dataclass(frozen=True)
class CameraCalibration:
    calibration_id: str
    resolution_wh: Tuple[int, int]
    fx: float
    fy: float
    cx: float
    cy: float
    distortion: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0)
    relative_scale_sigma: float = 0.0
    coordinates_undistorted: bool = False
    production_verified: bool = False
    provenance: Tuple[Tuple[str, str], ...] = ()

    def validate(self) -> None:
        vals = (self.fx, self.fy, self.cx, self.cy, self.relative_scale_sigma)
        if not all(isfinite(float(v)) for v in vals):
            raise ValueError("malformed_calibration_non_finite")
        if self.fx <= 0 or self.fy <= 0:
            raise ValueError("malformed_calibration_focal")
        w, h = self.resolution_wh
        if w <= 0 or h <= 0:
            raise ValueError("malformed_calibration_resolution")
        if self.relative_scale_sigma < 0:
            raise ValueError("malformed_calibration_uncertainty")
        if any(not isfinite(float(v)) for v in self.distortion):
            raise ValueError("malformed_calibration_distortion")
        if any(abs(float(v)) > 1e-15 for v in self.distortion) and not self.coordinates_undistorted:
            raise ValueError("distortion_not_supported_by_span_model")


@dataclass(frozen=True)
class CalibratedPoint:
    point_type: str
    x: Optional[float]
    y: Optional[float]
    confidence: float
    valid: bool
    reason: str = ""


@dataclass(frozen=True)
class CalibratedGeometryInput:
    source_geometry_ref: str
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_id: Optional[str]
    target_class: str
    destination_resolution_wh: Tuple[int, int]
    transform_id: str
    transform_version: str
    transform_valid: bool
    transform_production_verified: bool
    transform_relative_scale_sigma: float
    points: Tuple[CalibratedPoint, ...]
    provenance: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class PhysicalSpanSpec:
    span_id: str
    point_a: str
    point_b: str
    length_m: float
    sigma_m: float
    correspondence_verified: bool
    independence_group: str
    provenance: str
    orientation_projection_factor: float = 1.0
    orientation_factor_sigma: float = 0.0
    orientation_valid: bool = True
    min_orientation_confidence: float = 0.0

    def validate(self) -> None:
        vals = (self.length_m, self.sigma_m, self.orientation_projection_factor,
                self.orientation_factor_sigma, self.min_orientation_confidence)
        if not all(isfinite(float(v)) for v in vals):
            raise ValueError("malformed_span_non_finite")
        if self.length_m <= 0 or self.sigma_m < 0:
            raise ValueError("malformed_physical_span")
        if not (0.0 < self.orientation_projection_factor <= 1.0):
            raise ValueError("malformed_orientation_projection_factor")
        if self.orientation_factor_sigma < 0:
            raise ValueError("malformed_orientation_uncertainty")
        if not (0.0 <= self.min_orientation_confidence <= 1.0):
            raise ValueError("malformed_orientation_confidence")
        if not self.point_a or not self.point_b or self.point_a == self.point_b:
            raise ValueError("malformed_span_points")
        if not self.independence_group:
            raise ValueError("malformed_independence_group")


@dataclass(frozen=True)
class TargetGeometryProfile:
    profile_id: str
    version: str
    target_class: str
    spans: Tuple[PhysicalSpanSpec, ...]
    provenance: Tuple[Tuple[str, str], ...]
    production_verified: bool = False

    def validate(self) -> None:
        if not self.profile_id or not self.version or not self.target_class:
            raise ValueError("malformed_target_profile")
        ids = set()
        for span in self.spans:
            span.validate()
            if span.span_id in ids:
                raise ValueError("duplicate_span_id")
            ids.add(span.span_id)


@dataclass(frozen=True)
class RangeConfig:
    point_sigma_px: float = 0.75
    min_normalized_image_span: float = 1e-7
    min_candidate_confidence: float = 0.10
    min_independent_candidates: int = 2
    max_relative_consistency_residual: float = 0.18
    max_relative_pair_disagreement: float = 0.30
    uncertainty_floor_relative: float = 0.01

    def validate(self) -> None:
        if self.point_sigma_px <= 0 or self.min_normalized_image_span <= 0:
            raise ValueError("malformed_range_config")
        if self.min_independent_candidates < 1:
            raise ValueError("malformed_range_config")
        if not (0 < self.max_relative_consistency_residual < 1):
            raise ValueError("malformed_range_config")
        if not (0 < self.max_relative_pair_disagreement < 2):
            raise ValueError("malformed_range_config")
        if self.uncertainty_floor_relative < 0:
            raise ValueError("malformed_range_config")


@dataclass(frozen=True)
class RangeCandidate:
    span_id: str
    independence_group: str
    point_a: str
    point_b: str
    calibrated_length_normalized: Optional[float]
    physical_span_m: Optional[float]
    physical_sigma_m: Optional[float]
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: float
    valid: bool
    accepted: bool
    rejection_reason: str
    provenance: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class GeometryRangeObservation:
    source_geometry_ref: str
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_id: Optional[str]
    target_class: str
    profile_id: str
    profile_version: str
    calibration_id: str
    transform_id: str
    transform_version: str
    candidates: Tuple[RangeCandidate, ...]
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: float
    validity: RangeValidity
    production_metric_verified: bool
    provenance: Tuple[Tuple[str, str], ...]
    processing_time_ms: float
    error: str = ""


@dataclass(frozen=True)
class ExistingRangeObservation:
    source: str
    range_m: Optional[float]
    sigma_m: Optional[float]
    confidence: float
    valid: bool
    provenance: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ShadowRangeComparison:
    comparable: bool
    existing: ExistingRangeObservation
    sparse: GeometryRangeObservation
    absolute_delta_m: Optional[float]
    relative_delta: Optional[float]
    reason: str = ""


class SparseGeometryRangeSource:
    """Passive SHADOW range source. No authoritative HOROS/range-estimator integration."""

    def __init__(self, calibration: CameraCalibration, profile: TargetGeometryProfile,
                 config: RangeConfig | None = None) -> None:
        self.calibration = calibration
        self.profile = profile
        self.config = config or RangeConfig()

    def estimate(self, geometry: CalibratedGeometryInput) -> GeometryRangeObservation:
        t0 = perf_counter_ns()
        try:
            self.calibration.validate()
            self.profile.validate()
            self.config.validate()
            self._validate_geometry(geometry)
            if geometry.target_class != self.profile.target_class:
                return self._invalid(geometry, t0, (), "target_class_profile_mismatch")
            points = {p.point_type: p for p in geometry.points}
            candidates = [self._candidate(span, points, geometry) for span in self.profile.spans]
            candidates = self._robust_acceptance(candidates)
            accepted = [c for c in candidates if c.valid and c.accepted]
            groups = {c.independence_group for c in accepted}
            if len(groups) < self.config.min_independent_candidates:
                return self._invalid(geometry, t0, tuple(candidates), "insufficient_independent_evidence")

            representatives = []
            for group in sorted(groups):
                cg = [c for c in accepted if c.independence_group == group]
                representatives.append(min(cg, key=lambda c: float(c.sigma_m) / max(c.confidence, 1e-9)))

            if len(representatives) == 2:
                a, b = representatives
                rel = abs(float(a.range_m) - float(b.range_m)) / max((float(a.range_m) + float(b.range_m)) * 0.5, 1e-9)
                if rel > self.config.max_relative_pair_disagreement:
                    return self._invalid(geometry, t0, tuple(candidates), "candidate_disagreement")

            weights = np.array([c.confidence / max(float(c.sigma_m) ** 2, 1e-12) for c in representatives], dtype=np.float64)
            ranges = np.array([float(c.range_m) for c in representatives], dtype=np.float64)
            if not np.all(np.isfinite(weights)) or float(weights.sum()) <= 0:
                return self._invalid(geometry, t0, tuple(candidates), "invalid_fusion_weights")
            z = float(np.sum(weights * ranges) / np.sum(weights))
            formal_sigma = sqrt(1.0 / float(np.sum(weights)))
            disagreement_sigma = sqrt(float(np.sum(weights * (ranges - z) ** 2) / np.sum(weights))) if len(ranges) > 1 else 0.0
            sigma = max(formal_sigma, disagreement_sigma, abs(z) * self.config.uncertainty_floor_relative)
            confidence = float(np.clip(sum(c.confidence for c in representatives) / len(representatives), 0.0, 1.0))
            production_verified = bool(
                geometry.transform_production_verified and geometry.transform_valid
                and self.profile.production_verified and self.calibration.production_verified
            )
            validity = RangeValidity.VALID if production_verified else RangeValidity.DEGRADED
            provenance = geometry.provenance + self.profile.provenance + (
                ("range_source", "SPARSE_GEOMETRY_SHADOW"),
                ("metric_status", "VERIFIED" if production_verified else "NOT_VERIFIED"),
            )
            return GeometryRangeObservation(
                geometry.source_geometry_ref, geometry.frame_id, geometry.timestamp, geometry.target_id,
                geometry.target_class, self.profile.profile_id, self.profile.version,
                self.calibration.calibration_id, geometry.transform_id, geometry.transform_version,
                tuple(candidates), z, sigma, confidence, validity, production_verified, provenance,
                (perf_counter_ns() - t0) / 1e6,
            )
        except Exception as exc:
            return self._invalid(geometry, t0, (), str(exc))

    def _validate_geometry(self, g: CalibratedGeometryInput) -> None:
        if not g.transform_valid:
            raise ValueError("transform_invalid")
        if g.destination_resolution_wh != self.calibration.resolution_wh:
            raise ValueError("calibration_plane_mismatch")
        if not isfinite(float(g.transform_relative_scale_sigma)) or g.transform_relative_scale_sigma < 0:
            raise ValueError("malformed_transform_uncertainty")

    def _candidate(self, span: PhysicalSpanSpec, points: dict[str, CalibratedPoint],
                   geometry: CalibratedGeometryInput) -> RangeCandidate:
        base_prov = (("profile_span", span.provenance), ("span_id", span.span_id))
        if not span.correspondence_verified:
            return self._reject(span, "physical_correspondence_not_verified", base_prov)
        if not span.orientation_valid:
            return self._reject(span, "orientation_not_valid", base_prov)
        a, b = points.get(span.point_a), points.get(span.point_b)
        if a is None or b is None:
            return self._reject(span, "missing_point", base_prov)
        if (not a.valid) or (not b.valid) or a.x is None or a.y is None or b.x is None or b.y is None:
            return self._reject(span, "invalid_or_null_point", base_prov)
        vals = (a.x, a.y, b.x, b.y, a.confidence, b.confidence)
        if not all(isfinite(float(v)) for v in vals):
            return self._reject(span, "non_finite_point", base_prov)

        du = float(b.x - a.x)
        dv = float(b.y - a.y)
        q = hypot(du / self.calibration.fx, dv / self.calibration.fy)
        if (not isfinite(q)) or q < self.config.min_normalized_image_span:
            return self._reject(span, "near_zero_image_span", base_prov, q=q)

        orientation_conf = max(0.0, 1.0 - min(span.orientation_factor_sigma / max(span.orientation_projection_factor, 1e-12), 1.0))
        if orientation_conf < span.min_orientation_confidence:
            return self._reject(span, "orientation_confidence_too_low", base_prov, q=q)
        z = span.length_m * span.orientation_projection_factor / q
        if not isfinite(z) or z <= 0:
            return self._reject(span, "impossible_range", base_prov, q=q)

        sigma_du = sqrt(2.0) * self.config.point_sigma_px
        sigma_dv = sqrt(2.0) * self.config.point_sigma_px
        dq_du = (du / (self.calibration.fx ** 2)) / q
        dq_dv = (dv / (self.calibration.fy ** 2)) / q
        sigma_q = sqrt((dq_du * sigma_du) ** 2 + (dq_dv * sigma_dv) ** 2)
        rel_sigma = sqrt(
            (span.sigma_m / span.length_m) ** 2 + (sigma_q / q) ** 2
            + (span.orientation_factor_sigma / span.orientation_projection_factor) ** 2
            + self.calibration.relative_scale_sigma ** 2
            + geometry.transform_relative_scale_sigma ** 2
        )
        sigma_z = max(abs(z) * rel_sigma, abs(z) * self.config.uncertainty_floor_relative)
        confidence = float(np.clip(min(a.confidence, b.confidence) * orientation_conf, 0.0, 1.0))
        if confidence < self.config.min_candidate_confidence:
            return self._reject(span, "candidate_confidence_too_low", base_prov, q=q)
        return RangeCandidate(
            span.span_id, span.independence_group, span.point_a, span.point_b, q,
            span.length_m, span.sigma_m, z, sigma_z, confidence, True, False, "",
            base_prov + (("orientation_projection_factor", f"{span.orientation_projection_factor:.9g}"),),
        )

    def _robust_acceptance(self, candidates: list[RangeCandidate]) -> list[RangeCandidate]:
        valid = [c for c in candidates if c.valid and c.range_m is not None]
        groups: dict[str, list[RangeCandidate]] = {}
        for c in valid:
            groups.setdefault(c.independence_group, []).append(c)
        if len(groups) < 3:
            return [self._set_accepted(c, c.valid) for c in candidates]
        reps = [min(cg, key=lambda c: float(c.sigma_m) / max(c.confidence, 1e-9)) for cg in groups.values()]
        center = median([float(c.range_m) for c in reps])
        out = []
        for c in candidates:
            if not c.valid:
                out.append(c)
                continue
            residual = abs(float(c.range_m) - center) / max(abs(center), 1e-9)
            if residual > self.config.max_relative_consistency_residual:
                out.append(RangeCandidate(**{**c.__dict__, "accepted": False, "rejection_reason": "consistency_outlier"}))
            else:
                out.append(self._set_accepted(c, True))
        return out

    @staticmethod
    def _set_accepted(c: RangeCandidate, accepted: bool) -> RangeCandidate:
        return RangeCandidate(**{**c.__dict__, "accepted": accepted})

    def _reject(self, span: PhysicalSpanSpec, reason: str,
                provenance: Tuple[Tuple[str, str], ...], q: Optional[float] = None) -> RangeCandidate:
        return RangeCandidate(span.span_id, span.independence_group, span.point_a, span.point_b,
                              q, span.length_m, span.sigma_m, None, None, 0.0, False, False, reason, provenance)

    def _invalid(self, g: CalibratedGeometryInput, t0: int,
                 candidates: Tuple[RangeCandidate, ...], error: str) -> GeometryRangeObservation:
        return GeometryRangeObservation(
            g.source_geometry_ref, g.frame_id, g.timestamp, g.target_id, g.target_class,
            self.profile.profile_id, self.profile.version, self.calibration.calibration_id,
            g.transform_id, g.transform_version, candidates, None, None, 0.0,
            RangeValidity.INVALID, False,
            g.provenance + (("range_source", "SPARSE_GEOMETRY_SHADOW"),),
            (perf_counter_ns() - t0) / 1e6, error,
        )


def compare_with_existing(existing: ExistingRangeObservation,
                          sparse: GeometryRangeObservation) -> ShadowRangeComparison:
    if (not existing.valid) or existing.range_m is None or (not isfinite(float(existing.range_m))) or existing.range_m <= 0:
        return ShadowRangeComparison(False, existing, sparse, None, None, "existing_range_invalid")
    if sparse.validity == RangeValidity.INVALID or sparse.range_m is None:
        return ShadowRangeComparison(False, existing, sparse, None, None, "sparse_range_invalid")
    delta = abs(float(existing.range_m) - float(sparse.range_m))
    rel = delta / max((float(existing.range_m) + float(sparse.range_m)) * 0.5, 1e-9)
    return ShadowRangeComparison(True, existing, sparse, delta, rel)
