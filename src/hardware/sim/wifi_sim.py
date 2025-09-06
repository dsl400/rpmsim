"""
WiFi Hardware Simulation Module
Simulates WiFi hardware behavior for development and testing
"""

import utime as time
import urandom as random

class WiFiSimulator:
    """Simulates WiFi hardware for development"""
    
    def __init__(self):
        self.is_initialized = False
        self.is_connected = False
        self.current_network = None
        self.connection_strength = 0
        self.scan_results = []
        
        # Mock network database
        self.available_networks = [
            {"ssid": "HomeNetwork", "signal": -45, "security": "WPA2", "channel": 6},
            {"ssid": "OfficeWiFi", "signal": -67, "security": "WPA2", "channel": 11},
            {"ssid": "GuestNetwork", "signal": -78, "security": "Open", "channel": 1},
            {"ssid": "MobileHotspot", "signal": -82, "security": "WPA2", "channel": 3},
            {"ssid": "TestNetwork", "signal": -55, "security": "WPA2", "channel": 9},
        ]
    
    def initialize(self):
        """Initialize WiFi hardware simulation"""
        print("[WiFi SIM] Initializing WiFi hardware simulation...")
        time.sleep_ms(100)  # Simulate initialization delay
        self.is_initialized = True
        print("[WiFi SIM] WiFi hardware simulation initialized")
        return True
    
    def scan_networks(self):
        """Simulate network scanning"""
        if not self.is_initialized:
            raise RuntimeError("WiFi not initialized")
        
        print("[WiFi SIM] Scanning for networks...")
        time.sleep_ms(500)  # Simulate scan delay
        
        # Simulate varying signal strengths
        self.scan_results = []
        for network in self.available_networks:
            # Add some randomness to signal strength
            signal_variation = random.randint(-10, 10)
            simulated_network = network.copy()
            simulated_network["signal"] = max(-100, min(-20, network["signal"] + signal_variation))
            self.scan_results.append(simulated_network)
        
        print(f"[WiFi SIM] Found {len(self.scan_results)} networks")
        return self.scan_results
    
    def connect(self, ssid, password=None):
        """Simulate connecting to a network"""
        if not self.is_initialized:
            raise RuntimeError("WiFi not initialized")
        
        print(f"[WiFi SIM] Connecting to {ssid}...")
        
        # Find network in scan results
        target_network = None
        for network in self.scan_results:
            if network["ssid"] == ssid:
                target_network = network
                break
        
        if not target_network:
            print(f"[WiFi SIM] Network {ssid} not found")
            return False
        
        # Simulate connection process
        time.sleep_ms(1000)  # Simulate connection delay
        
        # Simulate connection success/failure based on signal strength
        success_probability = max(0.3, min(0.95, (100 + target_network["signal"]) / 100))
        connection_successful = random.random() < success_probability
        
        if connection_successful:
            self.is_connected = True
            self.current_network = target_network
            self.connection_strength = target_network["signal"]
            print(f"[WiFi SIM] Connected to {ssid}")
            return True
        else:
            print(f"[WiFi SIM] Failed to connect to {ssid}")
            return False
    
    def disconnect(self):
        """Simulate disconnecting from network"""
        if self.is_connected:
            print(f"[WiFi SIM] Disconnecting from {self.current_network['ssid']}")
            self.is_connected = False
            self.current_network = None
            self.connection_strength = 0
        return True
    
    def get_status(self):
        """Get current WiFi status"""
        return {
            "initialized": self.is_initialized,
            "connected": self.is_connected,
            "network": self.current_network,
            "signal_strength": self.connection_strength
        }
    
    def get_ip_info(self):
        """Get IP configuration (simulated)"""
        if not self.is_connected:
            return None
        
        return {
            "ip": "192.168.1.100",
            "subnet": "255.255.255.0",
            "gateway": "192.168.1.1",
            "dns": "8.8.8.8"
        }
    
    def check_firmware_update(self):
        """Simulate firmware update check"""
        print("[WiFi SIM] Checking for firmware updates...")
        time.sleep_ms(300)
        
        # Simulate random update availability
        update_available = random.random() < 0.2  # 20% chance
        
        if update_available:
            return {
                "available": True,
                "version": "1.2.3",
                "size": "2.4 MB",
                "description": "Bug fixes and performance improvements"
            }
        else:
            return {"available": False}
    
    def reset(self):
        """Reset WiFi hardware simulation"""
        print("[WiFi SIM] Resetting WiFi hardware...")
        self.disconnect()
        self.is_initialized = False
        time.sleep_ms(200)
        return True
