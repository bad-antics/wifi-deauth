"""Deauth attack detection"""
import time, json
from datetime import datetime

class DeauthDetector:
    def __init__(self, threshold=10, window=5):
        self.threshold = threshold
        self.window = window
        self.deauth_count = {}
        self.alerts = []
    
    def process_frame(self, frame_type, src_mac, dst_mac, timestamp=None):
        ts = timestamp or time.time()
        if frame_type == 0xC0:  # Deauth
            key = f"{src_mac}->{dst_mac}"
            self.deauth_count.setdefault(key, []).append(ts)
            # Clean old entries
            self.deauth_count[key] = [t for t in self.deauth_count[key] if ts - t < self.window]
            if len(self.deauth_count[key]) >= self.threshold:
                alert = {"type": "deauth_flood", "source": src_mac, "target": dst_mac,
                         "count": len(self.deauth_count[key]), "time": str(datetime.fromtimestamp(ts))}
                self.alerts.append(alert)
                return alert
        return None
    
    def get_alerts(self):
        return self.alerts
