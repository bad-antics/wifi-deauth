import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from wifi_deauth.config import DeauthConfig
from wifi_deauth.core import DeauthFrame, DeauthEngine
from wifi_deauth.detector import DeauthDetector

class TestConfig(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(DeauthConfig.PACKET_COUNT, 100)
        self.assertIn(7, DeauthConfig.REASON_CODES)

class TestFrame(unittest.TestCase):
    def test_build(self):
        frame = DeauthFrame.build("aa:bb:cc:dd:ee:ff", "11:22:33:44:55:66", 7)
        self.assertIsInstance(frame, bytes)
        self.assertGreater(len(frame), 10)

class TestDetector(unittest.TestCase):
    def test_detection(self):
        d = DeauthDetector(threshold=3, window=10)
        for i in range(5):
            alert = d.process_frame(0xC0, "aa:bb:cc:dd:ee:ff", "11:22:33:44:55:66")
        self.assertTrue(len(d.get_alerts()) > 0)

if __name__ == "__main__":
    unittest.main()
