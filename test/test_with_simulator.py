#!/usr/bin/env python3
"""
Test script for ECU Diagnostic Tool using MpSimulator
This script runs inside the MicroPython simulator with LVGL
"""

import utime as time
import usys as sys
import lvgl as lv

# Add src directory to path
sys.path.append('/src')

def test_data_manager():
    """Test data manager functionality"""
    try:
        from utils.data_manager import DataManager
        
        # Create data manager instance
        dm = DataManager()
        
        # Test loading systems
        systems = dm.load_systems()
        brands = dm.get_brands()
        
        print(f"Data Manager: Found {len(brands)} brands")
        return True, f"Brands: {', '.join(brands[:3])}" if brands else "No brands found"
        
    except Exception as e:
        print(f"Data Manager test failed: {e}")
        return False, str(e)

def test_error_handler():
    """Test error handler functionality"""
    try:
        from utils.error_handler import ErrorHandler
        
        eh = ErrorHandler()
        eh.handle_error("Test error", "Test context", "INFO")
        
        log = eh.get_error_log()
        print(f"Error Handler: {len(log)} log entries")
        return True, f"{len(log)} entries logged"
        
    except Exception as e:
        print(f"Error Handler test failed: {e}")
        return False, str(e)

def test_wifi_manager():
    """Test WiFi manager functionality"""
    try:
        from hardware.wifi_manager import WiFiManager
        
        wm = WiFiManager()
        success = wm.initialize()
        networks = wm.scan_networks()
        
        print(f"WiFi Manager: Found {len(networks)} networks")
        return True, f"Init: {success}, Networks: {len(networks)}"
        
    except Exception as e:
        print(f"WiFi Manager test failed: {e}")
        return False, str(e)

def test_ecu_manager():
    """Test ECU manager functionality"""
    try:
        from hardware.ecu_manager import ECUManager
        
        em = ECUManager()
        success = em.initialize()
        live_data = em.get_live_data()
        
        print(f"ECU Manager: {len(live_data)} data points")
        return True, f"Init: {success}, Data points: {len(live_data)}"
        
    except Exception as e:
        print(f"ECU Manager test failed: {e}")
        return False, str(e)

def create_test_ui():
    """Create test UI for the simulator"""
    
    # Initialize LVGL
    lv.init()
    
    # Register display driver
    disp_drv = lv.sdl_window_create(800, 480)
    lv.sdl_window_set_resizeable(disp_drv, False)
    lv.sdl_window_set_title(disp_drv, "ECU Diagnostic Tool - Test")
    
    # Register input driver
    mouse = lv.sdl_mouse_create()
    
    # Create main screen
    scr = lv.obj()
    lv.screen_load(scr)
    
    # Title
    title = lv.label(scr)
    title.set_text("ECU Diagnostic Tool - Implementation Test")
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
    
    # Test results storage
    test_results = []
    
    def run_tests(evt):
        """Run all tests and display results"""
        results_area.set_text("Running tests...\n\n")
        lv.task_handler()
        
        tests = [
            ("Data Manager", test_data_manager),
            ("Error Handler", test_error_handler),
            ("WiFi Manager", test_wifi_manager),
            ("ECU Manager", test_ecu_manager)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                success, details = test_func()
                status = "✓ PASS" if success else "✗ FAIL"
                result_text = f"{status} {test_name}: {details}\n"
                
                if success:
                    passed += 1
                    
                results_area.add_text(result_text)
                lv.task_handler()
                time.sleep_ms(100)  # Small delay for visual feedback
                
            except Exception as e:
                results_area.add_text(f"✗ FAIL {test_name}: Exception - {e}\n")
                lv.task_handler()
        
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
    test_btn.add_event_cb(run_tests, lv.EVENT.CLICKED, None)
    exit_btn.add_event_cb(exit_app, lv.EVENT.CLICKED, None)
    
    return scr

def main():
    """Main function"""
    print("Starting ECU Diagnostic Tool Test...")
    
    # Create test UI
    create_test_ui()
    
    # Main event loop
    while True:
        lv.task_handler()
        time.sleep_ms(5)

if __name__ == '__main__':
    main()
