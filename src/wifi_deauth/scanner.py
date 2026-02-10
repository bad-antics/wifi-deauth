"""WiFi network scanner"""
import subprocess, re, json

class WiFiScanner:
    @staticmethod
    def scan_networks(interface="wlan0"):
        """Scan for nearby WiFi networks"""
        try:
            result = subprocess.check_output(["iwlist", interface, "scan"], stderr=subprocess.DEVNULL, text=True)
            networks = []
            current = {}
            for line in result.split("\n"):
                line = line.strip()
                if "Cell" in line and "Address:" in line:
                    if current: networks.append(current)
                    current = {"bssid": line.split("Address: ")[1] if "Address: " in line else ""}
                elif "ESSID:" in line:
                    m = re.search(r'ESSID:"([^"]*)"', line)
                    current["essid"] = m.group(1) if m else ""
                elif "Channel:" in line:
                    m = re.search(r"Channel:(\d+)", line)
                    current["channel"] = int(m.group(1)) if m else 0
                elif "Signal level=" in line:
                    m = re.search(r"Signal level=(-?\d+)", line)
                    current["signal"] = int(m.group(1)) if m else 0
            if current: networks.append(current)
            return networks
        except:
            return []
    
    @staticmethod
    def scan_clients(interface="wlan0mon", duration=10):
        """Passive client scanning"""
        return []  # Requires packet capture
