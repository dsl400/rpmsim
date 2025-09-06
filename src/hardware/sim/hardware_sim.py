"""
Hardware Simulation Manager
Coordinates all hardware simulation modules
"""

from .wifi_sim import WiFiSimulator
from .ecu_sim import ECUSimulator
import utime as time

class HardwareSimulator:
    """Main hardware simulation coordinator"""
    
    def __init__(self):
        self.wifi = WiFiSimulator()
        self.ecu = ECUSimulator()
        self.is_initialized = False
        
        # Simulation state
        self.simulation_mode = True
        self.debug_mode = True
    
    def initialize(self):
        """Initialize all hardware simulation modules"""
        print("[HW SIM] Initializing hardware simulation...")
        
        try:
            # Initialize WiFi simulation
            if not self.wifi.initialize():
                raise RuntimeError("WiFi simulation initialization failed")
            
            # Initialize ECU simulation
            if not self.ecu.initialize():
                raise RuntimeError("ECU simulation initialization failed")
            
            self.is_initialized = True
            print("[HW SIM] Hardware simulation initialized successfully")
            return True
            
        except Exception as e:
            print(f"[HW SIM] Hardware simulation initialization failed: {e}")
            return False
    
    def get_wifi(self):
        """Get WiFi simulator instance"""
        return self.wifi
    
    def get_ecu(self):
        """Get ECU simulator instance"""
        return self.ecu
    
    def update(self):
        """Update all simulation modules"""
        if not self.is_initialized:
            return
        
        # Update ECU simulation
        self.ecu.update_simulation()
    
    def get_system_status(self):
        """Get overall system status"""
        return {
            "simulation_mode": self.simulation_mode,
            "initialized": self.is_initialized,
            "wifi_status": self.wifi.get_status(),
            "ecu_status": self.ecu.get_status(),
            "uptime": time.ticks_ms()
        }
    
    def reset_all(self):
        """Reset all hardware simulations"""
        print("[HW SIM] Resetting all hardware simulations...")
        
        self.wifi.reset()
        self.ecu.stop_simulation()
        
        # Re-initialize
        return self.initialize()
    
    def enable_debug(self, enabled=True):
        """Enable/disable debug mode"""
        self.debug_mode = enabled
        print(f"[HW SIM] Debug mode {'enabled' if enabled else 'disabled'}")
    
    def simulate_hardware_fault(self, component, fault_type):
        """Simulate hardware faults for testing"""
        print(f"[HW SIM] Simulating {fault_type} fault in {component}")
        
        if component == "wifi":
            if fault_type == "disconnect":
                self.wifi.disconnect()
            elif fault_type == "reset":
                self.wifi.reset()
        
        elif component == "ecu":
            if fault_type == "communication_error":
                self.ecu.inject_dtc("U0001", "CAN Communication Error")
            elif fault_type == "sensor_fault":
                self.ecu.inject_dtc("P0335", "Crankshaft Position Sensor Fault")
    
    def get_simulation_info(self):
        """Get simulation environment information"""
        return {
            "simulator_version": "1.0.0",
            "supported_protocols": ["WiFi", "CAN", "OBD-II"],
            "simulation_features": [
                "WiFi Network Simulation",
                "ECU Live Data Simulation", 
                "RPM Signal Generation",
                "DTC Injection",
                "Sensor Configuration"
            ],
            "debug_mode": self.debug_mode
        }

# Global hardware simulator instance
hardware_sim = None

def get_hardware_simulator():
    """Get global hardware simulator instance"""
    global hardware_sim
    if hardware_sim is None:
        hardware_sim = HardwareSimulator()
    return hardware_sim

def initialize_hardware_simulation():
    """Initialize hardware simulation"""
    sim = get_hardware_simulator()
    return sim.initialize()
