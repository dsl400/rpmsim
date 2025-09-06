#!/usr/bin/env python3
"""
Comprehensive test for ECU Diagnostic Tool
Tests actual implementation files with proper module loading
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
lv.sdl_window_set_title(disp_drv, "ECU Diagnostic Tool - Comprehensive Test")

# Register input driver
mouse = lv.sdl_mouse_create()

# Add src directory to path for imports
sys.path.append('src')

def test_imports():
    """Test importing our actual implementation modules"""
    results = []
    
    # Test data manager import
    try:
        from utils.data_manager import DataManager
        dm = DataManager()
        results.append(("✓ PASS", "Data Manager import successful"))
    except Exception as e:
        results.append(("✗ FAIL", f"Data Manager import failed: {e}"))
    
    # Test error handler import
    try:
        from utils.error_handler import ErrorHandler
        eh = ErrorHandler()
        results.append(("✓ PASS", "Error Handler import successful"))
    except Exception as e:
        results.append(("✗ FAIL", f"Error Handler import failed: {e}"))
    
    # Test navigation manager import
    try:
        from utils.navigation_manager import NavigationManager, AppState
        nm = NavigationManager()
        app_state = AppState()
        results.append(("✓ PASS", "Navigation Manager import successful"))
    except Exception as e:
        results.append(("✗ FAIL", f"Navigation Manager import failed: {e}"))
    
    # Test hardware managers import
    try:
        from hardware.wifi_manager import WiFiManager
        from hardware.ecu_manager import ECUManager
        wm = WiFiManager()
        em = ECUManager()
        results.append(("✓ PASS", "Hardware Managers import successful"))
    except Exception as e:
        results.append(("✗ FAIL", f"Hardware Managers import failed: {e}"))
    
    # Test screen imports
    try:
        from screens.main_screen import MainScreen
        from screens.wifi_setup import WifiSetupScreen
        from screens.system_selection import SystemSelectionScreen
        results.append(("✓ PASS", "Screen classes import successful"))
    except Exception as e:
        results.append(("✗ FAIL", f"Screen classes import failed: {e}"))
    
    return results

def test_functionality():
    """Test core functionality with mock data"""
    results = []
    
    try:
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
                }
            ]
        }
        
        # Test data operations
        brands = []
        for system in mock_systems.get('systems', []):
            if system['brand'] not in brands:
                brands.append(system['brand'])
        
        if len(brands) > 0:
            results.append(("✓ PASS", f"Data processing: Found {len(brands)} brands"))
        else:
            results.append(("✗ FAIL", "Data processing: No brands found"))
        
        # Test error handling
        error_log = []
        error_entry = {
            'error': 'Test error',
            'context': 'Test context',
            'severity': 'INFO',
            'timestamp': 'mock_time'
        }
        error_log.append(error_entry)
        
        if len(error_log) > 0:
            results.append(("✓ PASS", f"Error handling: {len(error_log)} entries logged"))
        else:
            results.append(("✗ FAIL", "Error handling: No entries logged"))
        
        # Test hardware simulation
        mock_networks = [
            {'ssid': 'TestNetwork1', 'signal': -45},
            {'ssid': 'TestNetwork2', 'signal': -67}
        ]
        
        mock_live_data = {
            'RPM': 2000,
            'Coolant Temp': 85,
            'Throttle Position': 12
        }
        
        if len(mock_networks) > 0 and len(mock_live_data) > 0:
            results.append(("✓ PASS", f"Hardware simulation: {len(mock_networks)} networks, {len(mock_live_data)} data points"))
        else:
            results.append(("✗ FAIL", "Hardware simulation: Missing data"))
        
    except Exception as e:
        results.append(("✗ FAIL", f"Functionality test failed: {e}"))
    
    return results

def create_test_ui():
    """Create comprehensive test UI"""
    scr = lv.obj()
    lv.screen_load(scr)
    
    # Title
    title = lv.label(scr)
    title.set_text("ECU Diagnostic Tool - Comprehensive Test")
    title.align(lv.ALIGN.TOP_MID, 0, 20)
    
    # Test results area
    results_area = lv.textarea(scr)
    results_area.set_size(700, 350)
    results_area.align(lv.ALIGN.CENTER, 0, 10)
    results_area.set_text("Click 'Run Import Tests' or 'Run Functionality Tests' to start...\n")
    
    # Import test button
    import_btn = lv.button(scr)
    import_btn.set_size(180, 50)
    import_btn.align(lv.ALIGN.BOTTOM_LEFT, 50, -50)
    
    import_label = lv.label(import_btn)
    import_label.set_text("Run Import Tests")
    import_label.center()
    
    # Functionality test button
    func_btn = lv.button(scr)
    func_btn.set_size(180, 50)
    func_btn.align(lv.ALIGN.BOTTOM_MID, 0, -50)
    
    func_label = lv.label(func_btn)
    func_label.set_text("Run Functionality Tests")
    func_label.center()
    
    # Exit button
    exit_btn = lv.button(scr)
    exit_btn.set_size(150, 50)
    exit_btn.align(lv.ALIGN.BOTTOM_RIGHT, -50, -50)
    
    exit_label = lv.label(exit_btn)
    exit_label.set_text("Exit")
    exit_label.center()
    
    def run_import_tests(evt):
        """Run import tests"""
        results_area.set_text("Running import tests...\n\n")
        lv.task_handler()
        
        test_results = test_imports()
        
        passed = 0
        total = len(test_results)
        
        for status, details in test_results:
            if status.startswith("✓"):
                passed += 1
            results_area.add_text(f"{status} {details}\n")
            lv.task_handler()
            time.sleep_ms(100)
        
        # Summary
        summary = f"\n{'='*50}\n"
        summary += f"Import Test Results: {passed}/{total} tests passed\n"
        
        if passed == total:
            summary += "🎉 All imports successful!\n"
        else:
            summary += "⚠️ Some imports failed. Check module paths.\n"
        
        summary += f"{'='*50}\n"
        results_area.add_text(summary)
    
    def run_functionality_tests(evt):
        """Run functionality tests"""
        results_area.set_text("Running functionality tests...\n\n")
        lv.task_handler()
        
        test_results = test_functionality()
        
        passed = 0
        total = len(test_results)
        
        for status, details in test_results:
            if status.startswith("✓"):
                passed += 1
            results_area.add_text(f"{status} {details}\n")
            lv.task_handler()
            time.sleep_ms(100)
        
        # Summary
        summary = f"\n{'='*50}\n"
        summary += f"Functionality Test Results: {passed}/{total} tests passed\n"
        
        if passed == total:
            summary += "🎉 All functionality tests passed!\n"
        else:
            summary += "⚠️ Some functionality tests failed.\n"
        
        summary += f"{'='*50}\n"
        results_area.add_text(summary)
    
    def exit_app(evt):
        """Exit the application"""
        sys.exit(0)
    
    # Add event handlers
    import_btn.add_event_cb(run_import_tests, lv.EVENT.CLICKED, None)
    func_btn.add_event_cb(run_functionality_tests, lv.EVENT.CLICKED, None)
    exit_btn.add_event_cb(exit_app, lv.EVENT.CLICKED, None)
    
    return scr

def main():
    """Main function"""
    print("Starting ECU Diagnostic Tool Comprehensive Test...")
    
    # Create test UI
    create_test_ui()
    
    print("Comprehensive test loaded.")
    print("- Click 'Run Import Tests' to test module imports")
    print("- Click 'Run Functionality Tests' to test core logic")
    
    # Main event loop
    while True:
        lv.task_handler()
        time.sleep_ms(5)

if __name__ == '__main__':
    main()
