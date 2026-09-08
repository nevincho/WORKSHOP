import unittest
import numpy as np
from ai_calibrated_geometry_adapter import *

AI=PlaneSpec("HQ_AI",(640,640))
CAL=PlaneSpec("HQ_CAL",(2028,1520))

def mk(A):
    return AICalibratedGeometryAdapter(GeometryTransform("t","1",AI,CAL,A))

def geo():
    pts=(SparsePointLike("CENTER",320,320,.9,True), SparsePointLike("NOSE",None,None,.2,False,"ambiguous"), SparsePointLike("TAIL",500,300,.7,True))
    return Task1GeometryLike("f1",1.2,"t1","FPV",(100,120,500,520),(320,320),pts,"TASK1")

class T(unittest.TestCase):
    def assertP(self,a,b,tol=1e-9):
        self.assertTrue(np.allclose(a,b,atol=tol,rtol=0), (a,b))
    def test_identity(self):
        e=mk(affine_axis_aligned(1,1,0,0)); self.assertP(e.ai_to_cal((10,20)),(10,20))
    def test_anisotropic_full_frame_resize(self):
        sx,sy=640/2028,640/1520; e=mk(center_aligned_crop_resize((0,0),(sx,sy)))
        self.assertP(e.cal_to_ai((0,0)),((sx-1)/2,(sy-1)/2))
        self.assertP(e.cal_to_ai((2027,1519)),((2027.5)*sx-.5,(1519.5)*sy-.5))
        self.assertP(e.ai_to_cal(e.cal_to_ai((1014,760))),(1014,760))
    def test_crop_resize(self):
        sx,sy=640/1600,640/1200; e=mk(center_aligned_crop_resize((200,100),(sx,sy)))
        self.assertP(e.cal_to_ai((200,100)),((sx-1)/2,(sy-1)/2))
        self.assertP(e.ai_to_cal(((sx-1)/2,(sy-1)/2)),(200,100))
    def test_padding_letterbox_inverse(self):
        s=640/2028; pad_y=(640-1520*s)/2; e=mk(center_aligned_crop_resize((0,0),(s,s),(0,pad_y)))
        expected=((s-1)/2,(s-1)/2+pad_y)
        self.assertP(e.cal_to_ai((0,0)),expected); self.assertP(e.ai_to_cal(expected),(0,0))
    def test_round_trip_both_directions(self):
        e=mk(affine_axis_aligned(.31,.42,7.5,13.0))
        for p in [(0,0),(1014,760),(2027,1519)]: self.assertP(e.ai_to_cal(e.cal_to_ai(p)),p,1e-8)
        for p in [(0,0),(320,320),(639,639)]: self.assertP(e.cal_to_ai(e.ai_to_cal(p)),p,1e-8)
    def test_bbox_mapping(self):
        e=mk(affine_axis_aligned(.5,.25,10,20)); o=e.adapt(geo())
        self.assertP(o.bbox_xyxy,((100-10)/.5,(120-20)/.25,(500-10)/.5,(520-20)/.25))
    def test_task1_sparse_points(self):
        e=mk(affine_axis_aligned(.5,.5,0,0)); o=e.adapt(geo())
        self.assertP((o.points[0].x,o.points[0].y),(640,640)); self.assertTrue(o.transform_valid)
    def test_null_invalid_preserved(self):
        e=mk(affine_axis_aligned(.5,.5,0,0)); o=e.adapt(geo())
        p=o.points[1]; self.assertFalse(p.valid); self.assertIsNone(p.x); self.assertIsNone(p.y)
    def test_boundary_corner_coordinates(self):
        sx,sy=640/2028,640/1520; e=mk(center_aligned_crop_resize((0,0),(sx,sy)))
        self.assertP(e.cal_to_ai((0,0)),((sx-1)/2,(sy-1)/2))
        self.assertP(e.cal_to_ai((2027,1519)),((2027.5)*sx-.5,(1519.5)*sy-.5))
    def test_noninvertible_fail_closed(self):
        e=mk(((1,0,0),(0,0,0),(0,0,1))); o=e.adapt(geo())
        self.assertFalse(o.transform_valid); self.assertIsNone(o.bbox_xyxy); self.assertIsNone(o.center)
        self.assertTrue(all((not p.valid and p.x is None and p.y is None) for p in o.points))
    def test_malformed_non_affine_fail_closed(self):
        e=mk(((1,0,0),(0,1,0),(.1,0,1))); o=e.adapt(geo()); self.assertFalse(o.transform_valid)
    def test_intrinsics_consistency(self):
        A=affine_axis_aligned(.3,.4,8,12); e=mk(A)
        K=np.array([[15756.86,0,1014],[0,15848.54,760],[0,0,1.]],float)
        Kai=e.intrinsics_cal_to_ai(K); p=np.array([.02,-.01,1.]); cal=K@p; cal_xy=cal[:2]/cal[2]; ai=Kai@p; ai_xy=ai[:2]/ai[2]
        self.assertP(ai_xy,e.cal_to_ai(tuple(cal_xy)),1e-8)

if __name__=="__main__": unittest.main(verbosity=2)
