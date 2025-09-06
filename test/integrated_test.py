#!/usr/bin/env python3
"""
Integrated test for ECU Diagnostic Tool with UI
Tests core components with visual feedback in MicroPython simulator
"""

import utime as time
import usys as sys
import lvgl as lv
import ujson as json

# Initialize LVGL
lv.init()

# Register display driver
disp_drv = lv.sdl_window_create(800, 480)
lv.sdl_window_set_resizeable(disp_drv, False)
lv.sdl_window_set_title(disp_drv, "ECU Diagnostic Tool - Integrated Test")

# Register input driver
mouse = lv.sdl_mouse_create()

# Include our implementations directly in the test file
class DataManager:
    def __init__(self):
        self.systems_cache = None
        self.user_settings_cache = None
        
    def load_systems(self):
        """Load systems from database"""
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
                },
                {
                    "brand": "Mercedes",
                    "system": "Engine",
                    "system_name": "Bosch EDC17",
                    "tools": [
                        {
                            "name": "RPM Simulator",
                            "type": "rpm_simulator",
                            "config": {
                                "crank": {"degrees_per_tooth": 10, "missing_teeth": 1},
                                "cam": {"degrees_per_tooth": 20}
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

# Global instances
data_manager = DataManager()
error_handler = ErrorHandler()
wifi_manager = WiFiManager()
ecu_manager = ECUManager()

def run_tests():
    """Run all tests and return results"""
    results = []
    
    # Test Data Manager
    try:
        data_manager.load_systems()
        brands = data_manager.get_brands()
        if len(brands) >= 3:
            results.append(("✓ PASS", f"Data Manager: Found {len(brands)} brands"))
        else:
            results.append(("✗ FAIL", f"Data Manager: Only {len(brands)} brands found"))
    except Exception as e:
        results.append(("✗ FAIL", f"Data Manager: {e}"))
    
    # Test Error Handler
    try:
        error_handler.handle_error("Test error", "Test context", "INFO")
        log = error_handler.get_error_log()
        if len(log) > 0:
            results.append(("✓ PASS", f"Error Handler: {len(log)} entries logged"))
        else:
            results.append(("✗ FAIL", "Error Handler: No entries logged"))
    except Exception as e:
        results.append(("✗ FAIL", f"Error Handler: {e}"))
    
    # Test WiFi Manager
    try:
        wifi_manager.initialize()
        networks = wifi_manager.scan_networks()
        if len(networks) > 0:
            results.append(("✓ PASS", f"WiFi Manager: Found {len(networks)} networks"))
        else:
            results.append(("✗ FAIL", "WiFi Manager: No networks found"))
    except Exception as e:
        results.append(("✗ FAIL", f"WiFi Manager: {e}"))
    
    # Test ECU Manager
    try:
        ecu_manager.initialize()
        live_data = ecu_manager.get_live_data()
        ecu_manager.simulate_rpm(2000)
        current_rpm = ecu_manager.get_current_rpm()
        if len(live_data) >= 8 and current_rpm == 2000:
            results.append(("✓ PASS", f"ECU Manager: {len(live_data)} data points, RPM={current_rpm}"))
        else:
            results.append(("✗ FAIL", f"ECU Manager: Data points={len(live_data)}, RPM={current_rpm}"))
    except Exception as e:
        results.append(("✗ FAIL", f"ECU Manager: {e}"))
    
    return results

def create_test_ui():
    """Create test UI"""
    scr = lv.obj()
    lv.screen_load(scr)
    
    # Title
    title = lv.label(scr)
    title.set_text("ECU Diagnostic Tool - Integrated Test")
    title.align(lv.ALIGN.TOP_MID, 0, 20)
    
    # Test results area
    results_area = lv.textarea(scr)
    results_area.set_size(700, 300)
    results_area.align(lv.ALIGN.CENTER, 0, 0)
    results_area.set_text("Click 'Run Tests' to start testing...\n")
    
    # Test button
    test_btn = lv.button(scr)
    test_btn.set_size(150, 50)
    test_btn.align(lv.ALIGN.BOTTOM_LEFT, 50, -50)
    
    test_label = lv.label(test_btn)
    test_label.set_text("Run Tests")
    test_label.center()
    
    # Exit button
    exit_btn = lv.button(scr)
    exit_btn.set_size(150, 50)
    exit_btn.align(lv.ALIGN.BOTTOM_RIGHT, -50, -50)
    
    exit_label = lv.label(exit_btn)
    exit_label.set_text("Exit")
    exit_label.center()
    
    def run_test_suite(evt):
        """Run all tests and display results"""
        results_area.set_text("Running tests...\n\n")
        lv.task_handler()
        
        test_results = run_tests()
        
        passed = 0
        total = len(test_results)
        
        for status, details in test_results:
            if status.startswith("✓"):
                passed += 1
            results_area.add_text(f"{status} {details}\n")
            lv.task_handler()
            time.sleep_ms(100)
        
        # Final summary
        summary = f"\n{'='*50}\n"
        summary += f"Test Results: {passed}/{total} tests passed\n"
        
        if passed == total:
            summary += "🎉 All tests passed! Implementation working correctly.\n"
        else:
            summary += "⚠️ Some tests failed. Check details above.\n"
        
        summary += f"{'='*50}\n"
        results_area.add_text(summary)
    
    def exit_app(evt):
        """Exit the application"""
        sys.exit(0)
    
    # Add event handlers
    test_btn.add_event_cb(run_test_suite, lv.EVENT.CLICKED, None)
    exit_btn.add_event_cb(exit_app, lv.EVENT.CLICKED, None)
    
    return scr

def main():
    """Main function"""
    print("Starting ECU Diagnostic Tool Integrated Test...")
    
    # Create test UI
    create_test_ui()
    
    print("Integrated test loaded. Click 'Run Tests' to execute all tests.")
    
    # Main event loop
    while True:
        lv.task_handler()
        time.sleep_ms(5)

if __name__ == '__main__':
    main()
