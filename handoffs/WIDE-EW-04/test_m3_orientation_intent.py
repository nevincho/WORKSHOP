import unittest
from dataclasses import replace
from m3_orientation_intent import M2OrientationGuidance, build_m3_orientation_intent


def valid_guidance(**kwargs):
    base = M2OrientationGuidance(
        status="AVAILABLE",
        guidance_type="ORIENT_OBSERVATION_AXIS",
        cue_id=7,
        source="WIDE_IMX708",
        provenance="WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC",
        timestamp_monotonic_s=10.0,
        expires_at_s=10.5,
        image_x_norm=0.2,
        image_y_norm=0.5,
        horizontal_offset_norm=-0.6,
        sector="LEFT",
        mission_authority_valid=True,
    )
    return replace(base, **kwargs)


class M3IntentTests(unittest.TestCase):
    def test_valid_left_intent(self):
        r = build_m3_orientation_intent(valid_guidance(), 10.2)
        self.assertEqual((r.status, r.intent_type, r.sector), ("VALID", "ORIENT_OBSERVATION_AXIS", "LEFT"))

    def test_valid_center_intent(self):
        g = valid_guidance(image_x_norm=0.5, horizontal_offset_norm=0.0, sector="CENTER")
        r = build_m3_orientation_intent(g, 10.2)
        self.assertEqual((r.status, r.sector), ("VALID", "CENTER"))

    def test_valid_right_intent(self):
        g = valid_guidance(image_x_norm=0.8, horizontal_offset_norm=0.6, sector="RIGHT")
        r = build_m3_orientation_intent(g, 10.2)
        self.assertEqual((r.status, r.sector), ("VALID", "RIGHT"))

    def test_stale_guidance(self):
        r = build_m3_orientation_intent(valid_guidance(), 10.6)
        self.assertEqual((r.status, r.reason), ("SUPPRESSED", "STALE_GUIDANCE"))

    def test_malformed_direction(self):
        g = valid_guidance(image_x_norm=0.9, horizontal_offset_norm=-0.6)
        r = build_m3_orientation_intent(g, 10.2)
        self.assertEqual((r.status, r.reason), ("SUPPRESSED", "MALFORMED_DIRECTION"))

    def test_invalid_provenance(self):
        r = build_m3_orientation_intent(valid_guidance(provenance="OTHER"), 10.2)
        self.assertEqual((r.status, r.reason), ("SUPPRESSED", "INVALID_PROVENANCE"))

    def test_mission_authority_lost(self):
        r = build_m3_orientation_intent(valid_guidance(mission_authority_valid=False), 10.2)
        self.assertEqual((r.status, r.reason), ("SUPPRESSED", "MISSION_AUTHORITY_LOST"))

    def test_hq_authority_preempts(self):
        r = build_m3_orientation_intent(valid_guidance(), 10.2, hq_authoritative_target_active=True)
        self.assertEqual((r.status, r.reason, r.intent_type), ("SUPPRESSED", "HQ_AUTHORITY_ACTIVE", "NO_INTENT"))

    def test_acquisition_cancelled(self):
        r = build_m3_orientation_intent(valid_guidance(status="SUPPRESSED"), 10.2)
        self.assertEqual((r.status, r.reason), ("SUPPRESSED", "GUIDANCE_SUPPRESSED_OR_CANCELLED"))

    def test_unsupported_semantic(self):
        r = build_m3_orientation_intent(valid_guidance(guidance_type="MAINTAIN_OBSERVATION"), 10.2)
        self.assertEqual((r.status, r.reason), ("SUPPRESSED", "UNSUPPORTED_SEMANTIC"))

    def test_no_stale_intent_retention(self):
        first = build_m3_orientation_intent(valid_guidance(), 10.2)
        second = build_m3_orientation_intent(valid_guidance(), 10.6)
        self.assertEqual(first.status, "VALID")
        self.assertEqual((second.status, second.intent_type, second.cue_id), ("SUPPRESSED", "NO_INTENT", None))

    def test_no_physical_command_fields(self):
        r = build_m3_orientation_intent(valid_guidance(), 10.2)
        fields = vars(r)
        for forbidden in (
            "yaw", "yaw_deg", "yaw_rate", "heading", "heading_deg", "bearing", "bearing_deg",
            "range", "range_m", "xyz", "target_id", "track_id", "motor", "servo", "pwm", "actuator",
            "fc_command", "carrier_command", "command_send",
        ):
            self.assertNotIn(forbidden, fields)


if __name__ == "__main__":
    unittest.main()
