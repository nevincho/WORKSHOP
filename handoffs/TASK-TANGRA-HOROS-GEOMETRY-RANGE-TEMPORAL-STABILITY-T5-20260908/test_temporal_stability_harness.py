import unittest
from temporal_stability_harness import *
class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.m,cls.r=run_all()
    def test_static_noise_stability(self):
        x=self.m['A_STATIC_NOISE']; self.assertLessEqual(x['center_rms_jitter_px'],1.5); self.assertLessEqual(x['fused_range_cv'],.03)
    def test_translation_stability(self): self.assertLessEqual(self.m['B_TRANSLATION']['fused_range_cv'],.03)
    def test_scale_monotonicity(self):
        z=[r.fused_range_m for r in self.r['C_SCALE_CHANGE'] if r.fused_range_m is not None]; self.assertTrue(all(z[i+1] <= z[i]+.35 for i in range(len(z)-1)))
    def test_mild_orientation(self): self.assertLessEqual(self.m['D_ROTATION']['fused_range_cv'],.03)
    def test_foreshortening_bounded(self): self.assertLess(self.m['E_FORESHORTEN']['max_transient_error_m'],1.5)
    def test_corrupted_frame_bounded(self):
        r=self.r['F_CORRUPT'][40]; self.assertTrue(r.state in (State.DEGRADED,State.CONFLICT,State.INVALID)); self.assertTrue(r.fused_range_m is None or abs(r.fused_range_m-r.truth_range_m)<1.5)
    def test_weak_contrast_degradation(self): self.assertGreaterEqual(self.m['G_WEAK_CONTRAST']['invalid_frames'],5)
    def test_axial_ambiguity(self):
        self.assertLess(self.m['H_AXIAL_AMBIGUITY']['nose_tail_valid_rate'],1.0); [self.assertIsNotNone(self.r['H_AXIAL_AMBIGUITY'][i].fused_range_m) for i in range(30,35)]
    def test_partial_silhouette(self): [self.assertIsNotNone(self.r['I_PARTIAL_SILHOUETTE'][i].fused_range_m) for i in range(30,35)]
    def test_recovery(self): self.assertIsNotNone(self.r['G_WEAK_CONTRAST'][35].fused_range_m)
    def test_no_cross_target_state(self):
        ev=EveryFrameEvaluator(); a=build_sequences()['A_STATIC_NOISE'][0]; b=FrameFixture(**{**a.__dict__,'target_id':'TGT-B','index':999}); self.assertEqual(ev.evaluate(b).target_id,'TGT-B')
    def test_repeatability(self):
        m2,_=run_all();
        for k in self.m:
            for f in ('lr_span_cv','fused_range_cv','range_bias_m','invalid_frames'): self.assertAlmostEqual(self.m[k][f],m2[k][f],places=12)
    def test_fusion_state_transition(self):
        rr=self.r['G_WEAK_CONTRAST']; self.assertEqual(rr[29].state,State.DEGRADED); self.assertEqual(rr[30].state,State.INVALID); self.assertEqual(rr[35].state,State.DEGRADED)
    def test_frozen_contract_constants(self):
        self.assertEqual(TASK1_COMMIT,'c7b378841979f82b037c47be3571fa72a7b70e51'); self.assertEqual(TASK2_COMMIT,'4bd4b5d38357db501de07511aeabaa4c0ae058e1'); self.assertEqual(TASK3_COMMIT,'c121ce25dbba84520c6f8e644281a7cb2bf3ee73'); self.assertEqual(TASK4_COMMIT,'7f628a727b89599ea6977053ea12211b10e0ffcd')
    def test_decision(self): self.assertTrue(decision(self.m))
if __name__=='__main__': unittest.main()
