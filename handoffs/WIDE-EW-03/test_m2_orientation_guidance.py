import unittest
from dataclasses import replace
from m2_orientation_guidance import M1OrientationRequest, build_m2_orientation_guidance


def request(**changes):
    base = M1OrientationRequest(
        state="ACQUIRE",
        action="ORIENT_REQUEST_PENDING",
        cue_id=7,
        source="WIDE_IMX708",
        provenance="WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC",
        timestamp_monotonic_s=10.0,
        expires_at_s=10.5,
        image_x_norm=0.2,
        image_y_norm=0.5,
        horizontal_offset_norm=-0.6,
        sector="LEFT",
        quality=0.8,
        persistence_frames=2,
        mission_authority_valid=True,
    )
    return replace(base, **changes)


class M2OrientationGuidanceTests(unittest.TestCase):
    def test_valid_left_orient(self):
        g = build_m2_orientation_guidance(request(), 10.2)
        self.assertEqual((g.status, g.guidance_type, g.sector), ("AVAILABLE", "ORIENT_OBSERVATION_AXIS", "LEFT"))

    def test_valid_center_orient(self):
        g = build_m2_orientation_guidance(request(image_x_norm=0.5, horizontal_offset_norm=0.0, sector="CENTER"), 10.2)
        self.assertEqual((g.status, g.guidance_type, g.sector), ("AVAILABLE", "ORIENT_OBSERVATION_AXIS", "CENTER"))

    def test_valid_right_orient(self):
        g = build_m2_orientation_guidance(request(image_x_norm=0.8, horizontal_offset_norm=0.6, sector="RIGHT"), 10.2)
        self.assertEqual((g.status, g.guidance_type, g.sector), ("AVAILABLE", "ORIENT_OBSERVATION_AXIS", "RIGHT"))

    def test_stale_acquisition(self):
        g = build_m2_orientation_guidance(request(), 10.6)
        self.assertEqual((g.status, g.reason), ("SUPPRESSED", "STALE_ACQUISITION"))

    def test_malformed_direction(self):
        g = build_m2_orientation_guidance(request(horizontal_offset_norm=0.1), 10.2)
        self.assertEqual((g.status, g.reason), ("SUPPRESSED", "MALFORMED_DIRECTION"))

    def test_invalid_provenance(self):
        g = build_m2_orientation_guidance(request(provenance="INVALID"), 10.2)
        self.assertEqual((g.status, g.reason), ("SUPPRESSED", "INVALID_PROVENANCE"))

    def test_mission_authority_lost(self):
        g = build_m2_orientation_guidance(request(mission_authority_valid=False), 10.2)
        self.assertEqual((g.status, g.reason), ("SUPPRESSED", "MISSION_AUTHORITY_LOST"))

    def test_hq_authority_preempts(self):
        g = build_m2_orientation_guidance(request(), 10.2, hq_authoritative_target_active=True)
        self.assertEqual((g.status, g.guidance_type, g.reason), ("SUPPRESSED", "NO_GUIDANCE", "HQ_AUTHORITY_ACTIVE"))

    def test_acquisition_cancelled(self):
        g = build_m2_orientation_guidance(request(state="SEARCH", action="NO_ACTION"), 10.2)
        self.assertEqual((g.status, g.reason), ("SUPPRESSED", "ACQUISITION_NOT_PENDING"))

    def test_timeout_clears_guidance(self):
        first = build_m2_orientation_guidance(request(), 10.2)
        second = build_m2_orientation_guidance(request(), 10.6)
        self.assertEqual(first.guidance_type, "ORIENT_OBSERVATION_AXIS")
        self.assertEqual((second.status, second.guidance_type), ("SUPPRESSED", "NO_GUIDANCE"))

    def test_no_m3_or_metric_fields(self):
        g = build_m2_orientation_guidance(request(), 10.2)
        fields = vars(g)
        for forbidden in ("m3", "command", "yaw", "yaw_rate", "heading", "bearing", "range", "xyz", "target_id", "track_id"):
            self.assertNotIn(forbidden, fields)


if __name__ == "__main__":
    unittest.main()
