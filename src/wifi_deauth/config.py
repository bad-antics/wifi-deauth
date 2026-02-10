"""WiFi Deauth Config"""
class DeauthConfig:
    INTERFACE = "wlan0"
    MONITOR_INTERFACE = "wlan0mon"
    PACKET_COUNT = 100
    INTERVAL = 0.1
    BROADCAST = "ff:ff:ff:ff:ff:ff"
    REASON_CODES = {
        1: "Unspecified", 2: "Auth no longer valid", 3: "Leaving BSS",
        4: "Inactivity", 5: "AP overloaded", 6: "Class 2 from non-auth",
        7: "Class 3 from non-assoc", 8: "Disassoc - leaving BSS",
    }
    DEFAULT_REASON = 7
    CHANNEL_HOP = True
    HOP_INTERVAL = 0.5
