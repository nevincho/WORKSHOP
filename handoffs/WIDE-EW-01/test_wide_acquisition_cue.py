import unittest
from wide_acquisition_cue import WideCueGenerator, cue_is_acceptable


def make_frame(width=160, height=90, rect=None, value=255):
    frame = [[0 for _ in range(width)] for _ in range(height)]
    if rect is not None:
        x0, y0, x1, y1 = rect
        for y in range(y0, y1):
            for x in range(x0, x1):
                frame[y][x] = value
    return frame


def persistent_motion(generator, rect, t0=1.0):
    x0, y0, x1, y1 = rect
    generator.process(make_frame(), t0)
    first = generator.process(make_frame(rect=rect), t0 + 0.1)
    second = generator.process(make_frame(rect=(x0 + 5, y0, x1 + 5, y1)), t0 + 0.2)
    return first, second


class WideCueTests(unittest.TestCase):
    def test_static_no_persistent_cue(self):
        g = WideCueGenerator()
        f = make_frame()
        self.assertIsNone(g.process(f, 1.0))
        self.assertIsNone(g.process(f, 1.1))
        self.assertIsNone(g.process(f, 1.2))

    def test_motion_left(self):
        g = WideCueGenerator()
        first, cue = persistent_motion(g, (10, 30, 35, 60))
        self.assertIsNone(first)
        self.assertIsNotNone(cue)
        self.assertEqual(cue.sector, "LEFT")
        self.assertLess(cue.horizontal_offset_norm, 0.0)

    def test_motion_center(self):
        g = WideCueGenerator()
        first, cue = persistent_motion(g, (65, 30, 95, 60))
        self.assertIsNone(first)
        self.assertIsNotNone(cue)
        self.assertEqual(cue.sector, "CENTER")

    def test_motion_right(self):
        g = WideCueGenerator()
        first, cue = persistent_motion(g, (120, 30, 145, 60))
        self.assertIsNone(first)
        self.assertIsNotNone(cue)
        self.assertEqual(cue.sector, "RIGHT")
        self.assertGreater(cue.horizontal_offset_norm, 0.0)

    def test_transient_noise_rejected(self):
        g = WideCueGenerator()
        g.process(make_frame(), 1.0)
        noisy = make_frame()
        noisy[10][10] = 255
        self.assertIsNone(g.process(noisy, 1.1))
        self.assertIsNone(g.process(make_frame(), 1.2))

    def test_stale_cue_rejected(self):
        g = WideCueGenerator(max_age_s=0.5)
        _, cue = persistent_motion(g, (10, 30, 35, 60), t0=1.0)
        self.assertTrue(cue_is_acceptable(cue, 1.4))
        self.assertFalse(cue_is_acceptable(cue, 2.0))

    def test_malformed_frame_fails_closed(self):
        g = WideCueGenerator()
        self.assertIsNone(g.process([[0]], 1.0))


if __name__ == "__main__":
    unittest.main()
