import copy
import hashlib
import unittest

import cv2
import numpy as np

from sparse_target_geometry import GeometryValidity, PointType, SparseTargetGeometryExtractor, TargetGeometryInput


def fixture(angle=0.0, clipped=False, symmetric=False, fg=30, bg=230):
    img = np.full((220, 260, 3), bg, np.uint8)
    cx, cy = (32, 45) if clipped else (130, 110)
    if symmetric:
        poly = np.array([[-55,-10],[-12,-10],[-12,-35],[12,-35],[12,-10],[55,-10],[55,10],[12,10],[12,35],[-12,35],[-12,10],[-55,10]], np.float32)
    else:
        poly = np.array([[58,0],[14,-12],[-18,-28],[-42,-28],[-30,-10],[-58,-10],[-58,10],[-30,10],[-42,28],[-18,28],[14,12]], np.float32)
    th = np.deg2rad(angle)
    R = np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]])
    p = (poly @ R.T) + [cx, cy]
    cv2.fillPoly(img, [np.rint(p).astype(np.int32)], (fg,fg,fg))
    x1,y1 = np.floor(p.min(axis=0)-8).astype(int)
    x2,y2 = np.ceil(p.max(axis=0)+8).astype(int)
    if clipped:
        x1 -= 25; y1 -= 25
    return img, (int(x1),int(y1),int(x2),int(y2))


def meta(bbox, conf=0.91):
    return TargetGeometryInput("frame-7", 123.5, "target-2", "FPV", conf, bbox)


class GeometryTests(unittest.TestCase):
    def setUp(self): self.e = SparseTargetGeometryExtractor()
    def test_near_top_down(self):
        img,b=fixture(0); o=self.e.extract(img,meta(b))
        self.assertIn(o.validity,(GeometryValidity.VALID,GeometryValidity.DEGRADED))
        self.assertEqual([p.point_type for p in o.points],[PointType.CENTER,PointType.LEFT_SILHOUETTE,PointType.RIGHT_SILHOUETTE,PointType.NOSE,PointType.TAIL])
        self.assertGreater(o.geometry_confidence,0.35)
    def test_mild_oblique_top_down_proxy(self):
        img,b=fixture(23); o=self.e.extract(img,meta(b))
        self.assertGreaterEqual(sum(p.valid for p in o.points),3)
    def test_point_order_repeatability(self):
        img,b=fixture(17); a=self.e.extract(img,meta(b)); c=self.e.extract(img,meta(b))
        self.assertEqual([(p.point_type,p.x,p.y,p.valid) for p in a.points],[(p.point_type,p.x,p.y,p.valid) for p in c.points])
    def test_geometry_confidence_tracks_detection_confidence(self):
        img,b=fixture(0)
        self.assertGreater(self.e.extract(img,meta(b,0.95)).geometry_confidence,self.e.extract(img,meta(b,0.10)).geometry_confidence)
    def test_ambiguous_nose_tail_is_not_fabricated(self):
        img,b=fixture(0,symmetric=True); o=self.e.extract(img,meta(b))
        nt=[p for p in o.points if p.point_type in (PointType.NOSE,PointType.TAIL)]
        self.assertTrue(all(not p.valid for p in nt)); self.assertTrue(all(p.x is None and p.y is None for p in nt)); self.assertIn("nose_tail_ambiguous",o.notes)
    def test_weak_contrast_fails_closed(self):
        img,b=fixture(0,fg=124,bg=128); o=self.e.extract(img,meta(b))
        self.assertEqual(o.validity,GeometryValidity.INVALID); self.assertEqual(o.geometry_confidence,0.0); self.assertIn("weak_photometric_separation",o.notes)
    def test_roi_boundary_case(self):
        img,b=fixture(0,clipped=True); o=self.e.extract(img,meta(b))
        self.assertIn("bbox_clipped_to_frame",o.notes); self.assertNotEqual(o.validity,GeometryValidity.VALID)
    def test_repeatability_on_unchanged_input(self):
        img,b=fixture(11); outputs=[self.e.extract(img,meta(b)) for _ in range(5)]
        sig=[(x.validity,round(x.geometry_confidence,12),[(p.point_type,p.x,p.y,p.valid) for p in x.points]) for x in outputs]
        self.assertTrue(all(s==sig[0] for s in sig[1:]))
    def test_no_mutation_of_upstream_data(self):
        img,b=fixture(9); t=meta(b); before=hashlib.sha256(img.tobytes()).hexdigest(); t_before=copy.deepcopy(t)
        self.e.extract(img,t)
        self.assertEqual(before,hashlib.sha256(img.tobytes()).hexdigest()); self.assertEqual(t,t_before)
    def test_invalid_blank_roi(self):
        img=np.full((100,100,3),127,np.uint8); o=self.e.extract(img,meta((20,20,80,80)))
        self.assertEqual(o.validity,GeometryValidity.INVALID)


if __name__ == "__main__": unittest.main(verbosity=2)
