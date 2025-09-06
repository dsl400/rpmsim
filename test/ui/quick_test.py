#!/usr/bin/env python3
"""
Quick UI Test for ECU Diagnostic Tool
Runs a subset of critical UI tests for rapid feedback
"""

try:
    import utime as time
    import usys as sys
except ImportError:
    import time
    import sys
import lvgl as lv

# Add src and test directories to path
sys.path.append('src')
sys.path.append('test')

def quick_test():
    """Run quick UI tests for critical functionality"""
    print("=" * 50)
    print("ECU DIAGNOSTIC TOOL - QUICK UI TEST")
    print("=" * 50)
    
    # Initialize LVGL
    lv.init()
    
    # Create display driver
    disp_drv = lv.sdl_window_create(800, 480)
    lv.sdl_window_set_resizeable(disp_drv, False)
    lv.sdl_window_set_title(disp_drv, "ECU Tool - Quick Test")
    
    # Create input driver
    mouse = lv.sdl_mouse_create()
    
    test_results = []
    
    # Test 1: Main Screen Basic Functionality
    try:
        print("\n1. Testing Main Screen...")
        from ui.test_main_screen import MainScreenUITest
        main_test = MainScreenUITest()
        
        # Run only critical tests
        if main_test.setup_test_environment():
            if main_test.test_toolbar_elements():
                test_results.append(("Main Screen - Toolbar", "PASS"))
            else:
                test_results.append(("Main Screen - Toolbar", "FAIL"))
            
            if main_test.test_menu_button_interaction():
                test_results.append(("Main Screen - Menu", "PASS"))
            else:
                test_results.append(("Main Screen - Menu", "FAIL"))
        
        main_test.cleanup()
        
    except Exception as e:
        test_results.append(("Main Screen", f"ERROR: {e}"))
    
    # Test 2: RPM Simulator Critical Functions
    try:
        print("\n2. Testing RPM Simulator...")
        from ui.test_rpm_simulator_screen import RPMSimulatorUITest
        rpm_test = RPMSimulatorUITest()
        
        if rpm_test.setup_test_environment():
            if rpm_test.test_rpm_display_elements():
                test_results.append(("RPM Simulator - Display", "PASS"))
            else:
                test_results.append(("RPM Simulator - Display", "FAIL"))
            
            if rpm_test.test_rpm_slider_interaction():
                test_results.append(("RPM Simulator - Slider", "PASS"))
            else:
                test_results.append(("RPM Simulator - Slider", "FAIL"))
        
        rpm_test.cleanup()
        
    except Exception as e:
        test_results.append(("RPM Simulator", f"ERROR: {e}"))
    
    # Test 3: System Selection Navigation
    try:
        print("\n3. Testing System Selection...")
        from ui.test_system_selection_screen import SystemSelectionUITest
        selection_test = SystemSelectionUITest()
        
        if selection_test.setup_test_environment():
            if selection_test.test_initial_screen_elements():
                test_results.append(("System Selection - Elements", "PASS"))
            else:
                test_results.append(("System Selection - Elements", "FAIL"))
        
        selection_test.cleanup()
        
    except Exception as e:
        test_results.append(("System Selection", f"ERROR: {e}"))
    
    # Print Results
    print("\n" + "=" * 50)
    print("QUICK TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    failed = 0
    errors = 0
    
    for test_name, result in test_results:
        if result == "PASS":
            print(f"✓ {test_name}: PASSED")
            passed += 1
        elif result == "FAIL":
            print(f"✗ {test_name}: FAILED")
            failed += 1
        else:
            print(f"⚠ {test_name}: {result}")
            errors += 1
    
    total = len(test_results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\nSummary: {passed}/{total} tests passed ({success_rate:.1f}%)")
    print(f"Failed: {failed}, Errors: {errors}")
    
    if failed == 0 and errors == 0:
        print("\n🎉 Quick test PASSED - Core UI functionality working!")
        return True
    else:
        print("\n❌ Quick test FAILED - Issues detected in core UI")
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
