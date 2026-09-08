import math
import unittest
from dataclasses import replace

from sparse_geometry_range_source import (
    CalibratedGeometryInput, CalibratedPoint, CameraCalibration, ExistingRangeObservation,
    PhysicalSpanSpec, RangeConfig, RangeValidity, SparseGeometryRangeSource,
    TargetGeometryProfile, compare_with_existing,
)

W=0.25
L=0.35
D=math.hypot(W/2, L/2)
CAL=CameraCalibration("HQ_PROVISIONAL_TEST", (2028,1520), 15756.86,15848.54,1014.0,760.0,
                      relative_scale_sigma=0.001, coordinates_undistorted=False, production_verified=False, provenance=(("fixture","SYNTHETIC"),))


def profile(width=W, length=L, sigma=0.002, production=False, projection=1.0, orient_sigma=0.0, include_diag=True):
    spans=[
        PhysicalSpanSpec("WIDTH","LEFT_SILHOUETTE","RIGHT_SILHOUETTE",width,sigma,True,"WIDTH","SYNTHETIC_EXPLICIT_WIDTH",projection,orient_sigma),
        PhysicalSpanSpec("LENGTH","NOSE","TAIL",length,sigma,True,"LENGTH","SYNTHETIC_EXPLICIT_LENGTH",projection,orient_sigma),
    ]
    if include_diag:
        diag=math.hypot(width/2,length/2)
        spans.append(PhysicalSpanSpec("LEFT_NOSE_DIAG","LEFT_SILHOUETTE","NOSE",diag,sigma,True,"DIAG","SYNTHETIC_EXPLICIT_STRUCTURAL_SPAN",projection,orient_sigma))
    return TargetGeometryProfile("SYNTH_TARGET","1","FPV_SYNTH",tuple(spans),(("fixture","SYNTHETIC"),),production)


def geom(z=20.0, projection=1.0, corrupt=None, invalid_nt=False, transform_valid=True, production_transform=False):
    # Construct points in normalized-camera geometry, then convert to pixels. Center at principal point.
    # All synthetic points lie at same depth and represent explicitly matched physical extrema.
    hw=(W*projection/z)/2
    hl=(L*projection/z)/2
    pts={
        "CENTER": (0.0,0.0),
        "LEFT_SILHOUETTE": (-hw,0.0),
        "RIGHT_SILHOUETTE": (hw,0.0),
        "NOSE": (0.0,-hl),
        "TAIL": (0.0,hl),
    }
    if corrupt:
        name, dx_px, dy_px=corrupt
        nx,ny=pts[name]
        pts[name]=(nx+dx_px/CAL.fx,ny+dy_px/CAL.fy)
    out=[]
    for name,(nx,ny) in pts.items():
        valid=True
        x=CAL.cx+nx*CAL.fx
        y=CAL.cy+ny*CAL.fy
        if invalid_nt and name in ("NOSE","TAIL"):
            valid=False; x=None; y=None
        out.append(CalibratedPoint(name,x,y,0.95,valid,"ambiguous_axial_polarity" if not valid else ""))
    return CalibratedGeometryInput("TASK2_SYNTH","f1",1.0,"t1","FPV_SYNTH",CAL.resolution_wh,
                                   "SYNTH_A","1",transform_valid,production_transform,0.001,tuple(out),(("fixture","SYNTHETIC"),))


class TestSparseRange(unittest.TestCase):
    def assertRange(self, obs, z, tol=0.08):
        self.assertNotEqual(obs.validity, RangeValidity.INVALID)
        self.assertAlmostEqual(obs.range_m,z,delta=tol)
        self.assertGreater(obs.sigma_m,0)

    def test_01_exact_top_down_multiple_ranges(self):
        src=SparseGeometryRangeSource(CAL,profile())
        for z in (8.0,20.0,50.0): self.assertRange(src.estimate(geom(z)),z)

    def test_02_multiple_consistent_spans(self):
        o=SparseGeometryRangeSource(CAL,profile()).estimate(geom(15.0))
        self.assertEqual(sum(c.accepted for c in o.candidates),3); self.assertRange(o,15.0)

    def test_03_one_corrupted_outlier(self):
        # Corrupt NOSE; LENGTH and DIAG move, so instead use a profile with a deliberately
        # separate explicit synthetic structural point span represented through NOSE only is correlated.
        # Here corruption is chosen to make DIAG the single robust residual outlier while width/length stay near center.
        g=geom(20.0)
        pts=list(g.points)
        idx=next(i for i,p in enumerate(pts) if p.point_type=="LEFT_SILHOUETTE")
        p=pts[idx]; pts[idx]=replace(p,y=p.y+55.0)
        g=replace(g,points=tuple(pts))
        o=SparseGeometryRangeSource(CAL,profile()).estimate(g)
        self.assertNotEqual(o.validity,RangeValidity.INVALID)
        self.assertTrue(any(c.rejection_reason=="consistency_outlier" for c in o.candidates))

    def test_04_insufficient_valid_spans(self):
        p=profile(include_diag=False)
        # unverify length correspondence leaves only WIDTH
        p=replace(p,spans=(p.spans[0],replace(p.spans[1],correspondence_verified=False)))
        o=SparseGeometryRangeSource(CAL,p).estimate(geom())
        self.assertEqual(o.validity,RangeValidity.INVALID); self.assertEqual(o.error,"insufficient_independent_evidence")

    def test_05_invalid_null_nose_tail_propagates(self):
        o=SparseGeometryRangeSource(CAL,profile()).estimate(geom(invalid_nt=True))
        nt=[c for c in o.candidates if "NOSE" in (c.point_a,c.point_b) or "TAIL" in (c.point_a,c.point_b)]
        self.assertTrue(all(not c.valid for c in nt)); self.assertTrue(all(c.range_m is None for c in nt))

    def test_06_uncertain_physical_dimension_increases_sigma(self):
        a=SparseGeometryRangeSource(CAL,profile(sigma=.001)).estimate(geom())
        b=SparseGeometryRangeSource(CAL,profile(sigma=.025)).estimate(geom())
        self.assertGreater(b.sigma_m,a.sigma_m)

    def test_07_disagreement_fail_closed(self):
        p=profile(include_diag=False)
        # profile LENGTH is intentionally inconsistent fixture physical model
        p=replace(p,spans=(p.spans[0],replace(p.spans[1],length_m=L*1.8)))
        o=SparseGeometryRangeSource(CAL,p).estimate(geom())
        self.assertEqual(o.validity,RangeValidity.INVALID); self.assertEqual(o.error,"candidate_disagreement")

    def test_08_malformed_calibration_or_transform(self):
        bad=replace(CAL,fx=0)
        self.assertEqual(SparseGeometryRangeSource(bad,profile()).estimate(geom()).validity,RangeValidity.INVALID)
        self.assertEqual(SparseGeometryRangeSource(CAL,profile()).estimate(geom(transform_valid=False)).validity,RangeValidity.INVALID)

    def test_09_near_zero_image_span(self):
        g=geom(); pts=list(g.points)
        l=next(p for p in pts if p.point_type=="LEFT_SILHOUETTE")
        for i,p in enumerate(pts):
            if p.point_type=="RIGHT_SILHOUETTE": pts[i]=replace(p,x=l.x,y=l.y)
        o=SparseGeometryRangeSource(CAL,profile()).estimate(replace(g,points=tuple(pts)))
        w=next(c for c in o.candidates if c.span_id=="WIDTH")
        self.assertFalse(w.valid); self.assertEqual(w.rejection_reason,"near_zero_image_span")

    def test_10_mild_synthetic_foreshortening_explicit(self):
        q=0.94
        p=profile(projection=q,orient_sigma=.02)
        o=SparseGeometryRangeSource(CAL,p).estimate(geom(25.0,projection=q))
        self.assertRange(o,25.0,0.12); self.assertGreater(o.sigma_m,0.3)

    def test_11_range_uncertainty_grows_with_point_error_at_far_range(self):
        cfg=RangeConfig(point_sigma_px=1.2)
        src=SparseGeometryRangeSource(CAL,profile(),cfg)
        near=src.estimate(geom(8.0)); far=src.estimate(geom(50.0))
        self.assertGreater(far.sigma_m,near.sigma_m)

    def test_12_repeatability(self):
        src=SparseGeometryRangeSource(CAL,profile()); g=geom(20.0)
        vals=[src.estimate(g) for _ in range(10)]
        self.assertTrue(all(v.range_m==vals[0].range_m and v.sigma_m==vals[0].sigma_m for v in vals))

    def test_13_unverified_correspondence_rejected(self):
        p=profile(); p=replace(p,spans=tuple(replace(s,correspondence_verified=False) for s in p.spans))
        o=SparseGeometryRangeSource(CAL,p).estimate(geom())
        self.assertEqual(o.validity,RangeValidity.INVALID)
        self.assertTrue(all(c.rejection_reason=="physical_correspondence_not_verified" for c in o.candidates))

    def test_14_production_metric_gate(self):
        o=SparseGeometryRangeSource(CAL,profile(production=False)).estimate(geom(production_transform=False))
        self.assertFalse(o.production_metric_verified); self.assertEqual(o.validity,RangeValidity.DEGRADED)

    def test_15_nonzero_distortion_requires_undistorted_coordinates(self):
        bad=replace(CAL,distortion=(0.1,0,0,0,0),coordinates_undistorted=False)
        o=SparseGeometryRangeSource(bad,profile()).estimate(geom())
        self.assertEqual(o.validity,RangeValidity.INVALID)
        self.assertIn("distortion_not_supported",o.error)

    def test_16_production_gate_requires_calibration_too(self):
        c=replace(CAL,production_verified=False)
        o=SparseGeometryRangeSource(c,profile(production=True)).estimate(geom(production_transform=True))
        self.assertFalse(o.production_metric_verified)

    def test_17_existing_range_shadow_comparison(self):
        sparse=SparseGeometryRangeSource(CAL,profile()).estimate(geom(20.0))
        old=ExistingRangeObservation("MONOCULAR_CLASS_SIZE",21.0,2.0,.7,True)
        c=compare_with_existing(old,sparse)
        self.assertTrue(c.comparable); self.assertAlmostEqual(c.absolute_delta_m,1.0,places=6)

    def test_18_candidate_exposes_calibrated_pixel_span_and_full_provenance(self):
        o=SparseGeometryRangeSource(CAL,profile()).estimate(geom(20.0))
        c=next(c for c in o.candidates if c.span_id=="WIDTH")
        self.assertGreater(c.calibrated_length_px,0.0)
        keys=dict(c.provenance)
        self.assertEqual(keys["source_geometry_ref"],"TASK2_SYNTH")
        self.assertEqual(keys["calibration_id"],CAL.calibration_id)
        self.assertEqual(keys["transform_id"],"SYNTH_A")


if __name__=='__main__': unittest.main()
