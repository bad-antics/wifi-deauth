"""Monitor mode management"""
import subprocess, os

class MonitorMode:
    @staticmethod
    def enable(interface="wlan0"):
        try:
            subprocess.run(["airmon-ng", "check", "kill"], capture_output=True)
            subprocess.run(["airmon-ng", "start", interface], capture_output=True)
            mon_iface = interface + "mon"
            subprocess.run(["iwconfig", mon_iface], capture_output=True, check=True)
            print(f"[+] Monitor mode enabled: {mon_iface}")
            return mon_iface
        except Exception as e:
            print(f"[-] Failed to enable monitor mode: {e}")
            return None
    
    @staticmethod
    def disable(interface="wlan0mon"):
        try:
            subprocess.run(["airmon-ng", "stop", interface], capture_output=True)
            subprocess.run(["systemctl", "restart", "NetworkManager"], capture_output=True)
            print(f"[+] Monitor mode disabled")
        except Exception as e:
            print(f"[-] Failed: {e}")
    
    @staticmethod
    def list_interfaces():
        try:
            result = subprocess.check_output(["iwconfig"], stderr=subprocess.DEVNULL, text=True)
            interfaces = []
            for line in result.split("\n"):
                if "IEEE 802.11" in line or "Mode:" in line:
                    iface = line.split()[0] if line[0] != " " else None
                    if iface: interfaces.append(iface)
            return interfaces
        except: return []
