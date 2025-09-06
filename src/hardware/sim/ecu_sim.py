"""
ECU Hardware Simulation Module
Simulates ECU hardware behavior for development and testing
"""

import utime as time
import urandom as random
import math

class ECUSimulator:
    """Simulates ECU hardware for development"""
    
    def __init__(self):
        self.is_initialized = False
        self.simulation_active = False
        self.current_rpm = 800  # Idle RPM
        self.target_rpm = 800
        self.sensor_config = {
            "crank": {"degrees_per_tooth": 6, "missing_teeth": 2},
            "cam": {"degrees_per_tooth": 12, "tooth_pattern": [1,1,1,1,1,1,0,1,1,1,1,1]}
        }
        
        # Live data simulation
        self.live_data = {
            "RPM": 800,
            "Coolant Temp": 85,
            "Throttle Position": 0,
            "Engine Load": 15,
            "Fuel Level": 75,
            "Speed": 0,
            "Intake Air Temp": 22,
            "MAF": 2.1,
            "Fuel Pressure": 3.5,
            "Oil Pressure": 2.8,
            "Battery Voltage": 12.6,
            "Timing Advance": 10
        }
        
        # DTC simulation
        self.stored_dtcs = []
        self.pending_dtcs = []
        
        # Simulation parameters
        self.rpm_change_rate = 50  # RPM change per update
        self.update_interval = 100  # ms
        self.last_update = 0
    
    def initialize(self):
        """Initialize ECU hardware simulation"""
        print("[ECU SIM] Initializing ECU hardware simulation...")
        time.sleep_ms(200)  # Simulate initialization delay
        self.is_initialized = True
        self.last_update = time.ticks_ms()
        print("[ECU SIM] ECU hardware simulation initialized")
        return True
    
    def start_simulation(self):
        """Start ECU simulation"""
        if not self.is_initialized:
            raise RuntimeError("ECU not initialized")
        
        print("[ECU SIM] Starting ECU simulation...")
        self.simulation_active = True
        return True
    
    def stop_simulation(self):
        """Stop ECU simulation"""
        print("[ECU SIM] Stopping ECU simulation...")
        self.simulation_active = False
        self.current_rpm = 800  # Return to idle
        self.target_rpm = 800
        return True
    
    def set_target_rpm(self, rpm):
        """Set target RPM for simulation"""
        self.target_rpm = max(0, min(8000, rpm))
        print(f"[ECU SIM] Target RPM set to {self.target_rpm}")
    
    def configure_sensors(self, config):
        """Configure sensor simulation parameters"""
        if "crank" in config:
            self.sensor_config["crank"].update(config["crank"])
        if "cam" in config:
            self.sensor_config["cam"].update(config["cam"])
        
        print(f"[ECU SIM] Sensor configuration updated: {self.sensor_config}")
        return True
    
    def update_simulation(self):
        """Update simulation state (called periodically)"""
        if not self.simulation_active:
            return
        
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_update) < self.update_interval:
            return
        
        self.last_update = current_time
        
        # Update RPM towards target
        if self.current_rpm != self.target_rpm:
            rpm_diff = self.target_rpm - self.current_rpm
            if abs(rpm_diff) <= self.rpm_change_rate:
                self.current_rpm = self.target_rpm
            else:
                self.current_rpm += self.rpm_change_rate if rpm_diff > 0 else -self.rpm_change_rate
        
        # Update live data based on RPM
        self._update_live_data()
    
    def _update_live_data(self):
        """Update live data based on current simulation state"""
        rpm = self.current_rpm
        
        # RPM
        self.live_data["RPM"] = rpm
        
        # Throttle position (correlates with RPM above idle)
        if rpm > 800:
            throttle = min(100, (rpm - 800) / 70)  # Rough correlation
            # Add some noise
            throttle += random.randint(-5, 5)
            self.live_data["Throttle Position"] = max(0, min(100, throttle))
        else:
            self.live_data["Throttle Position"] = random.randint(0, 3)
        
        # Engine load
        base_load = 15 if rpm <= 800 else min(95, 15 + (rpm - 800) / 80)
        self.live_data["Engine Load"] = max(0, min(100, base_load + random.randint(-5, 5)))
        
        # Speed (rough correlation with RPM)
        if rpm > 1000:
            speed = (rpm - 1000) / 50  # Very rough gear ratio simulation
            self.live_data["Speed"] = max(0, min(200, speed + random.randint(-2, 2)))
        else:
            self.live_data["Speed"] = 0
        
        # Coolant temperature (slowly increases with load)
        target_temp = 85 + (self.live_data["Engine Load"] - 15) * 0.3
        current_temp = self.live_data["Coolant Temp"]
        temp_diff = target_temp - current_temp
        self.live_data["Coolant Temp"] = current_temp + (temp_diff * 0.1)  # Slow change
        
        # MAF (Mass Air Flow)
        base_maf = 2.1 + (rpm - 800) / 1000
        self.live_data["MAF"] = max(0, base_maf + random.randint(-20, 20) / 100)
        
        # Fuel pressure
        self.live_data["Fuel Pressure"] = 3.5 + random.randint(-10, 10) / 100
        
        # Oil pressure (decreases slightly at idle)
        if rpm < 1000:
            self.live_data["Oil Pressure"] = 1.8 + random.randint(-10, 10) / 100
        else:
            self.live_data["Oil Pressure"] = 2.8 + random.randint(-20, 20) / 100
        
        # Battery voltage
        self.live_data["Battery Voltage"] = 12.6 + random.randint(-20, 20) / 100
        
        # Timing advance
        base_timing = 10 + (rpm - 800) / 200
        self.live_data["Timing Advance"] = max(0, min(35, base_timing + random.randint(-2, 2)))
    
    def get_live_data(self):
        """Get current live data"""
        self.update_simulation()
        return self.live_data.copy()
    
    def get_current_rpm(self):
        """Get current RPM"""
        self.update_simulation()
        return self.current_rpm
    
    def generate_sensor_signal(self, sensor_type):
        """Generate sensor signal pattern"""
        if sensor_type == "crank":
            config = self.sensor_config["crank"]
            teeth_per_rev = 360 // config["degrees_per_tooth"]
            pattern = [1] * teeth_per_rev
            # Remove missing teeth
            for i in range(config["missing_teeth"]):
                pattern[-(i+1)] = 0
            return pattern
        
        elif sensor_type == "cam":
            config = self.sensor_config["cam"]
            if "tooth_pattern" in config:
                return config["tooth_pattern"]
            else:
                teeth_per_rev = 360 // config["degrees_per_tooth"]
                return [1] * teeth_per_rev
        
        return []
    
    def read_dtcs(self):
        """Read stored diagnostic trouble codes"""
        print("[ECU SIM] Reading DTCs...")
        time.sleep_ms(100)
        return {
            "stored": self.stored_dtcs.copy(),
            "pending": self.pending_dtcs.copy()
        }
    
    def clear_dtcs(self):
        """Clear diagnostic trouble codes"""
        print("[ECU SIM] Clearing DTCs...")
        time.sleep_ms(200)
        cleared_count = len(self.stored_dtcs) + len(self.pending_dtcs)
        self.stored_dtcs.clear()
        self.pending_dtcs.clear()
        return cleared_count
    
    def inject_dtc(self, code, description="Simulated DTC"):
        """Inject a DTC for testing purposes"""
        dtc = {
            "code": code,
            "description": description,
            "timestamp": time.ticks_ms()
        }
        self.stored_dtcs.append(dtc)
        print(f"[ECU SIM] Injected DTC: {code} - {description}")
    
    def get_ecu_info(self):
        """Get ECU information"""
        return {
            "part_number": "SIM-ECU-001",
            "software_version": "1.0.0-SIM",
            "hardware_version": "A.01",
            "calibration_id": "SIM_CAL_001",
            "serial_number": "SIM123456789",
            "supported_protocols": ["ISO14230", "ISO15765"]
        }
    
    def get_status(self):
        """Get ECU simulation status"""
        return {
            "initialized": self.is_initialized,
            "simulation_active": self.simulation_active,
            "current_rpm": self.current_rpm,
            "target_rpm": self.target_rpm,
            "sensor_config": self.sensor_config.copy()
        }
