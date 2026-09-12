import unittest
from dataclasses import dataclass, replace
from wide_acquisition_bridge import (
    MC1AuthorityContext,
    HQAuthorityState,
    M1AcquisitionStateMachine,
    validate_wide_acquisition_cue,
)


@dataclass(frozen=True)
class Cue:
    schema_version: int = 1
    cue_id: int = 1
    source: str = "WIDE_IMX708"
    timestamp_monotonic_s: float = 10.0
    max_age_s: float = 0.5
    image_x_norm: float = 0.2
    image_y_norm: float = 0.5
    horizontal_offset_norm: float = -0.6
    sector: str = "LEFT"
    motion_area_norm: float = 0.02
    quality: float = 0.8
    persistence_frames: int = 2
    provenance: str = "WIDE_STABLE_BACKGROUND_DIFFERENCE_NON_METRIC"


GOOD = MC1AuthorityContext(True, True, True, True)
NO_HQ = HQAuthorityState(False)


def accepted(cue, now=10.2, authority=GOOD, hq=NO_HQ):
    return validate_wide_acquisition_cue(cue, now, authority, hq)


class BridgeTests(unittest.TestCase):
    def test_valid_left_cue(self):
        r = accepted(Cue())
        self.assertTrue(r.accepted)
        self.assertEqual(r.acquisition.sector, "LEFT")

    def test_valid_center_cue(self):
        r = accepted(replace(Cue(), image_x_norm=0.5, horizontal_offset_norm=0.0, sector="CENTER"))
        self.assertTrue(r.accepted)
        self.assertEqual(r.acquisition.sector, "CENTER")

    def test_valid_right_cue(self):
        r = accepted(replace(Cue(), image_x_norm=0.8, horizontal_offset_norm=0.6, sector="RIGHT"))
        self.assertTrue(r.accepted)
        self.assertEqual(r.acquisition.sector, "RIGHT")

    def test_stale_cue(self):
        r = accepted(Cue(), now=10.6)
        self.assertFalse(r.accepted)
        self.assertEqual(r.reason, "STALE_CUE")

    def test_low_quality_cue(self):
        r = accepted(replace(Cue(), quality=0.59))
        self.assertFalse(r.accepted)
        self.assertEqual(r.reason, "LOW_QUALITY")

    def test_low_persistence_cue(self):
        r = accepted(replace(Cue(), persistence_frames=1))
        self.assertFalse(r.accepted)
        self.assertEqual(r.reason, "LOW_PERSISTENCE")

    def test_malformed_cue(self):
        r = accepted(replace(Cue(), image_x_norm=1.2))
        self.assertFalse(r.accepted)
        self.assertEqual(r.reason, "MALFORMED_CUE")

    def test_mission_inactive(self):
        bad = MC1AuthorityContext(False, True, True, True)
        r = accepted(Cue(), authority=bad)
        self.assertFalse(r.accepted)
        self.assertEqual(r.reason, "MISSION_NOT_PERMITTED")

    def test_hq_already_authoritative(self):
        r = accepted(Cue(), hq=HQAuthorityState(True))
        self.assertFalse(r.accepted)
        self.assertEqual(r.reason, "HQ_AUTHORITY_ACTIVE")

    def test_cue_timeout(self):
        r = accepted(Cue())
        sm = M1AcquisitionStateMachine()
        d1 = sm.step(10.2, r.acquisition)
        self.assertEqual((d1.state, d1.action), ("ACQUIRE", "ORIENT_REQUEST_PENDING"))
        d2 = sm.step(10.6)
        self.assertEqual((d2.state, d2.reason), ("SEARCH", "CUE_TIMEOUT"))

    def test_return_to_search(self):
        r = accepted(Cue())
        sm = M1AcquisitionStateMachine()
        sm.step(10.2, r.acquisition)
        sm.step(10.6)
        d = sm.step(10.7)
        self.assertEqual((d.state, d.action), ("SEARCH", "NO_ACTION"))

    def test_hq_authority_preempts_pending_wide(self):
        r = accepted(Cue())
        sm = M1AcquisitionStateMachine()
        sm.step(10.2, r.acquisition)
        d = sm.step(10.3, hq_authoritative_target_active=True)
        self.assertEqual((d.state, d.action), ("AUTHORITATIVE_TRACK", "NO_WIDE_OVERRIDE"))
        self.assertIsNone(d.cue_id)

    def test_no_metric_fields_created(self):
        r = accepted(Cue())
        fields = vars(r.acquisition)
        for forbidden in ("bearing", "bearing_deg", "range", "range_m", "xyz", "target_id", "track_id"):
            self.assertNotIn(forbidden, fields)


if __name__ == "__main__":
    unittest.main()
