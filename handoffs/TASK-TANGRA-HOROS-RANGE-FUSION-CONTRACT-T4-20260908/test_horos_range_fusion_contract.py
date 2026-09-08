import math, unittest
from horos_range_fusion_contract import *


def mono(z=20.0,s=1.0,c=.8,verified=True,group="mono",valid=True):
    return adapt_monocular_class_size(ExistingMonocularClassSizeInput("v1",z,s,c,valid,verified,"f",1.0,"t",group,(("src","mono"),)))

def sparse(z=20.2,s=.8,c=.9,verified=False,group="sparse",valid=True,transform_valid=True):
    return adapt_sparse_geometry(SparseGeometryRangeInput("t3",z,s,c,valid,verified,transform_valid,verified,"f",1.0,"t",group,(("src","sparse"),)))

class T(unittest.TestCase):
    def setUp(self): self.f=HorosRangeFusionContract()
    def test_one_valid_mono(self):
        o=self.f.fuse((mono(),)); self.assertEqual(o.state,FusionState.VALID); self.assertAlmostEqual(o.range_m,20)
    def test_one_sparse_degraded(self):
        o=self.f.fuse((sparse(),)); self.assertEqual(o.state,FusionState.DEGRADED); self.assertEqual(o.metric_usability,MetricUsability.NOT_VERIFIED)
    def test_two_compatible(self):
        o=self.f.fuse((mono(),sparse(20.1,verified=True))); self.assertEqual(o.state,FusionState.VALID); self.assertTrue(20<=o.range_m<=20.1)
    def test_conflict(self):
        o=self.f.fuse((mono(20,.5),sparse(40,.5,verified=True))); self.assertEqual(o.state,FusionState.CONFLICT); self.assertIsNone(o.range_m); self.assertTrue(o.conflict)
    def test_correlated_prevent_double_count(self):
        a=mono(20,2,.8,group="same"); b=sparse(20.1,1,.9,verified=True,group="same")
        o=self.f.fuse((a,b)); self.assertEqual(len(o.contributing_sources),1); self.assertTrue(any(r.reason=="correlated_duplicate_not_counted" for r in o.rejected_sources))
    def test_invalid_nonfinite(self):
        e=replace(mono(),range_m=float('nan')); o=self.f.fuse((e,)); self.assertEqual(o.state,FusionState.INVALID)
    def test_unusable_metric(self):
        e=replace(mono(),metric_usability=MetricUsability.UNUSABLE); o=self.f.fuse((e,)); self.assertEqual(o.state,FusionState.INVALID)
    def test_uncertainty_weighted(self):
        o=self.f.fuse((mono(10,4,.8),sparse(12,.5,.9,verified=True))); self.assertGreater(o.range_m,11.5)
    def test_disagreement_increases_uncertainty(self):
        a=self.f.fuse((mono(20,1),sparse(20,1,verified=True)))
        b=self.f.fuse((mono(20,1),sparse(22,1,verified=True)))
        self.assertGreaterEqual(b.sigma_m,a.sigma_m)
    def test_not_verified_propagates(self):
        o=self.f.fuse((mono(20,1,verified=False),sparse(20,1,verified=False))); self.assertEqual(o.metric_usability,MetricUsability.NOT_VERIFIED); self.assertEqual(o.state,FusionState.DEGRADED)
    def test_provenance(self):
        o=self.f.fuse((mono(),sparse(20,1,verified=True))); p=dict(o.provenance); self.assertIn("contributor",p); self.assertIn(("src","mono"),o.provenance); self.assertIn(("src","sparse"),o.provenance)
    def test_los_compatible_no_bearing_fabrication(self):
        o=self.f.fuse((mono(),)); l=to_los_range_compatible(o); self.assertEqual(l.range_m,o.range_m); self.assertEqual(l.sigma_m,o.sigma_m); self.assertIsNone(l.bearing); self.assertIsNone(l.los); self.assertTrue(l.valid)
    def test_missing_uncertainty(self):
        e=replace(mono(),sigma_m=None); self.assertEqual(self.f.fuse((e,)).state,FusionState.INVALID)
    def test_missing_confidence(self):
        e=replace(mono(),confidence=None); self.assertEqual(self.f.fuse((e,)).state,FusionState.INVALID)
    def test_target_reference_conflict_fails_closed(self):
        a=mono(); b=replace(sparse(20,1,verified=True), target_ref="other")
        o=self.f.fuse((a,b)); self.assertEqual(o.state,FusionState.INVALID); self.assertEqual(o.reason,"target_reference_conflict")
    def test_frame_reference_conflict_fails_closed(self):
        a=mono(); b=replace(sparse(20,1,verified=True), frame_id="other-frame")
        o=self.f.fuse((a,b)); self.assertEqual(o.state,FusionState.INVALID); self.assertEqual(o.reason,"frame_reference_conflict")
    def test_soft_disagreement_degrades(self):
        o=self.f.fuse((mono(20,.7,1),sparse(23,.7,1,verified=True)))
        self.assertEqual(o.state,FusionState.DEGRADED); self.assertIsNotNone(o.range_m); self.assertFalse(o.conflict)
    def test_repeatability(self):
        es=(mono(20,1,.8),sparse(20.3,.8,.9,verified=True)); a=self.f.fuse(es); b=self.f.fuse(es)
        self.assertEqual((a.range_m,a.sigma_m,a.state,a.provenance),(b.range_m,b.sigma_m,b.state,b.provenance))
    def test_confidence_inflates_effective_sigma(self):
        hi=self.f.fuse((mono(10,1,1),sparse(12,1,1,verified=True)))
        lo=self.f.fuse((mono(10,1,.1),sparse(12,1,.1,verified=True)))
        self.assertGreaterEqual(lo.sigma_m,hi.sigma_m)
    def test_invalid_sparse_transform_unusable(self):
        e=sparse(transform_valid=False); self.assertEqual(e.metric_usability,MetricUsability.UNUSABLE); self.assertEqual(self.f.fuse((e,)).state,FusionState.INVALID)
    def test_agreement_does_not_upgrade(self):
        o=self.f.fuse((mono(20,1,verified=False),sparse(20,1,verified=False))); self.assertNotEqual(o.metric_usability,MetricUsability.VERIFIED)

if __name__=='__main__': unittest.main()
