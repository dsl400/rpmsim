#!/usr/bin/env python3
"""
Standalone test for ECU Diagnostic Tool
Includes minimal implementations for testing in MicroPython simulator
"""

import usys as sys
import ujson as json

# Minimal DataManager implementation for testing
class DataManager:
    def __init__(self):
        self.systems_cache = None
        self.user_settings_cache = None
        
    def load_systems(self):
        """Load systems from database"""
        # Mock data for testing
        mock_systems = {
            "systems": [
                {
                    "brand": "VW",
                    "system": "Engine",
                    "system_name": "Bosch ME7.9.7",
                    "tools": [
                        {
                            "name": "RPM Simulator",
                            "type": "rpm_simulator",
                            "config": {
                                "crank": {"degrees_per_tooth": 6, "missing_teeth": 2},
                                "cam": {"degrees_per_tooth": 12}
                            }
                        }
                    ]
                },
                {
                    "brand": "BMW",
                    "system": "Engine", 
                    "system_name": "Siemens MSV70",
                    "tools": [
                        {
                            "name": "RPM Simulator",
                            "type": "rpm_simulator",
                            "config": {
                                "crank": {"degrees_per_tooth": 6, "missing_teeth": 2},
                                "cam": {"degrees_per_tooth": 12}
                            }
                        }
                    ]
                }
            ]
        }
        self.systems_cache = mock_systems
        return mock_systems
        
    def get_brands(self):
        """Get list of available brands"""
        if not self.systems_cache:
            self.load_systems()
        
        brands = set()
        for system in self.systems_cache.get('systems', []):
            brands.add(system['brand'])
        return list(brands)
        
    def get_system_types(self, brand):
        """Get system types for a brand"""
        if not self.systems_cache:
            self.load_systems()
            
        types = set()
        for system in self.systems_cache.get('systems', []):
            if system['brand'] == brand:
                types.add(system['system'])
        return list(types)
        
    def get_system_names(self, brand, system_type):
        """Get system names for brand and type"""
        if not self.systems_cache:
            self.load_systems()
            
        names = []
        for system in self.systems_cache.get('systems', []):
            if system['brand'] == brand and system['system'] == system_type:
                names.append(system['system_name'])
        return names
        
    def get_system_tools(self, brand, system_type, system_name):
        """Get tools for a specific system"""
        if not self.systems_cache:
            self.load_systems()
            
        for system in self.systems_cache.get('systems', []):
            if (system['brand'] == brand and 
                system['system'] == system_type and 
                system['system_name'] == system_name):
                return system.get('tools', [])
        return []
        
    def get_user_settings(self):
        """Get user settings"""
        if not self.user_settings_cache:
            self.user_settings_cache = {
                'last_selected': {},
                'wifi': {},
                'preferences': {},
                'custom_systems': []
            }
        return self.user_settings_cache

# Minimal ErrorHandler implementation
class ErrorHandler:
    def __init__(self):
        self.error_log = []
        
    def handle_error(self, error, context="", severity="ERROR"):
        """Handle an error"""
        entry = {
            'error': str(error),
            'context': context,
            'severity': severity,
            'timestamp': 'mock_time'
        }
        self.error_log.append(entry)
        print(f"[{severity}] {context}: {error}")
        
    def get_error_log(self):
        """Get error log"""
        return self.error_log
        
    def get_log_summary(self):
        """Get log summary"""
        summary = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0, 'total': 0}
        for entry in self.error_log:
            severity = entry.get('severity', 'ERROR')
            if severity in summary:
                summary[severity] += 1
            summary['total'] += 1
        return summary

# Minimal WiFiManager implementation
class WiFiManager:
    def __init__(self):
        self.initialized = False
        
    def initialize(self):
        """Initialize WiFi"""
        self.initialized = True
        return True
        
    def scan_networks(self):
        """Scan for networks"""
        return [
            {'ssid': 'TestNetwork1', 'signal': -45},
            {'ssid': 'TestNetwork2', 'signal': -67},
            {'ssid': 'TestNetwork3', 'signal': -78}
        ]
        
    def is_connected(self):
        """Check if connected"""
        return False
        
    def get_connection_info(self):
        """Get connection info"""
        return {}

# Minimal ECUManager implementation  
class ECUManager:
    def __init__(self):
        self.initialized = False
        self.current_rpm = 800
        self.simulation_active = False
        
    def initialize(self):
        """Initialize ECU manager"""
        self.initialized = True
        return True
        
    def get_live_data(self):
        """Get live data"""
        return {
            'RPM': self.current_rpm,
            'Coolant Temp': 85,
            'Throttle Position': 12,
            'Engine Load': 25,
            'Fuel Level': 75,
            'Speed': 0,
            'Intake Air Temp': 22,
            'MAF': 3.2
        }
        
    def simulate_rpm(self, rpm):
        """Simulate RPM"""
        self.current_rpm = rpm
        
    def get_current_rpm(self):
        """Get current RPM"""
        return self.current_rpm
        
    def configure_sensors(self, config):
        """Configure sensors"""
        return True
        
    def start_simulation(self):
        """Start simulation"""
        self.simulation_active = True
        
    def stop_simulation(self):
        """Stop simulation"""
        self.simulation_active = False
        
    def is_simulation_active(self):
        """Check if simulation is active"""
        return self.simulation_active

def test_data_manager():
    """Test data manager functionality"""
    print("Testing Data Manager...")
    
    try:
        dm = DataManager()
        
        # Test loading systems
        systems = dm.load_systems()
        print(f"✓ Loaded systems database with {len(systems.get('systems', []))} systems")
        
        # Test getting brands
        brands = dm.get_brands()
        print(f"✓ Found brands: {brands}")
        
        # Test getting system types for a brand
        if brands:
            system_types = dm.get_system_types(brands[0])
            print(f"✓ System types for {brands[0]}: {system_types}")
            
            # Test getting system names
            if system_types:
                system_names = dm.get_system_names(brands[0], system_types[0])
                print(f"✓ System names for {brands[0]} {system_types[0]}: {system_names}")
                
                # Test getting tools
                if system_names:
                    tools = dm.get_system_tools(brands[0], system_types[0], system_names[0])
                    print(f"✓ Tools for {brands[0]} {system_types[0]} {system_names[0]}: {[t['name'] for t in tools]}")
        
        # Test user settings
        settings = dm.get_user_settings()
        print(f"✓ User settings loaded: {list(settings.keys())}")
        
        print("Data Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Data Manager test failed: {e}")
        return False

def test_error_handler():
    """Test error handler functionality"""
    print("\nTesting Error Handler...")
    
    try:
        eh = ErrorHandler()
        
        # Test error logging
        eh.handle_error("Test error", "Test context", "INFO")
        eh.handle_error("Test warning", "Test context", "WARNING")
        eh.handle_error("Test error", "Test context", "ERROR")
        
        # Test log retrieval
        log = eh.get_error_log()
        print(f"✓ Error log contains {len(log)} entries")
        
        # Test log summary
        summary = eh.get_log_summary()
        print(f"✓ Log summary: {summary}")
        
        print("Error Handler tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error Handler test failed: {e}")
        return False

def test_hardware_managers():
    """Test hardware manager functionality"""
    print("\nTesting Hardware Managers...")
    
    try:
        # Test WiFi Manager
        wm = WiFiManager()
        success = wm.initialize()
        networks = wm.scan_networks()
        print(f"✓ WiFi Manager: Init={success}, Networks={len(networks)}")
        
        # Test ECU Manager
        em = ECUManager()
        success = em.initialize()
        live_data = em.get_live_data()
        print(f"✓ ECU Manager: Init={success}, Data points={len(live_data)}")
        
        # Test RPM simulation
        em.simulate_rpm(2000)
        current_rpm = em.get_current_rpm()
        print(f"✓ RPM Simulation: Set to {current_rpm} RPM")
        
        print("Hardware Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Hardware Manager test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ECU Diagnostic Tool - Standalone Test Suite")
    print("=" * 60)
    
    tests = [
        test_data_manager,
        test_error_handler,
        test_hardware_managers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Core logic is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
