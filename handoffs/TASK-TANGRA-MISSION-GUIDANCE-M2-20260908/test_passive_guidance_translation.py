import unittest, math, inspect, importlib.util
from pathlib import Path
M1_PATH=Path(__file__).resolve().parents[2]/'handoffs/TASK-TANGRA-MISSION-MANAGEMENT-GUIDANCE-M1-20260908/mission_management_contract.py'
spec=importlib.util.spec_from_file_location('m1_frozen',M1_PATH); m1=importlib.util.module_from_spec(spec); spec.loader.exec_module(m1)
MissionDecision=m1.MissionDecision; MissionState=m1.MissionState; MissionAction=m1.MissionAction; M1Metric=m1.MetricStatus
from passive_guidance_translation import *
def md(action=MissionAction.MAINTAIN_TRACK,state=MissionState.TRACK,metric=M1Metric.VERIFIED,target='T1',ts=10.0,frame='F1'):
 return MissionDecision(state,action,target,ts,frame,metric,'SHADOW_NON_AUTHORITATIVE',False,'test',(('m1','TEST'),))
def nav(**kw):
 d=dict(target_ref='T1',timestamp=10.0,frame_ref='F1',lifecycle=Lifecycle.ESTIMATED,metric_status=MetricStatus.VERIFIED,observation_age_s=.1,uncertainty_m=1.0,target_xyz_m=(10.,5.,2.),carrier_xyz_m=(0.,0.,1.),carrier_heading_deg=90.,carrier_altitude_m=1.,search_relative_vector_m=None,provenance=(('nav','TEST'),)); d.update(kw); return NavigationEvidence(**d)
def ev(m=None,n=None,now=10.1,c=GuidanceContext()): return PassiveGuidanceTranslator().evaluate(GuidanceInput(m or md(),n,now),c)
class T(unittest.TestCase):
 def test_01_no_action(self): self.assertEqual(ev(md(MissionAction.NO_ACTION,MissionState.IDLE)).intent,GuidanceIntent.NO_GUIDANCE)
 def test_02_hold(self): self.assertEqual(ev(md(MissionAction.HOLD,MissionState.HOLD)).intent,GuidanceIntent.HOLD)
 def test_03_abort(self): self.assertEqual(ev(md(MissionAction.ABORT,MissionState.ABORT)).intent,GuidanceIntent.ABORT_HOLD)
 def test_04_complete(self): self.assertEqual(ev(md(MissionAction.MISSION_COMPLETE,MissionState.MISSION_COMPLETE)).intent,GuidanceIntent.HOLD)
 def test_05_observe_valid(self): self.assertEqual(ev(md(MissionAction.OBSERVE_TARGET,MissionState.OBSERVE),nav()).state,GuidanceState.AVAILABLE)
 def test_06_observe_no_geometry(self): self.assertEqual(ev(md(MissionAction.OBSERVE_TARGET,MissionState.OBSERVE),nav(target_xyz_m=None)).intent,GuidanceIntent.NO_GUIDANCE)
 def test_07_track_valid(self): self.assertEqual(ev(md(),nav()).intent,GuidanceIntent.MAINTAIN_OBSERVATION)
 def test_08_degraded_metric(self): self.assertEqual(ev(md(metric=M1Metric.UNUSABLE),nav(metric_status=MetricStatus.UNUSABLE)).intent,GuidanceIntent.HOLD)
 def test_09_not_verified(self):
  d=ev(md(metric=M1Metric.NOT_VERIFIED),nav(metric_status=MetricStatus.NOT_VERIFIED)); self.assertEqual(d.state,GuidanceState.DEGRADED); self.assertIsNone(d.relative_vector_m)
 def test_10_reacquire_sufficient(self):
  d=ev(md(MissionAction.REACQUIRE,MissionState.TARGET_LOST),nav(lifecycle=Lifecycle.DEGRADED,search_relative_vector_m=(2.,0.,0.))); self.assertEqual(d.intent,GuidanceIntent.REACQUIRE_TARGET); self.assertEqual(d.relative_vector_m,(2.,0.,0.))
 def test_11_reacquire_without_search(self): self.assertEqual(ev(md(MissionAction.REACQUIRE,MissionState.TARGET_LOST),nav()).reason,'reacquire_without_search_geometry')
 def test_12_missing_carrier_pose(self):
  d=ev(md(),nav(carrier_xyz_m=None)); self.assertEqual(d.intent,GuidanceIntent.MAINTAIN_OBSERVATION); self.assertIsNone(d.relative_vector_m)
 def test_13_stale_input(self): self.assertEqual(ev(md(),nav(),now=11.).state,GuidanceState.SUPPRESSED)
 def test_14_bad_target_xyz(self): self.assertEqual(ev(md(),nav(target_xyz_m=(math.nan,0,0))).state,GuidanceState.SUPPRESSED)
 def test_15_bad_carrier(self): self.assertEqual(ev(md(),nav(carrier_xyz_m=(0,math.inf,0))).state,GuidanceState.SUPPRESSED)
 def test_16_identity_discontinuity(self): self.assertEqual(ev(md(),nav(),c=GuidanceContext('OLD',9.9)).reason,'target_identity_discontinuity_requires_reset')
 def test_17_timestamp_regression(self): self.assertEqual(ev(md(ts=9.0),nav(timestamp=9.0),now=9.1,c=GuidanceContext('T1',9.5)).reason,'timestamp_regression')
 def test_18_lost_lifecycle(self): self.assertEqual(ev(md(MissionAction.REACQUIRE,MissionState.TARGET_LOST),nav(lifecycle=Lifecycle.LOST)).intent,GuidanceIntent.REACQUIRE_TARGET)
 def test_19_determinism(self): self.assertEqual(ev(md(),nav()),ev(md(),nav()))
 def test_20_uncertainty(self): self.assertEqual(ev(md(),nav(uncertainty_m=20.)).state,GuidanceState.DEGRADED)
 def test_21_no_control_side_effects(self):
  s=inspect.getsource(__import__('passive_guidance_translation')).lower()
  for x in ('import serial','import socket','uart','lora','esp-now','esp_now','pwm','dshot','pid','mixer','esc output','arm(','takeoff(','land('): self.assertNotIn(x,s)
 def test_22_no_fabricated_movement_coordinates(self):
  for n in (None,nav(target_xyz_m=None),nav(carrier_xyz_m=None),nav(target_xyz_m=(math.nan,0,0))):
   d=ev(md(),n); self.assertNotIn(d.intent,(GuidanceIntent.MOVE_RELATIVE,GuidanceIntent.SET_ALTITUDE,GuidanceIntent.SET_HEADING)); self.assertIsNone(d.relative_vector_m); self.assertIsNone(d.altitude_m); self.assertIsNone(d.heading_deg)
 def test_23_metric_mismatch(self): self.assertEqual(ev(md(metric=M1Metric.VERIFIED),nav(metric_status=MetricStatus.NOT_VERIFIED)).state,GuidanceState.SUPPRESSED)
 def test_24_frame_mismatch(self): self.assertEqual(ev(md(),nav(frame_ref='F2')).state,GuidanceState.SUPPRESSED)
 def test_25_navigation_stale(self): self.assertEqual(ev(md(),nav(timestamp=9.),now=10.1).reason,'stale_navigation_evidence')
 def test_26_bad_heading(self): self.assertEqual(ev(md(),nav(carrier_heading_deg=math.nan)).state,GuidanceState.SUPPRESSED)
 def test_27_bad_uncertainty(self): self.assertEqual(ev(md(),nav(uncertainty_m=-1.)).state,GuidanceState.SUPPRESSED)
 def test_28_m1_authority_rejected(self):
  x=md(); x=MissionDecision(x.state,x.action,x.target_ref,x.timestamp,x.frame_ref,x.metric_status,x.confidence_authority,x.world_guidance_context_available,x.reason,x.provenance,x.version,True); self.assertEqual(ev(x,nav()).state,GuidanceState.SUPPRESSED)
if __name__=='__main__': unittest.main()
