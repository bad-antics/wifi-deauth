#!/usr/bin/env python3
"""WiFi Deauth - Basic Usage (requires root + monitor mode)"""
from wifi_deauth.config import DeauthConfig
from wifi_deauth.core import DeauthEngine
from wifi_deauth.scanner import WiFiScanner

# Scan networks first
networks = WiFiScanner.scan_networks()
for net in networks:
    print(f"  {net.get('essid','?'):30s}  {net.get('bssid','')}  Ch:{net.get('channel',0)}")
