import copy
import json
import pathlib
import unittest

from system_health_v1.engine import CANONICAL_CONCEPTS, SystemHealthV1Engine

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_fixture(name):
    with (ROOT / "fixtures" / name).open("r", encoding="utf-8") as f:
        return json.load(f)

class FakeClock:
    def __init__(self, start=100.0): self.t=start
    def __call__(self): return self.t
    def advance(self, seconds): self.t += seconds

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.telemetry=load_fixture("current_telemetry_reduced.json")
        self.pi_status=load_fixture("current_pi_status_reduced.json")
        self.clock=FakeClock()
        self.engine=SystemHealthV1Engine(monotonic=self.clock)
    def health(self, telemetry=None, pi_status=None):
        return self.engine.normalize(self.telemetry if telemetry is None else telemetry, self.pi_status if pi_status is None else pi_status)["concepts"]
    def test_exactly_12_canonical_concepts(self):
        c=self.health(); self.assertEqual(tuple(c.keys()),CANONICAL_CONCEPTS); self.assertEqual(len(c),12)
    def test_current_fixture_expected_non_false_green_states(self):
        c=self.health()
        expected={"RUNTIME_HEALTH":"NOMINAL","SYSTEM_CPU":"NOT_VERIFIED","SYSTEM_RAM":"NOT_VERIFIED","CPU_TEMPERATURE":"NOT_VERIFIED","RUNTIME_PERFORMANCE":"NOT_VERIFIED","HQ_CAMERA_HEALTH":"NOMINAL","WIDE_PIPELINE_HEALTH":"NOMINAL","HAILO_HEALTH":"NOMINAL","CA_AUTHORITY_STATE":"NOT_VERIFIED","METRIC_HEALTH":"NOT_VERIFIED","HOROS_HEALTH":"DEGRADED","TELEMETRY_EDGE_HEALTH":"NOMINAL"}
        for k,v in expected.items(): self.assertEqual(c[k]["state"],v)
    def test_missing_payload_is_unavailable_not_nominal(self):
        c=self.engine.normalize({}, {})["concepts"]
        for k in CANONICAL_CONCEPTS:
            self.assertIn(c[k]["state"],{"UNAVAILABLE","NOT_VERIFIED"}); self.assertNotEqual(c[k]["state"],"NOMINAL")
    def test_wide_source_native_stale_bound(self):
        t=copy.deepcopy(self.telemetry); w=t["horos_shadow"]["wide_worker"]; w["last_age_s"]=0.51; w["last_fresh"]=False
        c=self.health(t)["WIDE_PIPELINE_HEALTH"]; self.assertEqual(c["state"],"STALE"); self.assertEqual(c["freshness"]["threshold_s"],0.5); self.assertIn("WIDE_STALE",c["reason_codes"])
    def test_wide_worker_not_running_is_fault(self):
        t=copy.deepcopy(self.telemetry); t["horos_shadow"]["wide_worker"]["running"]=False
        self.assertEqual(self.health(t)["WIDE_PIPELINE_HEALTH"]["state"],"FAULT")
    def test_numeric_resource_values_never_self_green(self):
        t=copy.deepcopy(self.telemetry); t["cpu_usage"]=0.1; t["ram_usage"]=0.1; t["cpu_temp"]=1.0; c=self.health(t)
        self.assertEqual(c["SYSTEM_CPU"]["state"],"NOT_VERIFIED"); self.assertEqual(c["SYSTEM_RAM"]["state"],"NOT_VERIFIED"); self.assertEqual(c["CPU_TEMPERATURE"]["state"],"NOT_VERIFIED")
    def test_performance_has_no_invented_threshold(self):
        t=copy.deepcopy(self.telemetry); t["fps"]=0.01; c=self.health(t)["RUNTIME_PERFORMANCE"]
        self.assertEqual(c["state"],"NOT_VERIFIED"); self.assertIn("PERFORMANCE_THRESHOLD_NOT_DEFINED",c["reason_codes"])
    def test_hq_camera_open_does_not_claim_frame_freshness(self):
        c=self.health()["HQ_CAMERA_HEALTH"]; self.assertEqual(c["state"],"NOMINAL"); self.assertEqual(c["freshness"]["state"],"UNKNOWN"); self.assertIn("HQ_FRAME_FRESHNESS",c["not_verified"])
    def test_hailo_observation_age_is_diagnostic_only(self):
        self.health(); self.clock.advance(9999); t=copy.deepcopy(self.telemetry); del t["detector_timing"]; c=self.health(t)["HAILO_HEALTH"]
        self.assertEqual(c["state"],"NOMINAL"); self.assertGreater(c["freshness"]["age_s"],9000); self.assertIsNone(c["freshness"]["threshold_s"])
    def test_ca_match_is_not_liveness_green(self):
        c=self.health()["CA_AUTHORITY_STATE"]; self.assertEqual(c["state"],"NOT_VERIFIED"); self.assertIn("CA_LIVENESS_NOT_VERIFIED",c["reason_codes"])
    def test_metric_non_authoritative_is_not_auto_fault_or_green(self):
        c=self.health()["METRIC_HEALTH"]; self.assertEqual(c["state"],"NOT_VERIFIED"); self.assertIn("METRIC_NON_AUTHORITATIVE",c["reason_codes"]); self.assertIn("METRIC_EXPECTATION_NOT_DEFINED",c["reason_codes"])
    def test_horos_age_without_threshold_never_creates_stale(self):
        t=copy.deepcopy(self.telemetry); t["horos_shadow"]["degraded_reasons"]=[]; t["server_time"]=999999.0; t["horos_shadow"]["timestamp"]=1.0; c=self.health(t)["HOROS_HEALTH"]
        self.assertEqual(c["state"],"NOT_VERIFIED"); self.assertEqual(c["freshness"]["state"],"UNKNOWN"); self.assertIsNone(c["freshness"]["threshold_s"])
    def test_telemetry_optional_remote_ingest_offline_does_not_override_direct_pi_live(self):
        c=self.health()["TELEMETRY_EDGE_HEALTH"]; self.assertEqual(c["state"],"NOMINAL"); self.assertEqual(c["values"]["remote_ingest_status"],"OFFLINE")
    def test_telemetry_primary_offline_is_fault(self):
        t=copy.deepcopy(self.telemetry); t["pi_http_status"]="OFFLINE"; c=self.health(t)["TELEMETRY_EDGE_HEALTH"]
        self.assertEqual(c["state"],"FAULT"); self.assertIn("TELEMETRY_DISCONNECTED",c["reason_codes"])
    def test_reason_provenance_and_contract_shape(self):
        c=self.health(); req={"concept","state","reason_codes","values","freshness","provenance","not_verified"}
        for k in CANONICAL_CONCEPTS:
            self.assertEqual(set(c[k]),req); self.assertTrue(c[k]["provenance"]); self.assertIn(c[k]["freshness"]["basis"],{"SOURCE_NATIVE","PC_DERIVED","CURRENT_POLL","NONE"})

if __name__ == "__main__": unittest.main()
