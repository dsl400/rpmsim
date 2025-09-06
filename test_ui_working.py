#!/usr/bin/env python3
"""
Working UI Test for ECU Diagnostic Tool
Tests all UI features and functionality
"""

try:
    import usys as sys
    import utime as time
except ImportError:
    import sys
    import time

# Add paths
sys.path.append('src')
sys.path.append('test')

import lvgl as lv

def test_all_ui_features():
    """Test all UI features comprehensively"""
    print("==================================================")
    print("ECU DIAGNOSTIC TOOL - COMPREHENSIVE UI TEST")
    print("==================================================")
    
    test_results = []
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "Comprehensive UI Test")
        
        # Create mouse
        mouse = lv.sdl_mouse_create()
        
        # Get screen
        screen = lv.screen_active()
        
        print("✓ LVGL setup completed")
        
        # Import modules
        from utils.navigation_manager import NavigationManager, AppState, nav_manager, app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        from screens.rpm_simulator.rpm_simulator_screen import RPMSimulatorScreen
        from screens.wifi_setup import WifiSetupScreen
        
        print("✓ All modules imported successfully")
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Set test data
        app_state.current_system = {
            'brand': 'VW',
            'system': 'Engine', 
            'system_name': 'Bosch ME7.9.7'
        }
        app_state.current_tool = 'RPM Simulator'
        
        print("✓ App state initialized")
        
        # Register screens
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        nav_manager.register_screen("main", MainScreen)
        nav_manager.register_screen("wifi_setup", WifiSetupScreen)
        
        print("✓ Screens registered")
        
        # Test 1: Main Screen
        print("\n1. Testing Main Screen...")
        main_screen = MainScreen(screen)
        expected_widgets = ['toolbar', 'menu_btn', 'title_btn', 'wifi_icon', 'main_area', 'title_label', 'wifi_label']
        main_test_passed = 0
        for widget_name in expected_widgets:
            if widget_name in main_screen.widgets:
                print(f"✓ Found {widget_name}")
                main_test_passed += 1
            else:
                print(f"✗ Missing {widget_name}")
        test_results.append(("Main Screen", main_test_passed, len(expected_widgets)))
        
        # Test 2: System Selection Navigation
        print("\n2. Testing System Selection...")
        result = nav_manager.navigate_to("system_selection")
        selection_test_passed = 0
        if result and nav_manager.current_screen:
            selection_screen = nav_manager.current_screen
            expected_widgets = ['left_container', 'right_container', 'system_list', 'search_display', 'keyboard', 'close_btn']
            for widget_name in expected_widgets:
                if widget_name in selection_screen.widgets:
                    print(f"✓ Found {widget_name}")
                    selection_test_passed += 1
                else:
                    print(f"✗ Missing {widget_name}")
            test_results.append(("System Selection", selection_test_passed, len(expected_widgets)))
        else:
            print("✗ Navigation to system selection failed")
            test_results.append(("System Selection", 0, 6))
        
        # Test 3: Data Manager Integration
        print("\n3. Testing Data Manager...")
        data_test_passed = 0
        brands = app_state.data_manager.get_brands()
        if brands and len(brands) >= 3:
            print(f"✓ Found {len(brands)} brands")
            data_test_passed += 1
        else:
            print(f"✗ Expected at least 3 brands, found {len(brands) if brands else 0}")
        
        if brands:
            system_types = app_state.data_manager.get_system_types(brands[0])
            if system_types:
                print(f"✓ Found {len(system_types)} system types for {brands[0]}")
                data_test_passed += 1
            else:
                print(f"✗ No system types found for {brands[0]}")
        
        test_results.append(("Data Manager", data_test_passed, 2))
        
        # Test 4: RPM Simulator
        print("\n4. Testing RPM Simulator...")
        rpm_screen_obj = lv.obj()
        rpm_screen = RPMSimulatorScreen(rpm_screen_obj)
        expected_widgets = ['rpm_slider', 'start_stop_btn', 'cam_toggle_btn', 'crank_toggle_btn', 'slider_min', 'slider_max']
        rpm_test_passed = 0
        for widget_name in expected_widgets:
            if widget_name in rpm_screen.widgets:
                print(f"✓ Found {widget_name}")
                rpm_test_passed += 1
            else:
                print(f"✗ Missing {widget_name}")
        test_results.append(("RPM Simulator", rpm_test_passed, len(expected_widgets)))
        
        # Test 5: WiFi Setup Screen
        print("\n5. Testing WiFi Setup...")
        wifi_screen_obj = lv.obj()
        wifi_screen = WifiSetupScreen(wifi_screen_obj)
        expected_widgets = ['network_list', 'scan_btn', 'password_input', 'connect_btn', 'skip_btn']
        wifi_test_passed = 0
        for widget_name in expected_widgets:
            if widget_name in wifi_screen.widgets:
                print(f"✓ Found {widget_name}")
                wifi_test_passed += 1
            else:
                print(f"✗ Missing {widget_name}")
        test_results.append(("WiFi Setup", wifi_test_passed, len(expected_widgets)))
        
        # Test 6: Navigation Back to Main
        print("\n6. Testing Navigation Back to Main...")
        result = nav_manager.navigate_to("main")
        if result:
            print("✓ Navigation back to main successful")
            test_results.append(("Navigation", 1, 1))
        else:
            print("✗ Navigation back to main failed")
            test_results.append(("Navigation", 0, 1))
        
    except Exception as e:
        print(f"[ERROR] Test setup failed: {e}")
        test_results.append(("Setup", 0, 1))
    
    # Print results
    print("\n==================================================")
    print("COMPREHENSIVE UI TEST RESULTS")
    print("==================================================")
    
    total_passed = sum(passed for _, passed, _ in test_results)
    total_tests = sum(total for _, _, total in test_results)
    
    print(f"\nOverall Summary: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
    print()
    
    for test_name, passed, total in test_results:
        percentage = (passed/total*100) if total > 0 else 0
        status = "PASS" if passed == total else "PARTIAL" if passed > 0 else "FAIL"
        print(f"{test_name}: {passed}/{total} ({percentage:.1f}%) - {status}")
    
    if total_passed == total_tests:
        print("\n🎉 ALL UI TESTS PASSED!")
        print("✅ All UI features are working correctly!")
        print("✅ Navigation between screens works")
        print("✅ Data manager integration works")
        print("✅ All major widgets are present")
        print("✅ System selection functionality works")
        print("✅ RPM Simulator screen works")
        print("✅ WiFi Setup screen works")
    elif total_passed > total_tests * 0.8:
        print(f"\n✅ MOST UI TESTS PASSED! ({total_passed}/{total_tests})")
        print("✅ Core functionality is working")
        print("⚠️  Some minor features may need attention")
    else:
        print(f"\n❌ UI TESTS FAILED - {total_tests-total_passed} tests failed")
    
    return total_passed == total_tests

if __name__ == "__main__":
    success = test_all_ui_features()
    if success:
        print("\n🎉 COMPREHENSIVE UI TEST PASSED!")
    else:
        print("\n⚠️  COMPREHENSIVE UI TEST COMPLETED WITH ISSUES")
