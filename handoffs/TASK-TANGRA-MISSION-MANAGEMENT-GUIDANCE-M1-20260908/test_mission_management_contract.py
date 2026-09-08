import unittest, math, inspect
from mission_management_contract import *
def base(**kw):
 d=dict(mission_active=True,operator_intent=OperatorIntent.TRACK,target_ref='T1',timestamp=1.0,frame_ref='F1',lifecycle=Lifecycle.ESTIMATED,xyz=(1.,2.,3.),vxyz=(0.,0.,0.),covariance=(1.,1.,1.),metric_status=MetricStatus.NOT_VERIFIED,target_class='SYN',observation_age_s=.1,provenance=(('source','TEST'),),system_ready=True,safety_available=True); d.update(kw); return MissionInput(**d)
class T(unittest.TestCase):
 def test_no_mission(self): self.assertEqual(MissionManager().decide(base(mission_active=False)).state,MissionState.IDLE)
 def test_observed(self): self.assertEqual(MissionManager().decide(base(lifecycle=Lifecycle.OBSERVED)).state,MissionState.OBSERVE)
 def test_tracked(self): self.assertEqual(MissionManager().decide(base()).state,MissionState.TRACK)
 def test_degraded(self): self.assertEqual(MissionManager().decide(base(metric_status=MetricStatus.UNUSABLE)).state,MissionState.DEGRADED)
 def test_temporary_degrade(self):
  m=MissionManager(); m.decide(base()); self.assertEqual(m.decide(base(timestamp=1.1,lifecycle=Lifecycle.DEGRADED)).action,MissionAction.OBSERVE_TARGET)
 def test_stale(self): self.assertEqual(MissionManager().decide(base(observation_age_s=9)).state,MissionState.HOLD)
 def test_lost(self): self.assertEqual(MissionManager().decide(base(lifecycle=Lifecycle.LOST)).state,MissionState.TARGET_LOST)
 def test_identity(self):
  m=MissionManager(); m.decide(base()); self.assertEqual(m.decide(base(target_ref='T2',timestamp=1.1)).reason,'target_identity_changed')
 def test_bad_xyz(self): self.assertEqual(MissionManager().decide(base(xyz=(math.nan,2,3))).state,MissionState.HOLD)
 def test_bad_cov(self): self.assertEqual(MissionManager().decide(base(covariance=(1,math.inf,1))).state,MissionState.HOLD)
 def test_missing_pose(self): self.assertFalse(MissionManager().decide(base()).world_guidance_context_available)
 def test_unavailable_readiness(self): self.assertEqual(MissionManager().decide(base(system_ready=None)).state,MissionState.HOLD)
 def test_hold(self): self.assertEqual(MissionManager().decide(base(operator_intent=OperatorIntent.HOLD)).action,MissionAction.HOLD)
 def test_abort(self): self.assertEqual(MissionManager().decide(base(operator_intent=OperatorIntent.ABORT)).state,MissionState.ABORT)
 def test_complete(self): self.assertEqual(MissionManager().decide(base(operator_intent=OperatorIntent.COMPLETE)).state,MissionState.MISSION_COMPLETE)
 def test_not_verified(self): self.assertEqual(MissionManager().decide(base()).metric_status,MetricStatus.NOT_VERIFIED)
 def test_timestamp_regression(self):
  m=MissionManager(); m.decide(base(timestamp=2)); self.assertEqual(m.decide(base(timestamp=1)).reason,'timestamp_regression')
 def test_determinism(self): self.assertEqual(MissionManager().decide(base()),MissionManager().decide(base()))
 def test_valid_pose(self): self.assertTrue(MissionManager().decide(base(carrier_pose=CarrierPose((0.,0.,10.),1.0,'LOCAL'))).world_guidance_context_available)
 def test_no_control_side_effects(self):
  s=inspect.getsource(__import__('mission_management_contract')).lower()
  for forbidden in ('import serial','import uart','import lora','import esp_now','import dshot','import pwm','import esc','import socket'): self.assertNotIn(forbidden,s)
 def test_unavailable_vs_negative(self): self.assertEqual(MissionManager().decide(base(observation_age_s=None)).reason,'stale_or_unknown_observation')
 def test_persistent_degrade(self):
  m=MissionManager(); m.decide(base()); m.decide(base(timestamp=1.1,lifecycle=Lifecycle.DEGRADED)); m.decide(base(timestamp=1.2,lifecycle=Lifecycle.DEGRADED)); self.assertEqual(m.decide(base(timestamp=1.3,lifecycle=Lifecycle.DEGRADED)).action,MissionAction.REACQUIRE)
if __name__=='__main__': unittest.main()
