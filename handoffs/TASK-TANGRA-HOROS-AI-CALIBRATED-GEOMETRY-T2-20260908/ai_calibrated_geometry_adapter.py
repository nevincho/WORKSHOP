from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
import math
import numpy as np

Point2 = Tuple[float, float]
BBox = Tuple[float, float, float, float]

@dataclass(frozen=True)
class PlaneSpec:
    name: str
    resolution_wh: Tuple[int, int]

@dataclass(frozen=True)
class GeometryTransform:
    transform_id: str
    version: str
    source_plane: PlaneSpec
    destination_plane: PlaneSpec
    matrix_src_from_dst: Tuple[Tuple[float,float,float],Tuple[float,float,float],Tuple[float,float,float]]
    pixel_convention: str = "continuous_image_coordinates; integer values denote pixel centers; origin=(0,0) at top-left pixel center"
    metadata: Tuple[Tuple[str,str], ...] = ()

    def matrix(self) -> np.ndarray:
        A=np.asarray(self.matrix_src_from_dst, dtype=np.float64)
        if A.shape != (3,3) or not np.all(np.isfinite(A)):
            raise ValueError("malformed_transform")
        if not np.allclose(A[2], [0.0,0.0,1.0], atol=1e-12):
            raise ValueError("non_affine_transform")
        if abs(np.linalg.det(A)) < 1e-12:
            raise ValueError("non_invertible_transform")
        return A

@dataclass(frozen=True)
class SparsePointLike:
    point_type: str
    x: Optional[float]
    y: Optional[float]
    confidence: float
    valid: bool
    reason: str = ""

@dataclass(frozen=True)
class Task1GeometryLike:
    frame_id: Optional[str]
    timestamp: Optional[float]
    target_id: Optional[str]
    target_class: str
    bbox_xyxy: BBox
    center: Optional[Point2]
    points: Tuple[SparsePointLike, ...]
    source: str
    provenance: Tuple[Tuple[str,str], ...] = ()

@dataclass(frozen=True)
class CalibratedGeometry:
    source_geometry_ref: str
    source_plane: PlaneSpec
    destination_plane: PlaneSpec
    transform_id: str
    transform_version: str
    transform_parameters: Tuple[Tuple[float,float,float],Tuple[float,float,float],Tuple[float,float,float]]
    bbox_xyxy: Optional[BBox]
    center: Optional[Point2]
    points: Tuple[SparsePointLike, ...]
    provenance: Tuple[Tuple[str,str], ...]
    transform_valid: bool
    frame_id: Optional[str]
    timestamp: Optional[float]
    metadata: Tuple[Tuple[str,str], ...] = ()
    error: str = ""

class AICalibratedGeometryAdapter:
    """Coordinate-only adapter. The stored matrix maps destination(CAL)->source(AI)."""

    def __init__(self, transform: GeometryTransform):
        self.transform = transform

    def _matrices(self):
        A = self.transform.matrix()
        return A, np.linalg.inv(A)

    @staticmethod
    def _apply(M: np.ndarray, p: Point2) -> Point2:
        v=M @ np.array([float(p[0]), float(p[1]), 1.0])
        return (float(v[0]), float(v[1]))

    def cal_to_ai(self, p: Point2) -> Point2:
        A,_=self._matrices()
        return self._apply(A,p)

    def ai_to_cal(self, p: Point2) -> Point2:
        _,Ai=self._matrices()
        return self._apply(Ai,p)

    def intrinsics_cal_to_ai(self, K_cal: np.ndarray) -> np.ndarray:
        A,_=self._matrices()
        K=np.asarray(K_cal,dtype=np.float64)
        if K.shape != (3,3):
            raise ValueError("malformed_intrinsics")
        return A @ K

    def _map_bbox_ai_to_cal(self, bbox: BBox) -> BBox:
        x1,y1,x2,y2=map(float,bbox)
        pts=[self.ai_to_cal((x1,y1)), self.ai_to_cal((x1,y2)), self.ai_to_cal((x2,y1)), self.ai_to_cal((x2,y2))]
        xs=[p[0] for p in pts]
        ys=[p[1] for p in pts]
        return (min(xs),min(ys),max(xs),max(ys))

    def adapt(self, g: Task1GeometryLike) -> CalibratedGeometry:
        try:
            self._matrices()
            bbox=self._map_bbox_ai_to_cal(g.bbox_xyxy)
            center=None if g.center is None else self.ai_to_cal(g.center)
            out=[]
            for p in g.points:
                if (not p.valid) or p.x is None or p.y is None:
                    out.append(SparsePointLike(p.point_type,None,None,p.confidence,False,p.reason))
                else:
                    x,y=self.ai_to_cal((p.x,p.y))
                    out.append(SparsePointLike(p.point_type,x,y,p.confidence,True,p.reason))
            return CalibratedGeometry(
                source_geometry_ref=f"{g.source}:{g.frame_id or 'unknown'}:{g.target_id or 'unknown'}",
                source_plane=self.transform.source_plane,
                destination_plane=self.transform.destination_plane,
                transform_id=self.transform.transform_id,
                transform_version=self.transform.version,
                transform_parameters=self.transform.matrix_src_from_dst,
                bbox_xyxy=bbox,
                center=center,
                points=tuple(out),
                provenance=g.provenance + (("adapter","AI_TO_CALIBRATED_HQ"),),
                transform_valid=True,
                frame_id=g.frame_id,
                timestamp=g.timestamp,
                metadata=self.transform.metadata)
        except Exception as e:
            return CalibratedGeometry(
                source_geometry_ref=f"{g.source}:{g.frame_id or 'unknown'}:{g.target_id or 'unknown'}",
                source_plane=self.transform.source_plane,
                destination_plane=self.transform.destination_plane,
                transform_id=self.transform.transform_id,
                transform_version=self.transform.version,
                transform_parameters=self.transform.matrix_src_from_dst,
                bbox_xyxy=None,
                center=None,
                points=tuple(SparsePointLike(p.point_type,None,None,p.confidence,False,p.reason or "transform_invalid") for p in g.points),
                provenance=g.provenance + (("adapter","AI_TO_CALIBRATED_HQ"),),
                transform_valid=False,
                frame_id=g.frame_id,
                timestamp=g.timestamp,
                metadata=self.transform.metadata,
                error=str(e))

def center_aligned_crop_resize(
    crop_origin_xy: Point2,
    scale_xy: Point2,
    pad_xy: Point2 = (0.0, 0.0),
) -> Tuple[Tuple[float,float,float],...]:
    """CAL->AI affine for crop then resize under the declared pixel-center convention."""
    cx, cy = map(float, crop_origin_xy)
    sx, sy = map(float, scale_xy)
    px, py = map(float, pad_xy)
    tx = -sx * cx + 0.5 * sx - 0.5 + px
    ty = -sy * cy + 0.5 * sy - 0.5 + py
    return affine_axis_aligned(sx, sy, tx, ty)

def affine_axis_aligned(sx: float, sy: float, tx: float, ty: float) -> Tuple[Tuple[float,float,float],...]:
    vals=(sx,sy,tx,ty)
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("non_finite_transform_parameter")
    return ((float(sx),0.0,float(tx)),(0.0,float(sy),float(ty)),(0.0,0.0,1.0))
