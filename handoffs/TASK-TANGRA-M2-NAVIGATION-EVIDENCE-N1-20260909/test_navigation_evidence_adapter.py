import inspect
import unittest
import math
import importlib.util
from pathlib import Path
from navigation_evidence_adapter import *

REPO_ROOT = Path(__file__).resolve().parents[2]

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

m1 = load("frozen_m1_n1", "handoffs/TASK-TANGRA-MISSION-MANAGEMENT-GUIDANCE-M1-20260908/mission_management_contract.py")
m2 = load("frozen_m2_n1", "handoffs/TASK-TANGRA-MISSION-GUIDANCE-M2-20260908/passive_guidance_translation.py")
m3 = load("frozen_m3_n1", "handoffs/TASK-TANGRA-MISSION-GUIDANCE-M3-20260908/passive_high_level_command_contract.py")

def src(**kw):
    d=dict(target_ref="T1",timestamp=10.0,frame_ref="HOROS_LOCAL",frame_semantics=FrameSemantics.CARRIER_RELATIVE_LOCAL_METRIC,lifecycle=Lifecycle.ESTIMATED,metric_status=MetricStatus.VERIFIED,observation_age_s=0.1,target_xyz_m=(10.0,5.0,2.0),position_covariance_m2=(1.0,0.0,0.0,0.0,4.0,0.0,0.0,0.0,9.0),covariance_semantics=COVARIANCE_SEMANTICS,carrier_origin_is_zero=True,provenance=(("horos","TEST"),),production_authority=False)
    d.update(kw); return HorosTargetNavigationSource(**d)

def adapt(s=None, **kw): return build_m2_navigation_evidence(s or src(),"T1","HOROS_LOCAL",10.1,**kw)

def m2nav(result):
    d=result.as_dict()
    if d is None: return None
    d["lifecycle"]=m2.Lifecycle(d["lifecycle"]); d["metric_status"]=m2.MetricStatus(d["metric_status"])
    return m2.NavigationEvidence(**d)

def md(action=m1.MissionAction.MAINTAIN_TRACK,state=m1.MissionState.TRACK,metric=m1.MetricStatus.VERIFIED):
    return m1.MissionDecision(state,action,"T1",10.0,"HOROS_LOCAL",metric,"SHADOW_NON_AUTHORITATIVE",False,"test",(("m1","TEST"),))

class N1Tests(unittest.TestCase):
    def test_01_valid_matching_horos_metric_state(self):
        r=adapt(); self.assertTrue(r.usable_for_active_track); d=r.as_dict(); self.assertEqual(d["carrier_xyz_m"],(0.0,0.0,0.0)); self.assertEqual(d["target_xyz_m"],(10.0,5.0,2.0))
    def test_02_target_id_mismatch(self): self.assertEqual(adapt(src(target_ref="OTHER")).reason,"target_identity_mismatch")
    def test_03_stale_horos_evidence(self):
        r=build_m2_navigation_evidence(src(timestamp=9.0),"T1","HOROS_LOCAL",10.1); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"stale_horos_evidence")
    def test_04_metric_not_verified_not_promoted(self):
        r=adapt(src(metric_status=MetricStatus.NOT_VERIFIED,position_covariance_m2=None,covariance_semantics=None)); self.assertFalse(r.usable_for_active_track); self.assertEqual(r.as_dict()["metric_status"],"NOT_VERIFIED")
    def test_05_missing_required_verified_target(self):
        r=adapt(src(target_xyz_m=None)); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"verified_target_xyz_missing")
    def test_06_frame_mismatch(self):
        r=adapt(src(frame_ref="OTHER")); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"frame_mismatch")
    def test_07_covariance_uncertainty_mapping(self): self.assertAlmostEqual(adapt().as_dict()["uncertainty_m"],math.sqrt(14.0),12)
    def test_08_malformed_covariance(self):
        bad=(1.0,2.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0); r=adapt(src(position_covariance_m2=bad)); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"verified_covariance_unavailable_or_invalid")
    def test_09_provenance_preservation(self):
        r=adapt(src(provenance=(("horos","A"),("ct","T1")))); self.assertIn(("horos","A"),r.provenance); self.assertIn(("ct","T1"),r.provenance); self.assertIn(("n1","M2_NAVIGATION_EVIDENCE_ADAPTER"),r.provenance)
    def test_10_target_loss(self):
        r=adapt(src(lifecycle=Lifecycle.LOST,target_xyz_m=None,position_covariance_m2=None,covariance_semantics=None)); self.assertFalse(r.usable_for_active_track); self.assertIsNone(r.as_dict()["target_xyz_m"])
    def test_11_recovery_with_fresh_evidence(self):
        lost=adapt(src(lifecycle=Lifecycle.LOST,target_xyz_m=None,position_covariance_m2=None,covariance_semantics=None)); fresh=adapt(src(timestamp=10.05)); self.assertFalse(lost.usable_for_active_track); self.assertTrue(fresh.usable_for_active_track)
    def test_12_m1_track_valid_navigation_exact_m2_behavior(self):
        d=m2.PassiveGuidanceTranslator().evaluate(m2.GuidanceInput(md(),m2nav(adapt()),10.1)); self.assertEqual(d.state,m2.GuidanceState.AVAILABLE); self.assertEqual(d.intent,m2.GuidanceIntent.MAINTAIN_OBSERVATION); self.assertEqual(d.reason,"verified_geometry_observation_guidance")
    def test_13_m2_output_exact_m3_behavior(self):
        gd=m2.PassiveGuidanceTranslator().evaluate(m2.GuidanceInput(md(),m2nav(adapt()),10.1)); cmd=m3.PassiveHighLevelCommandTranslator().translate(gd,10.1); self.assertEqual(cmd.state,m3.CommandState.SUPPRESSED); self.assertEqual(cmd.command_type,m3.CommandType.NO_COMMAND); self.assertEqual(cmd.reason,"semantic_guidance_without_explicit_movement")
    def test_14_hold_path(self):
        gd=m2.PassiveGuidanceTranslator().evaluate(m2.GuidanceInput(md(m1.MissionAction.HOLD,m1.MissionState.HOLD),None,10.1)); self.assertEqual(gd.intent,m2.GuidanceIntent.HOLD); self.assertEqual(m3.PassiveHighLevelCommandTranslator().translate(gd,10.1).command_type,m3.CommandType.HOLD)
    def test_15_abort_path(self):
        gd=m2.PassiveGuidanceTranslator().evaluate(m2.GuidanceInput(md(m1.MissionAction.ABORT,m1.MissionState.ABORT),None,10.1)); cmd=m3.PassiveHighLevelCommandTranslator().translate(gd,10.1); self.assertEqual(gd.intent,m2.GuidanceIntent.ABORT_HOLD); self.assertEqual(cmd.command_type,m3.CommandType.HOLD); self.assertTrue(cmd.abort_semantic)
    def test_16_production_authority_false(self): self.assertFalse(adapt().production_authority)
    def test_17_zero_transport_control_side_effects(self):
        s=inspect.getsource(__import__("navigation_evidence_adapter")).lower()
        for token in ("import serial","import socket","uart","lora","esp-now","esp_now","pwm","dshot","pid","mixer","esc","arm(","takeoff(","land(","motor"): self.assertNotIn(token,s)
    def test_18_carrier_position_not_target_position(self):
        d=adapt().as_dict(); self.assertNotEqual(d["carrier_xyz_m"],d["target_xyz_m"]); self.assertEqual(d["carrier_xyz_m"],(0.0,0.0,0.0))
    def test_19_carrier_origin_requires_explicit_frame_semantics(self):
        r=adapt(src(carrier_origin_is_zero=False)); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"carrier_origin_not_authoritative")
    def test_20_heading_altitude_not_invented(self):
        d=adapt().as_dict(); self.assertIsNone(d["carrier_heading_deg"]); self.assertIsNone(d["carrier_altitude_m"])
    def test_21_search_not_synthesized(self): self.assertIsNone(adapt().as_dict()["search_relative_vector_m"])
    def test_22_explicit_search_geometry_preserved_only(self):
        search=ExplicitSearchGeometry("T1",10.0,"HOROS_LOCAL",MetricStatus.VERIFIED,(2.0,0.0,0.0),(("search","AUTH"),),False); self.assertEqual(adapt(search=search).as_dict()["search_relative_vector_m"],(2.0,0.0,0.0))
    def test_23_search_frame_mismatch_fails(self):
        search=ExplicitSearchGeometry("T1",10.0,"OTHER",MetricStatus.VERIFIED,(2.0,0.0,0.0)); self.assertEqual(adapt(search=search).reason,"search_frame_mismatch")
    def test_24_direct_malformed_source_object_fails(self):
        r=build_m2_navigation_evidence(object(),"T1","HOROS_LOCAL",10.1); self.assertIsNone(r.m2_kwargs); self.assertFalse(r.usable_for_active_track)
    def test_25_verified_missing_covariance_fails_closed(self): self.assertIsNone(adapt(src(position_covariance_m2=None,covariance_semantics=None)).m2_kwargs)
    def test_26_uncertainty_above_m2_threshold_degrades(self):
        s=src(position_covariance_m2=(9.0,0.0,0.0,0.0,9.0,0.0,0.0,0.0,9.0)); d=m2.PassiveGuidanceTranslator().evaluate(m2.GuidanceInput(md(),m2nav(adapt(s)),10.1)); self.assertEqual(d.state,m2.GuidanceState.DEGRADED); self.assertEqual(d.reason,"uncertainty_above_shadow_threshold")
    def test_27_deterministic_repeated_mapping(self): self.assertEqual(adapt(),adapt())
    def test_28_malformed_source_provenance_fails_closed(self):
        class Forged: provenance=1
        r=build_m2_navigation_evidence(Forged(),"T1","HOROS_LOCAL",10.1); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"horos_source_required")
    def test_29_malformed_typed_source_provenance_fails_closed(self):
        r=adapt(src(provenance=(("ok","x"),("bad",1)))); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"source_provenance_invalid")
    def test_30_invalid_or_loose_freshness_policy_fails_closed(self):
        for value in (float("nan"),0.6,-0.1):
            r=build_m2_navigation_evidence(src(),"T1","HOROS_LOCAL",10.1,policy=NavigationAdapterPolicy(value)); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"invalid_freshness_policy")
    def test_31_malformed_search_provenance_fails_closed(self):
        search=ExplicitSearchGeometry("T1",10.0,"HOROS_LOCAL",MetricStatus.VERIFIED,(1.0,0.0,0.0),(("bad",1),),False); r=adapt(search=search); self.assertIsNone(r.m2_kwargs); self.assertEqual(r.reason,"search_provenance_invalid")

if __name__=="__main__": unittest.main()
