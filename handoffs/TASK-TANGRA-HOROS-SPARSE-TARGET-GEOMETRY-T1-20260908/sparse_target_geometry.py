from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import perf_counter_ns
from typing import Optional, Tuple

import cv2
import numpy as np


class PointType(str, Enum):
    CENTER = "CENTER"
    LEFT_SILHOUETTE = "LEFT_SILHOUETTE"
    RIGHT_SILHOUETTE = "RIGHT_SILHOUETTE"
    NOSE = "NOSE"
    TAIL = "TAIL"


class GeometryValidity(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    INVALID = "INVALID"


@dataclass(frozen=True)
class SparsePoint:
    point_type: PointType
    x: Optional[float]
    y: Optional[float]
    confidence: float
    valid: bool
    reason: str = ""


@dataclass(frozen=True)
class TargetGeometryInput:
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_id: Optional[str]
    target_class: str
    detection_confidence: float
    bbox_xyxy: Tuple[int, int, int, int]
    source: str = "HQ_PRIMARY_DETECTION_ROI"


@dataclass(frozen=True)
class SparseGeometryObservation:
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_id: Optional[str]
    target_class: str
    bbox_xyxy: Tuple[int, int, int, int]
    center: Optional[Tuple[float, float]]
    points: Tuple[SparsePoint, ...]
    geometry_confidence: float
    source: str
    processing_time_ms: float
    validity: GeometryValidity
    roi_shape_hw: Tuple[int, int]
    notes: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ExtractorConfig:
    min_component_area_px: int = 24
    min_component_area_fraction: float = 0.015
    max_component_area_fraction: float = 0.92
    min_axis_anisotropy: float = 1.08
    nose_tail_width_ratio_threshold: float = 1.22
    endpoint_band_fraction: float = 0.18
    border_penalty: float = 0.35


class SparseTargetGeometryExtractor:
    """Deterministic, single-frame, ROI-only SHADOW geometry extractor."""

    def __init__(self, config: ExtractorConfig | None = None) -> None:
        self.config = config or ExtractorConfig()

    def extract(self, frame: np.ndarray, target: TargetGeometryInput) -> SparseGeometryObservation:
        t0 = perf_counter_ns()
        notes: list[str] = []
        if frame is None or not isinstance(frame, np.ndarray) or frame.ndim not in (2, 3):
            return self._invalid(target, t0, (0, 0), "invalid_frame")

        h, w = frame.shape[:2]
        x1, y1, x2, y2 = target.bbox_xyxy
        cx1, cy1 = max(0, x1), max(0, y1)
        cx2, cy2 = min(w, x2), min(h, y2)
        if cx2 - cx1 < 3 or cy2 - cy1 < 3:
            return self._invalid(target, t0, (max(0, cy2-cy1), max(0, cx2-cx1)), "empty_or_tiny_roi")

        boundary_clipped = (cx1, cy1, cx2, cy2) != (x1, y1, x2, y2)
        if boundary_clipped:
            notes.append("bbox_clipped_to_frame")

        roi = frame[cy1:cy2, cx1:cx2]
        gray = self._to_gray(roi)
        mask, seg_conf, mask_note = self._segment(gray)
        notes.append(mask_note)
        if mask is None:
            return self._invalid(target, t0, gray.shape[:2], "no_reliable_foreground", tuple(notes))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            return self._invalid(target, t0, gray.shape[:2], "no_contour", tuple(notes))
        contour = max(contours, key=cv2.contourArea)
        pts = contour.reshape(-1, 2).astype(np.float64)
        if len(pts) < 4:
            return self._invalid(target, t0, gray.shape[:2], "insufficient_contour_points", tuple(notes))

        moments = cv2.moments(contour)
        if abs(moments["m00"]) < 1e-9:
            center_local = pts.mean(axis=0)
        else:
            center_local = np.array([moments["m10"] / moments["m00"], moments["m01"] / moments["m00"]])

        centered = pts - center_local
        cov = np.cov(centered.T) if len(pts) > 2 else np.eye(2)
        vals, vecs = np.linalg.eigh(cov)
        order = np.argsort(vals)[::-1]
        vals, vecs = vals[order], vecs[:, order]
        major = vecs[:, 0]
        minor = vecs[:, 1]
        if major[0] < 0 or (abs(major[0]) < 1e-9 and major[1] < 0):
            major = -major
        if np.linalg.det(np.column_stack([major, minor])) < 0:
            minor = -minor

        axis_anisotropy = float(np.sqrt(max(vals[0], 1e-9) / max(vals[1], 1e-9)))
        proj_major = centered @ major
        pos_end = pts[int(np.argmax(proj_major))]
        neg_end = pts[int(np.argmin(proj_major))]
        left_candidates = pts[pts[:, 0] == pts[:, 0].min()]
        right_candidates = pts[pts[:, 0] == pts[:, 0].max()]
        left = left_candidates[np.argmin(np.abs(left_candidates[:, 1] - center_local[1]))]
        right = right_candidates[np.argmin(np.abs(right_candidates[:, 1] - center_local[1]))]

        polarity, polarity_conf = self._infer_polarity(centered, proj_major, minor)
        if axis_anisotropy < self.config.min_axis_anisotropy:
            polarity = 0
            polarity_conf *= 0.35
            notes.append("major_axis_ambiguous")
        if polarity > 0:
            nose_local, tail_local = pos_end, neg_end
        elif polarity < 0:
            nose_local, tail_local = neg_end, pos_end
        else:
            nose_local = tail_local = None
            notes.append("nose_tail_ambiguous")

        det_conf = float(np.clip(target.detection_confidence, 0.0, 1.0))
        boundary_factor = (1.0 - self.config.border_penalty) if boundary_clipped else 1.0
        base_conf = float(np.clip((0.60 * seg_conf + 0.25 * det_conf + 0.15 * min(axis_anisotropy / 2.0, 1.0)) * boundary_factor, 0, 1))
        semantic_conf = base_conf * polarity_conf

        def global_xy(p):
            if p is None:
                return None, None
            return float(p[0] + cx1), float(p[1] + cy1)

        center_g = global_xy(center_local)
        left_g = global_xy(left)
        right_g = global_xy(right)
        nose_g = global_xy(nose_local)
        tail_g = global_xy(tail_local)
        nt_valid = nose_local is not None and tail_local is not None and semantic_conf >= 0.25
        points = (
            SparsePoint(PointType.CENTER, *center_g, base_conf, True),
            SparsePoint(PointType.LEFT_SILHOUETTE, *left_g, base_conf, True),
            SparsePoint(PointType.RIGHT_SILHOUETTE, *right_g, base_conf, True),
            SparsePoint(PointType.NOSE, *nose_g, semantic_conf, nt_valid, "" if nt_valid else "ambiguous_axial_polarity"),
            SparsePoint(PointType.TAIL, *tail_g, semantic_conf, nt_valid, "" if nt_valid else "ambiguous_axial_polarity"),
        )
        geometry_conf = float(np.clip(0.75 * base_conf + 0.25 * semantic_conf, 0, 1))
        if base_conf < 0.20:
            validity = GeometryValidity.INVALID
        elif nt_valid and not boundary_clipped:
            validity = GeometryValidity.VALID
        else:
            validity = GeometryValidity.DEGRADED
        elapsed_ms = (perf_counter_ns() - t0) / 1e6
        return SparseGeometryObservation(target.frame_id, target.timestamp, target.target_id, target.target_class, target.bbox_xyxy, (center_g[0], center_g[1]), points, geometry_conf, target.source, elapsed_ms, validity, gray.shape[:2], tuple(notes))

    def _to_gray(self, roi: np.ndarray) -> np.ndarray:
        if roi.ndim == 2:
            return roi.astype(np.uint8, copy=False)
        if roi.shape[2] == 4:
            return cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY)
        return cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    def _segment(self, gray: np.ndarray):
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, a = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        b = cv2.bitwise_not(a)
        best = (-1e9, None, 0.0, "")
        for name, candidate in (("otsu", a), ("otsu_inv", b)):
            score, mask, conf = self._score_mask(candidate)
            if score > best[0]:
                best = (score, mask, conf, name)
        return best[1], best[2], best[3]

    def _score_mask(self, binary: np.ndarray):
        n, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, 8)
        H, W = binary.shape
        area_total = H * W
        best_score, best_mask, best_conf = -1e9, None, 0.0
        roi_center = np.array([W / 2.0, H / 2.0])
        diag = max(float(np.hypot(W, H)), 1.0)
        for label in range(1, n):
            area = int(stats[label, cv2.CC_STAT_AREA])
            frac = area / area_total
            if area < self.config.min_component_area_px or frac < self.config.min_component_area_fraction or frac > self.config.max_component_area_fraction:
                continue
            component = (labels == label).astype(np.uint8) * 255
            border_pixels = np.concatenate([component[0, :], component[-1, :], component[:, 0], component[:, -1]])
            border_frac = float(np.count_nonzero(border_pixels)) / max(len(border_pixels), 1)
            dist = float(np.linalg.norm(centroids[label] - roi_center) / diag)
            centrality = max(0.0, 1.0 - 2.0 * dist)
            compact_area = min(frac / 0.20, 1.0)
            score = 1.7 * centrality + 0.7 * compact_area - 2.2 * border_frac
            conf = float(np.clip(0.50 * centrality + 0.30 * compact_area + 0.20 * (1.0 - min(border_frac * 2.0, 1.0)), 0, 1))
            if score > best_score:
                kernel = np.ones((3, 3), np.uint8)
                clean = cv2.morphologyEx(component, cv2.MORPH_CLOSE, kernel, iterations=1)
                best_score, best_mask, best_conf = score, clean, conf
        return best_score, best_mask, best_conf

    def _infer_polarity(self, centered, proj_major, minor):
        lo, hi = float(proj_major.min()), float(proj_major.max())
        span = hi - lo
        if span < 2.0:
            return 0, 0.0
        band = max(span * self.config.endpoint_band_fraction, 1.0)
        proj_minor = centered @ minor
        pos = np.abs(proj_minor[proj_major >= hi - band])
        neg = np.abs(proj_minor[proj_major <= lo + band])
        if len(pos) < 2 or len(neg) < 2:
            return 0, 0.0
        pos_width = float(np.percentile(pos, 90)) * 2.0 + 1e-6
        neg_width = float(np.percentile(neg, 90)) * 2.0 + 1e-6
        ratio = max(pos_width, neg_width) / min(pos_width, neg_width)
        if ratio < self.config.nose_tail_width_ratio_threshold:
            return 0, float(np.clip((ratio - 1.0) / (self.config.nose_tail_width_ratio_threshold - 1.0), 0, 0.49))
        polarity = 1 if pos_width < neg_width else -1
        conf = float(np.clip((ratio - 1.0) / 1.2, 0.0, 1.0))
        return polarity, conf

    def _invalid(self, target, t0, roi_shape, reason, notes=()):
        elapsed_ms = (perf_counter_ns() - t0) / 1e6
        return SparseGeometryObservation(target.frame_id, target.timestamp, target.target_id, target.target_class, target.bbox_xyxy, None, (), 0.0, target.source, elapsed_ms, GeometryValidity.INVALID, roi_shape, notes + (reason,))
