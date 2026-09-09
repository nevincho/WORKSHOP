import unittest
from navigation_evidence_adapter import *


def src(**kw):
    d=dict(target_ref="T1",timestamp=10.0,frame_ref="HOROS_LOCAL",frame_semantics=FrameSemantics.CARRIER_RELATIVE_LOCAL_METRIC,lifecycle=Lifecycle.ESTIMATED,metric_status=MetricStatus.VERIFIED,observation_age_s=0.1,target_xyz_m=(10.0,5.0,2.0),position_covariance_m2=(1.0,0.0,0.0,0.0,4.0,0.0,0.0,0.0,9.0),covariance_semantics=COVARIANCE_SEMANTICS,carrier_origin_is_zero=True,provenance=(("horos","TEST"),),production_authority=False)
    d.update(kw)
    return HorosTargetNavigationSource(**d)

class N1BoundaryAdversarialTests(unittest.TestCase):
    def test_01_covariance_semantics_object_cannot_spoof_string(self):
        class FakeSemantics:
            def __eq__(self, other): return True
            def __ne__(self, other): return False
        r=build_m2_navigation_evidence(src(covariance_semantics=FakeSemantics()),"T1","HOROS_LOCAL",10.1)
        self.assertIsNone(r.m2_kwargs)
        self.assertEqual(r.reason,"verified_covariance_unavailable_or_invalid")

    def test_02_malformed_expected_target_ref_fails_closed(self):
        class FakeRef:
            def __eq__(self, other): return True
        r=build_m2_navigation_evidence(src(),FakeRef(),"HOROS_LOCAL",10.1)
        self.assertIsNone(r.m2_kwargs)
        self.assertEqual(r.reason,"expected_target_ref_invalid")

    def test_03_malformed_expected_frame_ref_fails_closed(self):
        class FakeRef:
            def __eq__(self, other): return True
        r=build_m2_navigation_evidence(src(),"T1",FakeRef(),10.1)
        self.assertIsNone(r.m2_kwargs)
        self.assertEqual(r.reason,"expected_frame_ref_invalid")

    def test_04_whitespace_source_refs_fail_closed(self):
        r=build_m2_navigation_evidence(src(target_ref=" "),"T1","HOROS_LOCAL",10.1)
        self.assertIsNone(r.m2_kwargs)
        r=build_m2_navigation_evidence(src(frame_ref=" "),"T1"," ",10.1)
        self.assertIsNone(r.m2_kwargs)

    def test_05_malformed_search_refs_fail_closed_without_equality_bypass(self):
        class FakeRef:
            def __eq__(self, other): return True
        search=ExplicitSearchGeometry(FakeRef(),10.0,FakeRef(),MetricStatus.VERIFIED,(1.0,0.0,0.0))
        r=build_m2_navigation_evidence(src(),"T1","HOROS_LOCAL",10.1,search=search)
        self.assertIsNone(r.m2_kwargs)
        self.assertEqual(r.reason,"search_target_mismatch")

if __name__=="__main__":
    unittest.main()
